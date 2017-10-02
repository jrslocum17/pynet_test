#!/usr/bin/env python

"""
Assignment 3-2:
Use SNMPv3 to create two SVG image files.

Image1: input/output bytes on pynet-rtr1-Fa4
Image2: input/output packets on pynet-rtr1-Fa4

Get bytes and packets every five minutes for an hour, compute the differences and graph each point over time

Relevant OIDs:

('ifDescr_fa4', '1.3.6.1.2.1.2.2.1.2.5')
('ifInOctets_fa4', '1.3.6.1.2.1.2.2.1.10.5')
('ifInUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.11.5')
('ifOutOctets_fa4', '1.3.6.1.2.1.2.2.1.16.5'),
('ifOutUcastPkts_fa4', '1.3.6.1.2.1.2.2.1.17.5')


Command line syntax:
]$ SNMP_Graphing <ip_addr> <username> <graph_file_name> <graphing_interval_minutes> <num_iterations> <ifDescr_OID>...
<OID1> [<OID2> [<OID3> [<OID4>]]]
<will prompt for SNMPv3 auth_key/encrypt_key>

Plan:
Create my_router object, get SNMP key, download data. If interval is specified, sleep for interval, do until
num_iterations. If interval is not specified, run once and terminate. Either way, store diffs in a data structure in
a pickle file.


"""

import pygal
import time
import sys
import pickle
import getpass
import os.path
import json
import snmp_helper


from collections import namedtuple

DEBUG = False
SNMP_PORT = 161
PICKLE_FILE = "SNMP_Graphing_pkl.p"
SYSNAME = "SysName"
DESCRIPTION = "ifDescr"


class RouterOID(object):
    """
    Represents a router OID, the keys to measure it, a list of time deltas that measurements were taken,
    and a list of the measurements taken at those times
    """
    def __init__(self, ip_addr, username, auth_encr_key, oid_name, oid):
        self.router = (ip_addr, SNMP_PORT)
        self.snmp_user = (username, auth_encr_key, auth_encr_key)
        self.oid_name = oid_name
        self.oid = oid
        self.timestamp = 0
        self.total_measurement = 0
        self.num_data_points = 0
        self.time_diff_list = []
        self.measurement_diff_list = []

    def add_data_point(self):
        timestamp = int(time.time())
        if self.timestamp:
            time_diff = timestamp - self.timestamp
        else:
            time_diff = 0
        self.timestamp = timestamp
        self.time_diff_list.append(time_diff)

        snmp_data = snmp_helper.snmp_get_oid_v3(self.router, self.snmp_user, self.oid)
        total_measurement = int(snmp_helper.snmp_extract(snmp_data))
        if self.total_measurement:
            diff_measurement = total_measurement - self.total_measurement
        else:
            diff_measurement = 0

        self.total_measurement = total_measurement
        self.measurement_diff_list.append(diff_measurement)
        self.num_data_points += 1

    def get_time_list(self, last_n_values):
        first_index = 0 - last_n_values
        return self.time_diff_list[first_index:]

    def get_measurement_list(self, last_n_values):
        first_index = 0 - last_n_values
        return self.measurement_diff_list[first_index:]

    def print_me(self):
        print """
        router: {0}
        snmp_user: {1}
        oid_name: {2}
        timestamp: {3}
        total_measurement: {4}
        num_data_points: {5}
        """.format(self.router, self.snmp_user, self.oid_name, self.timestamp, self.total_measurement, self.num_data_points)
        print "time_diff_list: "
        for element in self.time_diff_list:
            print element
        print "measurement_diff_list: "
        for element in self.measurement_diff_list:
            print element


def get_data(oid_name, snmp_oid_list, ip_addr, snmp_port, username, auth_encr_key):
    router = (ip_addr, snmp_port)
    snmp_user = (username, auth_encr_key, auth_encr_key)
    for OID in snmp_oid_list:
        if OID['OID_NAME'] == oid_name:
            target_OID = OID['OID_VALUE']
            snmp_data = snmp_helper.snmp_get_oid_v3(router, snmp_user, target_OID)
            return snmp_helper.snmp_extract(snmp_data)
        else:
            return ""


def main():
    if len(sys.argv) < 7:
        sys.exit(("Usage %s <ip_addr> <username> <oid_file_name.json> <graph_file_name> <graphing_interval_minutes>" +
                 " <num_iterations> <graph_max_iterations>") % sys.argv[0])
    ip_addr = sys.argv[1]
    username = sys.argv[2]
    oid_file_name = sys.argv[3]
    graph_file = sys.argv[4]
    graph_interval = int(sys.argv[5])
    num_iterations = int(sys.argv[6])
    graph_max_iterations = int(sys.argv[7])
    auth_key = getpass.getpass("Please enter auth/encryption key: ")
    if DEBUG:
        print """
ip address: {0}
username: {1}
auth/encr key: {2}
oid_file_name: {3}
graph_file: {4}
graph_interval: {5}
num_iterations: {6}
graph_max_iterations: {7}
""".format(ip_addr, username, auth_key, oid_file_name, graph_file, graph_interval, num_iterations, graph_max_iterations)

    try:
        with open(oid_file_name) as f:
            json_snmp_oid_list = json.load(f)
    except IOError:
        sys.exit("Could not open OID file for reading: " + oid_file_name)

    router_hostname = get_data(SYSNAME, json_snmp_oid_list, ip_addr, SNMP_PORT, username, auth_key)

    my_router_oid_obj_list = []
    pickle_file = router_hostname + ".pkl"
    if os.path.exists(pickle_file):
        my_router_oid_obj_list = pickle.load(open(pickle_file, 'rb'))
    else:
        for OID in json_snmp_oid_list:
            if OID['Is_Counter'] == "True":
                myRouterOIDObj = RouterOID(ip_addr, username, auth_key, OID['OID_NAME'], OID['OID_VALUE'])
                my_router_oid_obj_list.append(myRouterOIDObj)
    if graph_interval == 0:
        num_iterations = 1
    for i in range(0, num_iterations):
        for router_oid_obj in my_router_oid_obj_list:
            router_oid_obj.add_data_point()
        if graph_interval > 0:
            time.sleep(60*graph_interval)
    if DEBUG:
        i = 1
        for myobj in my_router_oid_obj_list:
            print "MyRouterOIDObj {0}: ".format(i)
            myobj.print_me()
            i += 1
        print "line chart title: " + router_hostname + " stats"
        print "time_list for max_iterations (" + str(graph_max_iterations) + "):"
        for time_element in my_router_oid_obj_list[0].get_time_list(graph_max_iterations):
            print " " + str(time_element)
        print "measurement_list:"
        for oidObj in my_router_oid_obj_list:
            print "OID: " + oidObj.oid_name
            for measElem in oidObj.get_measurement_list(graph_max_iterations):
                print " " + str(measElem)
    line_chart = pygal.Line()
    line_chart.title = router_hostname + " stats"
    line_chart.x_label = my_router_oid_obj_list[0].get_time_list(graph_max_iterations)
    for router_oid_obj in my_router_oid_obj_list:
        line_chart.add(router_oid_obj.oid_name, router_oid_obj.get_measurement_list(graph_max_iterations))
    line_chart.render_to_file(graph_file)

    try:
        pickle.dump(my_router_oid_obj_list, open(pickle_file, "wb"))
    except IOError:
        sys.exit("Could not write state file %s" % pickle_file)

if __name__ == "__main__":
    main()
