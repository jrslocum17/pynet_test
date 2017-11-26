#!/usr/bin/env python

# Transfer this file to /home/jslocum/DJANGOX/djproject/ and execute there

from net_system.models import NetworkDevice, Credentials
import django


def main():
    django.setup()

    net_devices = NetworkDevice.objects.all()
    for a_device in net_devices:
        if "pynet-sw" in a_device.device_name:
            a_device.vendor = "Arista"
        elif "juniper" in a_device.device_name:
            a_device.vendor = "Juniper"
        else:
            a_device.vendor = "Cisco"
        a_device.save()

    for a_device in net_devices:
        print a_device, a_device.vendor


if __name__ == "__main__":
    main()


