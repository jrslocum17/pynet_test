#!/usr/bin/env python

import yaml
import json

from pprint import pprint as pp

with open("list_output.yml") as f:
 yaml_list=yaml.load(f)

with open("list_output.json") as f:
 json_list=json.load(f)

print("YAML List:")
pp(yaml_list)

print("")
print("JSON List:")
pp(json_list)
