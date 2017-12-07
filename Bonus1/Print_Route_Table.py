#!/usr/bin/env python
"""
Ex 3. Display the SRX's routing table. You will probably want to use RouteTable for this
(from jnpr.junos.op.routes import RouteTable).

The output should look similiar to the following:

Juniper SRX Routing Table:

0.0.0.0/0
  nexthop 10.220.88.1
  age 14582542
  via vlan.0
  protocol Static

10.220.88.0/24
  nexthop None
  age 14583120
  via vlan.0
  protocol Direct

10.220.88.39/32
  nexthop None
  age 14583289
  via vlan.0
  protocol Local


"""
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