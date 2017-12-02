#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

from getpass import getpass
from pprint import pprint

from napalm_base import get_network_driver
import yaml

YAML_FILE = 'my_devices.yml'

def get_napalm_info(napalm_obj, napalm_method, banner=""):
    my_method = getattr(napalm_obj, napalm_method)
    print('*' * 80)
    pprint(my_method())
    print('*' * 80)


def main():
    with open(YAML_FILE) as f:
        my_devices = yaml.load(f)

    pwd = getpass()

    command_list = ['get_facts', 'get_interfaces', 'get_bgp_neighbors']
    for device_dict in my_devices:
        if device_dict['device_type'] == 'eos':
            my_device = device_dict
            break
    device_type = my_device.pop('device_type')
    my_device['password'] = pwd
    driver = get_network_driver(device_type)
    device = driver(**my_device)
    device.open()
    facts = device.get_facts()
    print
    print("Device Type: {:<20} Hostname: {:<20} Model: {:<20}".format(device_type, my_device['hostname'], facts["model"]))
    print
    for cmd in command_list:
        raw_input("Hit enter to continue:")
        print()
        print("{} output:".format(cmd))
        get_napalm_info(device, cmd, "")


if __name__ == "__main__":
    main()
