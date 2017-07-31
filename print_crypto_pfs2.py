#!/home/jslocum/VENV/py27_venv/bin/python

from ciscoconfparse import CiscoConfParse
cisco_cfg=CiscoConfParse("cisco_ipsec.txt")
crypto_pfs2=cisco_cfg.find_objects_w_child(parentspec=r"crypto map CRYPTO", childspec=r"set pfs group2")
for i in crypto_pfs2:
 print(i.text)
 for child in i.children:
  print child.text

