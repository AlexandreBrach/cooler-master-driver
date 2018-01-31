#!/usr/bin/env python3

# -*- coding: utf-8 -*-
""" Module to manage Cooler Master S FR keyboard
    libusb should be installed on the system
    pyusb too, see more info at https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
"""

import sys
import time
import usb.core
import usb.util

CMMK_USB_VENDOR = 0x2516
#CMMK_USB_PRODUCT = 0x003b
CMMK_USB_INTERFACE = 1


def getKeyboardInfo(dev):
    """ print Cooler Master device informations

    longExplanation

    :param paramName: the usb device
    :type dev: usb.device

    :return: null
    :rtype: null
    """

    bLength = dev.bLength
    bDescriptorType = dev.bDescriptorType
    bcdUSB = dev.bcdUSB
    bDeviceClass = dev.bDeviceClass
    bDeviceSubClass = dev.bDeviceSubClass
    bDeviceProtocol = dev.bDeviceProtocol
    bMaxPacketSize0 = dev.bMaxPacketSize0
    idVendor = dev.idVendor
    idProduct = dev.idProduct
    bcdDevice = dev.bcdDevice
    iManufacturer = dev.iManufacturer
    iProduct = dev.iProduct
    bNumConfigurations = dev.bNumConfigurations
    address = dev.address
    bus = dev.bus
    port_number = dev.port_number
    port_numbers = dev.port_numbers
    speed = dev.speed
    serial = dev.serial_number
    langids = dev.langids
    if len(langids) != 0:
        product = dev.product
    else:
        product = None

    print("bLength :" + str(bLength))
    print("bDescriptorType :" + str(bDescriptorType))
    print(bcdUSB)
    print(bDeviceClass)
    print(bDeviceSubClass)
    print(bDeviceProtocol)
    print("bMaxPacketSize0 : " + str(bMaxPacketSize0))
    print("idVendor : " + str(idVendor))
    print("idProduct : " + str(idProduct))
    print("bcdDevice :" + str(bcdDevice))
    print("iManufacturer : " + str(iManufacturer))
    print("iProduct : " + str(iProduct))
    print("Serial Number: " + str(serial))
    print("bNumConfigurations :" + str(bNumConfigurations))
    print("address : " + str(address))
    print("bus :" + str(bus))
    print("port_number : " + str(port_number))
    print("speed: " + str(speed))
    print("langsid : " + str(langids))
    print(serial)
    print(product)


if __name__ == "__main__":
    coolermaster = usb.core.find(idVendor=CMMK_USB_VENDOR)
    if coolermaster is None:
        raise ValueError('Our device is not connected')

    iface = usb.core.Interface(coolermaster, CMMK_USB_INTERFACE)
    print(iface)
    usb.util.claim_interface(coolermaster, iface)

    configuration = usb.core.Configuration(coolermaster)
    coolermaster.set_configuration()
    endpoints = iface.endpoints()
    if endpoints[0].bEndpointAddress == 4:
        cooler_writer = endpoints[1]
        cooler_reader = endpoints[0]
    else:
        cooler_writer = endpoints[0]
        cooler_reader = endpoints[1]

    PROFILE = 1
    DATA = [0x51, 0x00, 0x00, 0x00, PROFILE]

    cooler_writer.write(DATA)
    usb.util.dispose_resources(coolermaster)
