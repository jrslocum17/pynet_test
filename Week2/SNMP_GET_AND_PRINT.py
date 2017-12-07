#!/usr/bin/env python
'''
 Ex 4c. Create a script that connects to both routers (pynet-rtr1 and pynet-rtr2) and prints out both the MIB2 sysName and sysDescr.

 A script that connects to both routers (pynet-rtr1 and pynet-rtr2)
 and prints out both the MIB2 sysName and sysDescr
'''
import json

import yaml

import SNMP_Router

YAML_Router_File = "Pynet_Routers.yml"
JSON_SNMP_OID_File = "SNMP_OIDs.json"

def main():

    with open(YAML_Router_File) as f:
        yaml_router_list = yaml.load(f)

    with open(JSON_SNMP_OID_File) as f:
        json_snmp_oid_list = json.load(f)

    for router in yaml_router_list:
        my_snmp_router = SNMP_Router.SNMP_Router(router)  # pass the dict into the class constructor
        my_router_output = my_snmp_router.Get_Router_Info(json_snmp_oid_list)
        print(router['router'] + ":\n" + my_router_output)

if __name__ == "__main__":
    main()
