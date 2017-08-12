#!/usr/bin/env python

"""
Write a python program that creates a list. One of the elements of the list
should be a dictionary with at least two keys. Write this list out to a file
using both YAML and JSON formats. The YAML file should be in the expanded form.
"""

import yaml
import json



from pprint import pprint


def main():

    yaml_file = "list_output.yaml"
    json_file = "list_output.json"

    my_dict = {
        'ip_addr': '10.234.120.1',
        'platform': 'Cisco_IOS',
        'vendor': 'cisco',
        'model': '2911'
    }

    some_list = [
        'some_string',
        99,
        18,
        my_dict,
        'another string',
        'last string'
    ]
    some_list.append(range(4))
    some_list[-4]['mammal'] = "bear"
    some_list[-4]['amphibian'] = "frog"

    pprint(some_list)

    with open("list_output.json", "w") as f:
        json.dump(some_list,f)

    with open("list_output.yml", "w") as f:
        f.write(yaml.dump(some_list,default_flow_style=False))

if __name__ == "__main__":
    main()
