#!/usr/bin/env python

from jnpr.junos import Device
from jnpr.junos.op.routes import RouteTable
from getpass import getpass
from pprint import pprint

USER = 'pyclass'


def main():
    pwd = getpass()

    a_device = Device(host='184.105.247.76', user=USER, password = pwd)
    a_device.open()

    routes = RouteTable(a_device)
    routes.get()

    print

    for k, v in routes.items():
        print k
        for info, stat in v:
            print("{} {}".format(info, stat))
        print

    print

if __name__ == "__main__":
    main()