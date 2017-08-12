#!/usr/bin/env python
"""
Use CiscoConfParse library to find the crypto maps that are using pfs group 2
"""

from ciscoconfparse import CiscoConfParse

def main():
    cisco_cfg_file = "cisco_ipsec.txt"

    cisco_cfg = CiscoConfParse(cisco_cfg_file)

    crypto_pfs2_maps = cisco_cfg.find_objects_w_child(parentspec=r"crypto map CRYPTO",
                                                 childspec=r"set pfs group2")
    print("\nCrypto Maps using Perfect Forwarding Secrecy Group 2:")
    for c_map in crypto_pfs2_maps:
        print "  {0}".format(c_map.text)
        #print(c_map.text)
        for child in c_map.children:
            print "   {0}".format(child.text)


if __name__ == "__main__":
    main()

