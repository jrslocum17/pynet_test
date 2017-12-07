#!/usr/bin/env python
"""
Ex 3. Use Pexpect to retrieve the output of 'show ip int brief' from pynet-rtr2.
Ex 4. Use PExpect to change the logging buffer size (logging buffered <size>) on pynet-rtr2.
Verify this change by examining the output of 'show run'.
"""

import pexpect
from getpass import getpass
import sys
import re

IP_ADDR = "184.105.247.71"
USERNAME = "pyclass"
PORT = 22


def run_command(ssh_conn, command, match):
    try:
        ssh_conn.sendline(command)
        ssh_conn.expect(match)
    except pexpect.TIMEOUT:
        print("Timed out waiting for response %s to command %s" % (match, command))
        return ""
    return ssh_conn.before, ssh_conn.after

def main():
    password = getpass()
    ssh_conn = pexpect.spawn('ssh -l {} {} -p {}'.format(USERNAME, IP_ADDR, PORT))
    #ssh_conn.logfile = sys.stdout
    ssh_conn.timeout = 3
    ssh_conn.expect('ssword:')
    ssh_conn.sendline(password)
    ssh_conn.expect('#')

    output_before, output_after = run_command(ssh_conn, "show ip int brief", "#")
    print("IP Address Table: " + output_before)

    pattern = re.compile(r'logging buffered ([1-9][0-9]*)')
    output_before, output_after = run_command(ssh_conn, "show run | include logging buffered", pattern)
    print("Previous Log Buffer Size: " + output_after)

    run_command(ssh_conn, "config term", "\)#")
    run_command(ssh_conn, "logging buffered 51200", "\)#")
    run_command(ssh_conn, "end", "#")

    output_before, output_after = run_command(ssh_conn, "show run | include logging buffered", pattern)
    print("New Log Buffer Size: " + output_after)
    ssh_conn.close()


if __name__ == "__main__":
    main()