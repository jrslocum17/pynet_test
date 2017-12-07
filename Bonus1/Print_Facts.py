#!/usr/bin/env python
"""
Ex 1. Use Juniper's PyEZ library to make a connection to the Juniper SRX and to print out the device's facts.
"""

from jnpr.junos import Device
from getpass import getpass
from pprint import pprint


def main():
    pwd = getpass()

    a_device = Device(host='184.105.247.76', user = 'pyclass', password = pwd)
    a_device.open()

    pprint(a_device.facts)


if __name__ == "__main__":
    main()