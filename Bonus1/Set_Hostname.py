#!/usr/bin/env python
"""
Ex 4. Use the PyEZ load() method to set the hostname of the SRX using set, conf (curly brace), and XML formats.

After each load(), display the differences between the running config and the candidate config. Additionally,
perform at least one commit and one rollback(0) in this program.

The committed hostname at the end of the program should be:  pynet-jnpr-srx1
"""
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from pprint import pprint
from getpass import getpass


from getpass import getpass

USER = 'pyclass'
NEW_NAME = 'pynet-jnpr-srx99'
ORIG_NAME = 'pynet-jnpr-srx1'


def main():
    pwd = getpass()

    a_device = Device(host='184.105.247.76', user = USER, password = pwd)
    a_device.open()

    pprint(a_device.facts)

    cfg = Config(a_device)
    cfg.lock()

    cfg.load("set system host-name {}".format(NEW_NAME), format="set", merge=True)
    print("Config changes after set method:")
    print cfg.diff()
    print("Rolling back...")
    cfg.rollback(0)
    print cfg.diff()
    print

    cfg.load(path="set_hostname.conf", format="text", merge=True)
    print("Config changes after conf method:")
    print cfg.diff()
    print("Rolling back from conf method...")
    cfg.rollback(0)
    print cfg.diff()
    print

    cfg.load(path="set_hostname.xml", format="xml", merge=True)
    print("Config changes after xml method:")
    print(cfg.diff())
    print("Committing after xml method...")
    cfg.commit(comment="Testing hostname change method through XML", confirm=1)
    print(cfg.diff())

    cfg.unlock()


if __name__ == "__main__":
    main()
