#!/usr/bin/env python
"""
Ex 1. Use Arista's eAPI to obtain 'show interfaces' from the switch. Parse the 'show interfaces' output to obtain the
'inOctets' and 'outOctets' fields for each of the interfaces on the switch.  Accomplish this using Arista's pyeapi.

"""
import pyeapi
from pprint import pprint

def main():
    pynet_sw4 = pyeapi.connect_to("pynet-sw4")
    command_result = pynet_sw4.enable('show interfaces')
    show_int_output = command_result[0]['result']
    interface_dict = show_int_output['interfaces']
    #pprint(interface_dict)
    sorted_ints = sorted(interface_dict.keys())
    print("")
    print("{:16}{:16}{:16}".format("Interface", "InOctets", "OutOctets"))
    print("{:-<16}{:-<16}{:-<16}".format("", "", ""))
    for int in sorted_ints:
        # Use .get() instead of a direct reference to have option of specifying a default if key not found
        in_octets = interface_dict[int].get('interfaceCounters', {}).get('inOctets', "")
        out_octets = interface_dict[int].get('interfaceCounters', {}).get('outOctets', "")
        print("{:16}{:<16}{:<16}".format(int, in_octets, out_octets))
    print("")

if __name__ == "__main__":
    main()