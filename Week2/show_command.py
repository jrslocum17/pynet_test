#!/usr/bin/env python

"""
Ex 2. telnetlib

    a. Write a script that connects using telnet to the pynet-rtr1 router. Execute the 'show ip int brief' command on the router and return the output.

Try to do this on your own (i.e. do not copy what I did previously). You should be able to do this by using the following items:

telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
remote_conn.read_until(<string_pattern>, TELNET_TIMEOUT)
remote_conn.read_very_eager()
remote_conn.write(<command> + '\n')
remote_conn.close()

"""
import telnetlib
import time
import socket
import sys
import getpass


MY_COMMAND = "show ip interface brief"
IP_ADDR = "184.105.247.70"
TELNET_PORT = 23
TELNET_TIMEOUT = 5

def telnet_conn(ip_addr):
    '''
    Connect to a device via Telnet
    :param ip_addr: The IP address of the target device
    :return: The connected object
    '''
    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        sys.exit("connection timed out")

def telnet_login(conn, username, password):
    '''
    Log into a device with the supplied username and password
    :param conn: The connection object
    :param USERNAME: The username for the device
    :param PASSWORD: The password that goes with the username
    :return: The text output from the login process
    '''
    output = conn.read_until("sername", TELNET_TIMEOUT)
    conn.write(username + "\n")
    output += conn.read_until("ssword", TELNET_TIMEOUT)
    conn.write(password + "\n")
    return output

def run_command(conn, command):
    '''
    Send a command to the remote device
    :return: The text output from the command
    '''
    command = command.rstrip()
    conn.write(command + "\n")
    time.sleep(1)
    output = conn.read_very_eager()
    return output

def main():
    my_conn = telnet_conn(IP_ADDR)
    username = raw_input("Username: ")
    password = getpass.getpass()
    output = telnet_login(my_conn,username,password)
    output += run_command(my_conn, "term leng 0")
    output += run_command(my_conn,MY_COMMAND)
    my_conn.close()
    print output

if __name__ == "__main__":
    main()