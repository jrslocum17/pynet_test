#!/usr/bin/env python

# Transfer this file to /home/jslocum/DJANGOX/djproject/ and execute there

from netmiko import ConnectHandler
from datetime import datetime

from net_system.models import NetworkDevice, Credentials
import django


def show_command(a_device, command):
    creds = a_device.credentials
    remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address,
                                 username=creds.username, password=creds.password,
                                 port=a_device.port, secret='')
    returnStr = "\n" + ("#" * 80)
    returnStr += "\n" + a_device.device_name + ":\n"
    returnStr += "\n" + remote_conn.send_command(command)
    returnStr += "\n" + ("#" * 80) + "\n"
    return returnStr


def main():
    django.setup()

    devices = NetworkDevice.objects.all()

    start_time = datetime.now()
    for a_device in devices:
        print(show_command(a_device, "show version"))

    print("\nElapsed Time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()
