#!/usr/bin/env python

"""

Ex. 8: Write a Python program using ciscoconfparse that parses this config file (cisco_ipsec.txt).
Note, this config file is not fully valid (i.e. parts of the configuration are missing).
The script should find all of the crypto map entries in the file (lines that begin with 'crypto map CRYPTO') and
for each crypto map entry print out its children.

Parse the Cisco config file and find the crypto map CRYPTO lines, then print the children of
those lines.
"""

from ciscoconfparse import CiscoConfParse

def main():
    """
    Find all the Crypto Map entries in a Cisco Config file (these are the lines that begin
    with 'Crypto map crypto' and print out all the children for each entry
    :return: yo mama
    """
    cisco_config_file = "cisco_ipsec.txt"

    cisco_cfg = CiscoConfParse(cisco_config_file)

    crypto_map = cisco_cfg.find_objects(r"^crypto map CRYPTO")
    for c_map in crypto_map:
        print(c_map.text)
        for child in c_map.children:
            print child.text
    print

if __name__ == "__main__":
    main()

