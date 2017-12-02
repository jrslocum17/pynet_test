#!/usr/bin/env python

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
