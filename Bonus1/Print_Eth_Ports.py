#!/usr/bin/env python
"""
Ex 2. For each of the SRX's interfaces, display: the operational state,
packets-in, and packets-out. You will probably want to use EthPortTable for
this.
"""
from jnpr.junos import Device
from jnpr.junos.op.ethport import EthPortTable
from getpass import getpass
from pprint import pprint

USER = 'pyclass'

def main():
    pwd = getpass()

    a_device = Device(host='184.105.247.76', user=USER, password = pwd)
    a_device.open()

    ports = EthPortTable(a_device)
    ports.get()

    print
    print "{:<20} {:<10} {:>20} {:>20}".format('interface', 'state', 'RX packets', 'TX packets')
    for intfc, tuple_list in ports.items():
        for info, stat in tuple_list:
            if info == 'oper':
                oper = stat
            elif info == 'rx_packets':
                rx_packets = stat
            elif info == 'tx_packets':
                tx_packets = stat
        print "{:<20} {:<10} {:>20} {:>20}".format(intfc, oper, rx_packets, tx_packets)

    print



if __name__ == "__main__":
    main()