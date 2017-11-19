#!/usr/bin/env python

'''
Ansible module to create a VLAN if not present or just change its name.
Will do nothing if VLAN is already present with the same name.
'''

from ansible.module_utils.basic import *
import pyeapi
# from add_remove_vlan import get_vlan, modify_vlan


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
    '''
    Ansible module to create VLAN if not present of just change its name.
    :return:
    '''

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            vlan_num=dict(required=True),
            vlan_name=dict(required=False, default="None"),
            remove=dict(type='bool', required=False, default='false')
        ),
        supports_check_mode=True
    )

    remote_sw = pyeapi.connect_to(module.params['host'])

    vlan_present = vlan_name = get_vlan(remote_sw, module.params['vlan_num'])

    if module.params['remove'] and not vlan_present:
        module.fail_json(msg="Error: VLAN {} is not present in configuration".format(module.params['vlan_num']))
    elif not module.params['remove'] and (vlan_name == module.params['vlan_name']):
        module.exit_json(msg="VLAN {} is already present in configuration and already named {}, no action necessary."
                         .format(module.params['vlan_num'],
                                 module.params['vlan_name'],
                                 str(module.params['remove'])),
                         changed=False)
    else:
        command_results = modify_vlan(remote_sw,
                                      module.params['vlan_num'],
                                      module.params['vlan_name'],
                                      remove=module.params['remove'],
                                      commit=(not module.check_mode))
        if command_results.startswith("Command failure"):
            module.fail_json(msg="VLAN modification failed: {}".format(command_results))
        else:
            module.exit_json(msg="{}VLAN {} with name {} {}."
                             .format("Check mode: " if module.check_mode else "",
                                     module.params['vlan_num'],
                                     vlan_name if module.params['remove'] else module.params['vlan_name'],
                                     "removed" if module.params['remove'] else "configured"),
                             changed=True)


if __name__ == "__main__":
    main()
