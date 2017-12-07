#!/usr/bin/env python
"""
Ex 8. Use processes and Netmiko to execute 'show version' on each device in the database.
Use a queue to get the output data back from the child processes.
Print this output data to the screen in the main process.
Calculate the amount of time required to do this.
"""
# Transfer this file to /home/jslocum/DJANGOX/djproject/ and execute there

from netmiko import ConnectHandler
from datetime import datetime

from net_system.models import NetworkDevice, Credentials
import django

from multiprocessing import Process, current_process, Queue
import time


def show_command(a_device, command, my_queue):
    my_dict = {}
    creds = a_device.credentials
    remote_conn = ConnectHandler(device_type=a_device.device_type, ip=a_device.ip_address,
                                 username=creds.username, password=creds.password,
                                 port=a_device.port, secret='')
    output = "#" * 80
    output += "\n" + remote_conn.send_command(command)
    output += "\n" + ("#" * 80) + "\n"

    my_dict[a_device.device_name] = output
    my_queue.put(my_dict)


def main():
    django.setup()

    devices = NetworkDevice.objects.all()
    my_queue = Queue(maxsize=15)
    procs = []
    start_time = datetime.now()
    for a_device in devices:
        my_proc = Process(target=show_command, args=(a_device, "show version", my_queue))
        my_proc.start()
        procs.append(my_proc)

    for a_proc in procs:
        print(a_proc)
        a_proc.join()

    while not my_queue.empty():
        my_dict = my_queue.get()
        for device_name, cmd_output in my_dict.iteritems():
            print "\n" + device_name
            print cmd_output

    print("\nElapsed Time: " + str(datetime.now() - start_time))


if __name__ == "__main__":
    main()