#!/usr/bin/env python

'''
Use SNMPv3 to detect when a router configuration changes, and send an e-mail notfication

Write a class that stores state in a Python Pickle file, a .json file, or a .yml file.
    Pass the state file to be created / updated in the constructor
    Choode the method based on the filename specified.

Write a driver script (could be the main() method in the file) which could be called by a cron job.
    The driver would instantiate the config_changes class and read its state file

Ex 1. Using SNMPv3 create a script that detects router configuration changes.

If the running configuration has changed, then send an email notification to yourself identifying the router that changed and the time that it changed.

Note, the running configuration of pynet-rtr2 is changing every 15 minutes (roughly at 0, 15, 30, and 45 minutes after the hour).  This will allow you to test your script in the lab environment.

In this exercise, you will possibly need to save data to an external file. One way you can accomplish this is by using a pickle file, see:
    http://youtu.be/ZJOJjyhhEvM

A pickle file lets you save native Python data structures (dictionaries, lists, objects) directly to a file.

Here is some additional reference material that you will probably need to solve this problem:

Cisco routers have the following three OIDs:

# Uptime when running config last changed
ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'

# Uptime when running config last saved (note any 'write' constitutes a save)
ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'

# Uptime when startup config last saved
ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'

From the above descriptions, the router will save the sysUptime timestamp (OID sysUptime = 1.3.6.1.2.1.1.3.0) when a running configuration change occurs. The router will also record the sysUptime timestamp when the running configuration is saved to the startup config.
​Here is some data on the behavior of these OIDs. Note, sysUptime times are in hundredths of seconds so 317579 equals 3175.79 seconds (i.e. a bit less than one hour)


# After reboot
pynet-rtr2.twb-tech.com
317579        (sysUptime)
2440            (ccmHistoryRunningLastChanged--running-config is changed during boot)
0                  (ccmHistoryRunningLastSaved -- i.e. reset to 0 on reload)
0                  (ccmHistoryStartupLastChanged -- i.e. reset to 0 on reload)

# After config change on router (but no save to startup config)
pynet-rtr2.twb-tech.com
322522        (sysUptime)
322219        (ccmHistoryRunningLastChanged)
0                  (ccmHistoryRunningLastSaved)
0                  (ccmHistoryStartupLastChanged)


# After 'write mem' on router
pynet-rtr2.twb-tech.com
324543        (sysUptime)
322219        (ccmHistoryRunningLastChanged)
323912        (ccmHistoryRunningLastSaved)
323912        (ccmHistoryStartupLastChanged)


# After another configuration change (but no save to startup config)
pynet-rtr2.twb-tech.com
327177        (sysUptime)
326813        (ccmHistoryRunningLastChanged)
323912        (ccmHistoryRunningLastSaved)
323912        (ccmHistoryStartupLastChanged)


# After 'show run' command (note, this causes 'ccmHistoryRunningLastSaved' to
# increase i.e. 'write terminal' causes this OID to be updated)
pynet-rtr2.twb-tech.com
343223        (sysUptime)
326813        (ccmHistoryRunningLastChanged)
342898        (ccmHistoryRunningLastSaved)
323912        (ccmHistoryStartupLastChanged)


Bonus challenge: instead of saving your data in a pickle file, save the data using either a YAML or a JSON file.

My alternate solution supports pickle, YAML, or JSON depending on the name of the file (.pkl, .yml, or .json).



Input files:
    router list file:
        Contains a list of dictionaries, with the following format:
            [
                {
                    'router': 'hostname1',
                    'ip_addr': 'router1_ip_addr',
                    'community': 'snmp_community',
                    'port': snmp_port
                },
                {
                    'router': 'hostname2',
                    'ip_addr': 'router2_ip_addr',
                    'community': 'snmp_community',
                    'port': snmp_port
                }
            ]
    state file:
        Contains a dictionary of two dictionaries: lastRebootTime and lastConfigChangeTime.
        The router name is the key, and the time is the value.
            {
                'lastRebootTime': {
                    'router_name1': 1,
                    'router_name2': 22,
                    'router_name3': 333,
                    'router_name4': 4444,
                    'router_name5': 55555
                },
                'lastConfigChangeTime': {
                    'router_name1': 88888,
                    'router_name2': 77777,
                    'router_name3': 6666,
                    'router_name4': 54444,
                    'router_name5': 555552
                }
            }

Parameters:
    check interval in seconds
    Yaml file or json file containing state
    Yaml or Json file containing router list

Algorithm:
    load routerList from router list file
    Get current date from OS
    For router in routerList:
        SNMP-Get router sysUptime
        routerRebootTime = date - sysUptime
        SNMP-Get current ccmHistoryRunningLastChanged
        runningLastChangedTime = routerRebootTime + ccmHistoryRunningLastChanged
        runningConfigChanged = False
        If state file:
            routerRebootTimeS = stateFile.routerRebootTime
            runningLastChangedTimeS = stateFile.runningLastChangedTime
            If routerRebootTime > routerRebootTimeS
                routerRebooted = True
                routerRebootTimeS = routerRebootTime
            If runningLastChangedTime > runningLastChangedTimeS:
                If !routerRebooted or (ccmHistoryRunningLastChanged > ROUTER_REBOOT_SECONDS):
                    runningConfigChanged = True
                    runningLastChangedTimeS = runningLastChangedTime
            if runningConfigChanged:
                send email
        stateFile.dump(routerRebootTimeS, runningLastChangedTimeS)

'''
import sys
import pickle
import yaml
import json
import time
import snmp_helper
import email_helper
from collections import namedtuple

ROUTER_REBOOT_SECONDS = 300 * 100 # converted to timeticks aka 100ths of a second
PICKLE_STATE_FILE = "Router_Reboot_Check.p"
SYSUPTIME_OID = '1.3.6.1.2.1.1.3.0'
RUNNINGLASTCHANGED_OID = '1.3.6.1.4.1.9.9.43.1.1.1.0'
EMAIL_SUBJECT = "%s configuration change detected"
EMAIL_MESSAGE_BODY = "Configuration on router %s was last changed at %s"
DEBUG = False
NetworkDevice = namedtuple("my_name", "field1 field2 field3")

class Router_Reboot_Check(object):
    def __init__(self, router_list_file, state_file, email_sender, email_recipients,
                 router_reboot_seconds=ROUTER_REBOOT_SECONDS):
        self.router_list_file = router_list_file
        self.state_file = state_file
        self.email_sender = email_sender
        self.email_recipients = email_recipients
        self.router_reboot_seconds = router_reboot_seconds

        try:
            if router_list_file.endswith("yml"):
                self.router_list = yaml.load(open(router_list_file, 'r'))
            elif router_list_file.endswith("json"):
                self.router_list = json.load(open(router_list_file, 'r'))
            else:
                sys.exit("Must specify router list as a .yml or .json file")
        except IOError as ioe:
            sys.exit("Cannot load router list file: %s" % router_list_file)
        if DEBUG:
            print("Router List: " + str(self.router_list))
        try:
            if state_file.endswith("yml"):
                self.state = yaml.load(open(state_file, 'r'))
            elif state_file.endswith("json"):
                self.state = json.load(open(state_file, 'r'))
            else:
                self.state = pickle.load(open(PICKLE_STATE_FILE, 'rb'))
        except IOError as ioe:
            self.state = {}
        if DEBUG:
            print("State length: %s, State: %s" % (len(self.state), str(self.state)))

    def check_routers(self):
        timestamp = int(time.time())
        if DEBUG:
            print("My time is: %s" % time.ctime(timestamp))
        for router in self.router_list:
            routerRebooted = False
            routerTuple = (router['ip_addr'], router['community'], router['port'])
            routerUptimeOIDData = snmp_helper.snmp_get_oid(routerTuple, SYSUPTIME_OID)
            routerUptime = int(float(snmp_helper.snmp_extract(routerUptimeOIDData)) / 100)
            routerRebootTime = timestamp - routerUptime

            lastConfigChangeSecondsOIDData = snmp_helper.snmp_get_oid(routerTuple, RUNNINGLASTCHANGED_OID)
            lastConfigChangeSeconds = int(float(snmp_helper.snmp_extract(lastConfigChangeSecondsOIDData)) / 100)
            runningLastChangedTime = routerRebootTime + lastConfigChangeSeconds
            if DEBUG:
                print("Router: %s     uptime: %s    reboot time: %s    last config change seconds: %s    running last changed time %s" % (router['router'], routerUptime, time.ctime(routerRebootTime), lastConfigChangeSeconds, time.ctime(runningLastChangedTime)))

            if len(self.state) == 0:
                self.state['lastRebootTime'] = {}
                self.state['lastConfigChangeTime'] = {}
            if router['router'] not in self.state['lastRebootTime'].keys():
                self.state['lastRebootTime'][router['router']] = routerRebootTime
                self.state['lastConfigChangeTime'][router['router']] = runningLastChangedTime
            if routerRebootTime > self.state['lastRebootTime'][router['router']]:
                routerRebooted = True
                self.state['lastRebootTime'][router['router']] = routerRebootTime
            if runningLastChangedTime > self.state['lastConfigChangeTime'][router['router']]:
                if not routerRebooted or (lastConfigChangeSeconds > ROUTER_REBOOT_SECONDS):
                    self.__send_email_alert(router['router'], runningLastChangedTime)
                self.state['lastConfigChangeTime'][router['router']] = runningLastChangedTime
        self.__dump_state()

    def __send_email_alert(self, router_name, lastChangedTime):
        for email_recipient in self.email_recipients:
            subject = str(EMAIL_SUBJECT % router_name)
            message = str(EMAIL_MESSAGE_BODY % (router_name, time.ctime(lastChangedTime)))
            print("Sending mail to %s with subject \"%s\" and message \"%s\" from %s" %
                  (email_recipient, subject, message, self.email_sender))
            email_helper.send_mail(email_recipient, subject, message, self.email_sender)

    def __dump_state(self):
        try:
            if self.state_file.endswith("yml"):
                with open(self.state_file, "w") as f:
                    f.write(yaml.dump(self.state, default_flow_style=False))
            elif self.state_file.endswith("json"):
                json.dump(self.state, open(self.state_file, 'w'))
            else:
                pickle.dump(self.state, open(self.state_file, "wb"))
        except IOError:
            sys.exit("Could not write state file %s" % self.state_file)


def main():
    if len(sys.argv) < 4:
        sys.exit("Usage: %s <router_list_file> <email_sender> <email_recipient1> [state_file] [email_recipient2] ..." % sys.argv[0])
    router_list_file = sys.argv[1]
    email_sender = sys.argv[2]
    email_recipients = [sys.argv[3]]
    state_file = ""
    if len(sys.argv) > 4:
        if sys.argv[4].endswith("yml") or sys.argv[4].endswith("json"):
            state_file = sys.argv[4]
        else:
            email_recipients.append(sys.argv[4])
            state_file = PICKLE_STATE_FILE
    for remainingArg in sys.argv[5:len(sys.argv)]:
        email_recipients.append(remainingArg)
    if DEBUG:
        print("Script name: %s, router_list_file: %s, state_file: %s, email_sender: %s, email_recipients: %s"
              % (sys.argv[0], router_list_file, state_file, email_sender, str(email_recipients)))
    my_router_reboot_check = Router_Reboot_Check(router_list_file, state_file, email_sender, email_recipients)
    my_router_reboot_check.check_routers()

if __name__ == "__main__":
    main()
