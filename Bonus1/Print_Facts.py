#!/usr/bin/env python


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