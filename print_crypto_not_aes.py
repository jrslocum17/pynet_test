#!/home/jslocum/VENV/py27_venv/bin/python

from ciscoconfparse import CiscoConfParse
cisco_cfg=CiscoConfParse("cisco_ipsec.txt")
crypto_not_aes=cisco_cfg.find_objects_wo_child(parentspec=r"crypto map CRYPTO", childspec=r"AES")
for i in crypto_not_aes:
 print(i.text)
 for child in i.children:
  print child.text

