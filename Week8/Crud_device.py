#!/usr/bin/env python

# Transfer this file to /home/jslocum/DJANGOX/djproject/ and execute there

from net_system.models import NetworkDevice, Credentials
import django
from time import sleep

def create_device(device_name, device_type, ip_addr, port, credentials):
    new_device = NetworkDevice.objects.get_or_create(
        device_name=device_name,
        device_type=device_type,
        ip_address=ip_addr,
        port=port,
        credentials=credentials
    )
    return new_device


def get_device(device_name):
    try:
        my_device = NetworkDevice.objects.get(device_name=device_name)
        return my_device
    except NetworkDevice.DoesNotExist:
        return None


def get_creds():
    creds = Credentials.objects.all()

    std_creds = creds[0]
    arista_creds = creds[1]

    return (std_creds, arista_creds)

def main():
    django.setup()

    std_creds, arista_creds = get_creds()

    net_devices = NetworkDevice.objects.all()
    print("\nAll devices:")
    for a_device in net_devices:
        print a_device, a_device.device_type, a_device.credentials
    print

    print("Adding two devices...")

    pynet_rtrX = NetworkDevice(
        device_name='pynet-rtrX',
        device_type="cisco_ios",
        ip_address='10.1.2.3',
        port=22,
        credentials=std_creds
    )
    pynet_rtrX.save()

    pynet_sw10 = create_device(
        device_name='pynet-sw10',
        device_type='Arista_EOS',
        ip_addr="172.16.1.5",
        port=8022,
        credentials=arista_creds
    )
    print pynet_sw10

    net_devices = NetworkDevice.objects.all()
    print("\nAll devices:")
    for a_device in net_devices:
        print a_device, a_device.device_type, a_device.credentials
    print

    print("Removing two devices...")
    rem_devices = ['pynet-sw10', 'pynet-rtrX']
    for my_dev in rem_devices:
        remove_dev = get_device(my_dev)
        if remove_dev:
            remove_dev.delete()

    #sleep(10)
    print("\nAll devices:")
    net_devices = NetworkDevice.objects.all()
    for a_device in net_devices:
        print a_device, a_device.device_type, a_device.credentials
    print


if __name__ == "__main__":
    main()
