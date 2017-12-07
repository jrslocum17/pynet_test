#!/usr/bin/env python
"""
Ex 1. Use Paramiko to retrieve the entire 'show version' output from pynet-rtr2.
Ex 2. Use Paramiko to change the 'logging buffered <size>' configuration on pynet-rtr2.
This will require that you enter into configuration mode.
"""
import paramiko
from getpass import getpass
from time import sleep

IP_ADDR = "184.105.247.70"
USERNAME = "pyclass"
PORT = 22
SLEEP_TIMER = 0.5
MAX_BUFFER = 6000

def run_command(remote_conn, command):
    outp = remote_conn.send(command + "\n")
    sleep(SLEEP_TIMER)
    output = ""
    while remote_conn.recv_ready():
        output += remote_conn.recv(MAX_BUFFER)
        sleep(SLEEP_TIMER)
    return output


def main():
    password = getpass()
    remote_conn_pre = paramiko.SSHClient()

    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(IP_ADDR,username=USERNAME, password=password, look_for_keys=False,allow_agent=False,port=PORT)
    remote_conn = remote_conn_pre.invoke_shell()
    remote_conn.settimeout(4.0)

    run_command(remote_conn, "terminal length 0")
    output = run_command(remote_conn, "show version")
    print(output)

    output = run_command(remote_conn, "show run | include logging buffered")
    print("Original Log Buffer Size: " + output)
    run_command(remote_conn, "config term")
    run_command(remote_conn, "logging buffered 65536")
    run_command(remote_conn, "end")
    output = run_command(remote_conn, "show run | include logging buffered")
    print("Modified Log Buffer Size: " + output)

    remote_conn.close()

if __name__ == "__main__":
    main()
