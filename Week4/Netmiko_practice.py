#!/usr/bin/env python
"""
5. Use Netmiko to enter into configuration mode on pynet-rtr2. Also use Netmiko to verify your state
(i.e. that you are currently in configuration mode).
6. Use Netmiko to execute 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.
7. Use Netmiko to change the logging buffer size (logging buffered <size>) on pynet-rtr2.
8. Use Netmiko to change the logging buffer size (logging buffered <size>) and to disable console logging
(no logging console) from a file on both pynet-rtr1 and pynet-rtr2 (see 'Errata and Other Info, item #4).
"""

from netmiko import ConnectHandler
from datetime import datetime

pynet1 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.70',
    'username': 'pyclass',
    'password': '88newclass',
    'port': 22
}
pynet2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': '88newclass',
    'port': 22
}
srx = {
    'device_type': 'juniper',
    'ip': '184.105.247.76',
    'username': 'pyclass',
    'password': '88newclass',
    'port': 22
}

def run_show_commands(remote_conns, commands):
    output = ""
    for remote_conn in remote_conns:
        for command in commands:
            output += "{} output from {}:\n".format(command, remote_conn.find_prompt())
            output += remote_conn.send_command(command)
            output += "\n\n"
    return output


def main():
    print "\nStart time: " + str(datetime.now())

    pynet_rtr2 = ConnectHandler(**pynet2)
    current_prompt = pynet_rtr2.find_prompt()
    print("The current prompt is: " + current_prompt)
    pynet_rtr2.config_mode()
    is_cfg_mode = pynet_rtr2.check_config_mode()
    print("The router is in config mode: " + str(is_cfg_mode))
    current_prompt = pynet_rtr2.find_prompt()
    print("The updated prompt is: " + current_prompt)
    pynet_rtr2.exit_config_mode()

    pynet_rtr1 = ConnectHandler(**pynet1)
    srx_rtr = ConnectHandler(**srx)

    arp_output = run_show_commands([pynet_rtr1, pynet_rtr2, srx_rtr], ['show arp'])
    print(arp_output)

    outp = pynet_rtr2.send_command("show run | include logging")
    print("Previous logging commands for pynet2: " + outp)
    config_commands = ['logging buffered 16384', 'no logging console']
    pynet_rtr2.send_config_set(config_commands)
    outp = pynet_rtr2.send_command("show run | include logging")
    print("New logging commands for pynet2: " + outp)

    print("Previous logging commands:\n" + run_show_commands([pynet_rtr1, pynet_rtr2], ['show run | inc logging']))
    pynet_rtr1.send_config_from_file(config_file='Config_commands.txt')
    pynet_rtr2.send_config_from_file(config_file='Config_commands.txt')
    print("New logging commands:\n" + run_show_commands([pynet_rtr1, pynet_rtr2], ['show run | inc logging']))

    print "\nEnd time: " + str(datetime.now())

if __name__ == "__main__":
    main()