#!/usr/bin/env python

import telnetlib
import time
import socket
import sys
import getpass

IP_ADDR = "184.105.247.70"
COMMAND = "show ip interface brief"
TELNET_PORT = 23
TELNET_TIMEOUT = 5
DISABLE_PAGING_CMD = "term leng 0"

class ShowCommand(object):
    '''
    Base class for the Cisco IOS "show command" program
    '''

    def __init__(self, ip_addr, username, password, command, port, timeout):
        self.ip_addr = ip_addr
        self.username = username
        self.password = password
        self.my_command = command
        self.port = port
        self.timeout = timeout

    def telnetConnect(self):
        '''
        Create a Telnet connection to a remote device
        :ip_addr: The remote IP address
        :return:
        '''
        try:
            self.my_conn = telnetlib.Telnet(self.ip_addr, self.port, self.timeout)
        except socket.timeout:
            sys.exit("connection timed out")

    def telnetLogin(self):
        '''
        Log into the remote device via Telnet
        '''
        self.output = self.my_conn.read_until("sername", self.timeout)
        self.my_conn.write(self.username + "\n")
        self.output += self.my_conn.read_until("ssword", self.timeout)
        self.my_conn.write(self.password + "\n")

    def sendCommand(self, command = COMMAND):
        '''
        Send command argument to remote device for execution
        '''
        command = command.rstrip()
        self.my_conn.write(command + "\n")
        time.sleep(1)
        self.output = self.my_conn.read_very_eager()

    def disablePaging(self):
        '''
        Disable paging on the remote device
        :return:
        '''
        self.sendCommand(DISABLE_PAGING_CMD)

    def closeConnection(self):
        '''
        Close the Telnet Connection
        :return:
        '''
        self.my_conn.close()

def main():
    username = raw_input("Username: ")
    password = getpass.getpass()
    my_command = ShowCommand(IP_ADDR,username,password,COMMAND,TELNET_PORT,TELNET_TIMEOUT)
    my_command.telnetConnect()
    my_command.telnetLogin()
    my_command.disablePaging()
    print my_command.output
    my_command.sendCommand()
    print my_command.output
    my_command.closeConnection()

if __name__ == "__main__":
    main()