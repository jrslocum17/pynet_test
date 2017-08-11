#!/home/jslocum/VENV/py27_venv/bin/python


import yaml
import json
from pprint import pprint as pp

some_list = range(4)
some_list.append("hello")
some_list.append("goodbye")
some_list.append({})
some_list[-1]['mammal'] = "bear"
some_list[-1]['amphibian'] = "frog"

pp(some_list)

with open("list_output.json", "w") as f:
    json.dump(some_list,f)

with open("list_output.yml", "w") as f:
    f.write(yaml.dump(some_list,default_flow_style=False))
