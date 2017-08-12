#!/usr/bin/env python
"""
Reads a Cisco config file for crypto maps that are NOT using AES encryption
"""

import re
from ciscoconfparse import CiscoConfParse

def main():
    cisco_cfg_file = "cisco_ipsec.txt"
    cisco_cfg = CiscoConfParse(cisco_cfg_file)

    crypto_not_aes = cisco_cfg.find_objects_wo_child(parentspec=r"crypto map CRYPTO",
                                                 childspec=r"AES")

    print("Crypto Maps not using AES:")
    for c_map in crypto_not_aes:
        #print("   {0}").format(c_map.text)
        for child in c_map.children:
            #print ("   {0}").format(child.text)
            if "transform" in child.text:
                match = re.search(r"set transform-set (.*)$", child.text)
                encryption = match.group(1)
                print("   {0} >>> {1}".format(c_map.text.strip(), encryption))
    print

if __name__ == "__main__":
    main()
