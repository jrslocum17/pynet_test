#!/usr/bin/env python

# Transfer this file to /home/jslocum/DJANGOX/djproject/ and execute there

from netmiko import ConnectHandler
from datetime import datetime

from net_system.models import NetworkDevice, Credentials
import django

import threading
import time


def show_command(a_device, command):
    creds = a_device.credentials
    remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address,
                                 username=creds.username, password=creds.password,
                                 port=a_device.port, secret='')
    print "\n" + ("#" * 80)
    print "\n" + a_device.device_name + ":\n"
    print "\n" + remote_conn.send_command(command)
    print "\n" + ("#" * 80) + "\n"
    remote_conn.disconnect()


def main():
    django.setup()

    devices = NetworkDevice.objects.all()

    start_time = datetime.now()
    for a_device in devices:
        my_thread = threading.Thread(target=show_command, args=(a_device, "show version"))
        my_thread.start()

    main_thread = threading.currentThread()
    for a_thread in threading.enumerate():
        if a_thread != main_thread:
            print(a_thread)
            a_thread.join()

    print("\nElapsed Time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()