#!/usr/bin/env python

# Transfer this file to /home/jslocum/DJANGOX/djproject/ and execute there

from netmiko import ConnectHandler
from datetime import datetime

from net_system.models import NetworkDevice, Credentials
import django

from multiprocessing import Process, current_process
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



def main():
    django.setup()

    devices = NetworkDevice.objects.all()

    procs = []
    start_time = datetime.now()
    for a_device in devices:
        my_proc = Process(target=show_command, args=(a_device, "show version",))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
        print(a_proc)
        a_proc.join()

    print("\nElapsed Time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()