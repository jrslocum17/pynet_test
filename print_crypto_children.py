#!/home/jslocum/VENV/py27_venv/bin/python

from ciscoconfparse import CiscoConfParse
cisco_cfg = CiscoConfParse("cisco_ipsec.txt")
crypto_map = cisco_cfg.find_objects(r"^crypto map CRYPTO")
for i in crypto_map:
 print(i.text)
 for child in i.children:
  print child.text

