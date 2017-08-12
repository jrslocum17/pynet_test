#!/usr/bin/env python
"""
Creates a list. One of the elements of the list is a dictionary with two keys. This list
is written to a YAML file and a JSON file
"""
import yaml
import json

from pprint import pprint

def output_format(my_list, my_str):
    '''
    Make the output format easier to read
    :param my_list: a list of the items to print
    :param my_str: the name of the list
    :return:
    '''
    print "\n\n"
    print "#" * 3
    print "#" * 3 + my_str
    print "#" * 3
    pprint(my_list)

def main():
    '''
    Read YAML and JSON files, pretty print to standard out
    :return:
    '''
    yaml_file = "list_output.yml"
    json_file = "list_output.json"

    with open(yaml_file) as f:
        yaml_list=yaml.load(f)

    with open(json_file) as f:
        json_list=json.load(f)

    output_format(yaml_list, " YAML")
    output_format(json_list, " JSON")
    print "\n"

if __name__ == "__main__":
    main()
