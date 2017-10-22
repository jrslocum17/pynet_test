#!/usr/bin/env python

'''
Example program to show multiprocessing with Netmiko

'''

import sys
import warnings
with warnings.catch_warnings(record=True) as w:
    import paramiko

import multiprocessing
import time
from datetime import datetime

import netmiko
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException

from DEVICE_CREDS import all_devices
'''
::Contents of DEVICE_CREDS.py, a file within this directory
pynet1 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.70',
    'username': 'pyclass',
    'password': '88newclass',
    'port': 22
}
pynet2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': '88newclass',
    'port': 22
}
srx = {
    'device_type': 'juniper',
    'ip': '184.105.247.76',
    'username': 'pyclass',
    'password': '88newclass',
    'port': 22
}

all_devices = [
    pynet1,
    pynet2,
    srx
]

a_device is just one of the dicts above, and all_devices is a list of the dicts


'''

def printout(results):

    print "Successful devices:"
    for device_dict in results:
        for key_device_ip_port, value_tuple_bool_string in device_dict.iteritems():
            (successTorF, output_string) = value_tuple_bool_string
            if successTorF:
                print("\n")
                print("Device = " + key_device_ip_port + "\n")
                print(output_string)
                print("\n")

    print "Failed devices:"
    for device_dict in results:
        for key_device_ip_port, value_tuple_bool_string in device_dict.iteritems():
            (successTorF, output_string) = value_tuple_bool_string
            if not successTorF:
                print("\n")
                print("Device = " + key_device_ip_port + "\n")
                print(output_string)
                print("\n")




def worker_show_command(target_device, command, return_data_queue):
    '''
    For a given target device, execute a show command and store the output in a queue as a value in a dictionary,
    with the key being the target device name.
    :param target_device: A dict containing parameters for the device we're running the command against
    :param return_data_queue: A queue containing output and the hostname
    :return:
    '''

    device_ip_port = "{ip}:{port}".format(**target_device)
    return_data = {}
    '''
    return_data is a dict {}
    identifier is a string in the "ip_addr:port" format (this is the key)
    return_data[identifier] stores a value, which is a tuple in the form (True|False, "string output from show cmd")
    True if the attempt worked, with output from the command, and False if attempt failed, with error string 
    return_data = {
        'ip:port': '(True|False),"show cmd output"'
    }
    '''

    SSHClass = netmiko.ssh_dispatcher(target_device['device_type'])

    try:
        device_connection = SSHClass(**target_device)
        show_cmd_output = device_connection.send_command(command)
        return_data[device_ip_port] = (True, show_cmd_output)
    except (NetMikoTimeoutException, NetMikoAuthenticationException) as conn_except:
        return_data[device_ip_port] = (False, conn_except)

    return_data_queue.put(return_data)


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: %s <show_command_in_doublequotes>" % sys.argv[0])
    command = sys.argv[1]

    print "\nStart time: " + str(datetime.now())

# The results from each process will be stored in multiproc_queue
    return_data_queue = multiprocessing.Queue()
    processes = []

    for target_device in all_devices:
        proc = multiprocessing.Process(target=worker_show_command, args=(target_device, command, return_data_queue))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    results = []
    # while it is true that any process in the list of processes is_alive(), pass the while condition
    while not return_data_queue.empty():
        results.append(return_data_queue.get())

#   while not any(word in list_of_words for word in ['AND', 'OR', 'NOT']):
#       print 'No boolean'


    printout(results)

    print "\nEnd time: " + str(datetime.now())

if __name__ == "__main__":
    main()
