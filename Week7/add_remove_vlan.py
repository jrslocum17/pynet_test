#!/usr/bin/env python
"""
Ex 2. Using Arista's pyeapi, create a script that allows you to add a VLAN (both the VLAN ID and the VLAN name).
Your script should first check that the VLAN ID is available and only add the VLAN if it doesn't already exist.
Use VLAN IDs between 100 and 999.  You should be able to call the script from the command line as follows:

   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

If you call the script with the --remove option, the VLAN will be removed.

   python eapi_vlan.py --remove 100          # remove VLAN100

Once again only remove the VLAN if it exists on the switch.  You will probably want to use Python's argparse to
accomplish the argument processing.

In the lab environment, if you want to directly execute your script, then you will need to use '#!/usr/bin/env python'
at the top of the script (instead of '!#/usr/bin/python').

"""
import argparse
import pyeapi
from pprint import pprint

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Enter the name of the VLAN")
    parser.add_argument("--remove", help="Remove a specified VLAN", action="store_true")
    parser.add_argument("vlan_number", help="Enter the VLAN number")
    args = parser.parse_args()
    return {'vlan': args.vlan_number, 'name': args.name, 'remove': args.remove}


def get_vlan(net_conn, vlan_num):
    '''
    Check for the existence of a VLAN, return the name if found
    :param net_conn: The pyeapi connection object for the switch to be checked
    :param vlan_num: The VLAN to be checked against all configured VLANs
    :return: VLAN name if the VLAN was found, empty string otherwise
    '''
    command_result = net_conn.enable("show vlan")
    vlan_dict = command_result[0]['result']['vlans']
    #pprint(vlan_dict)
    if vlan_num in vlan_dict.keys():
        return vlan_dict[vlan_num]['name']
    else:
        return ""


def modify_vlan(net_conn, vlan_num, vlan_name, remove=False, commit=True):
    '''
    Add a VLAN with name, or remove a VLAN
    :param net_conn: The pyeapi connection object for the switch to be modified.
    :param vlan_num: The VLAN number to be added.
    :param vlan_name: The name of the VLAN
    :param remove: True if the VLAN is to be removed, False otherwise
    :return:
    '''

    if not commit:
        return "VLAN configuration simulated."

    if remove:
        cfg_cmds = ["no vlan {}".format(vlan_num)]
    else:
        cfg_cmds = ["vlan {}".format(vlan_num), "name {}".format(vlan_name)]

    command_results = net_conn.config(cfg_cmds)

    for result_dict in command_results:  # Look for non-empty dictionaries returned as results
        if result_dict:  # If there is a non-empty dict, it contains an error
            return "Command failure: configuration attempt unsuccessful"

    return "VLAN " + ("removal" if remove else "configuration") + " successful."


def main():
    args_dict = get_args()
    pynet_sw4 = pyeapi.connect_to("pynet-sw4")

    vlan_present = vlan_name = get_vlan(pynet_sw4, args_dict['vlan'])

    if args_dict['remove'] and not vlan_present:
        print("Error: VLAN %s is not present in configuration" % args_dict['vlan'])
        exit(2)
    elif (vlan_name == args_dict['name']):
        print("VLAN %s is already present in configuration and already named %s, no action necessary."
              % (args_dict['vlan'], args_dict['name']))
        exit(1)
    else:
        command_results = modify_vlan(pynet_sw4,
                                      vlan_num=args_dict['vlan'],
                                      vlan_name=args_dict['name'],
                                      remove=args_dict['remove'])

    print(command_results)


if __name__ == "__main__":
    main()
