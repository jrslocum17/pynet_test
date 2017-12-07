#!/usr/bin/env python
"""
Ex 1. Construct a script that retrieves NAPALM facts from two IOS routers, two Arista switches, and one Junos device.
pynet-rtr1   (Cisco IOS)  184.105.247.70
pynet-rtr2   (Cisco IOS)  184.105.247.71
pynet-sw1    (Arista EOS) 184.105.247.72
pynet-sw2    (Arista EOS) 184.105.247.73
​juniper-srx               184.105.247.76

Retrieve the 'model' number from each device and print the model to standard out.

As part of this exercise define the devices that you use in a Python file (for example my_devices.py) and import
these devices into your program. Optionally, define the devices in a YAML file and read this my_devices.yml file in.

"""
from __future__ import print_function
from __future__ import unicode_literals

from getpass import getpass
from pprint import pprint
from napalm_base import get_network_driver
from pyeapi.eapilib import CommandError
import yaml
import re

YAML_FILE = 'my_devices.yml'


def main():
    with open(YAML_FILE) as f:
        my_devices = yaml.load(f)
    #pprint(my_devices)

    pwd = getpass()

    print("{:<20} {:<20} {:<20}".format("Device Type", "Hostname", "Model"))
    for device_dict in my_devices:
        device_dict['password'] = pwd
        device_type = device_dict.pop('device_type')
        driver = get_network_driver(device_type)
        device=driver(**device_dict)

        device.open()
        facts = device.get_facts()
        print('*' * 80)
        print("{:<20} {:<20} {:<20}".format(device_type, device_dict['hostname'], facts['model']))
        print('*' * 80)
        print


if __name__ == "__main__":
    main()
