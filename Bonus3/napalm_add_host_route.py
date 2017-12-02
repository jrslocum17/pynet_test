#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

from getpass import getpass
from pprint import pprint
from napalm_base import get_network_driver
from pyeapi.eapilib import CommandError
import yaml

YAML_FILE = 'my_devices.yml'
CFG_FILE = 'ios_host_route.cfg'


def main():
    with open(YAML_FILE) as f:
        my_devices = yaml.load(f)

    pwd = getpass()

    for device_dict in my_devices:
        if device_dict['device_type'] == 'ios':
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
    print("Load config change (merge)")
    device.load_merge_candidate(filename=CFG_FILE)
    print(device.compare_config())
    print()
    raw_input("Hit enter to continue: ")
    print("Discarding configuration...")
    device.discard_config()
    print("Config comparison (should be empty)")
    print(device.compare_config())
    print()
    raw_input("Hit enter to continue: ")
    print("Reloading configuration...")
    device.load_merge_candidate(filename=CFG_FILE)
    print(device.compare_config())
    print("Committing change...")
    device.commit_config()
    print()


if __name__ == "__main__":
    main()
