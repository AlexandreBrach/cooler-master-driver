#!/usr/bin/python3

import sys
import time
import array
import usb.core
import usb.util

#CMMK_USB_PRODUCT = 0x003b

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


class CoolerMaster:

    CMMK_USB_VENDOR = 0x2516
    CMMK_USB_INTERFACE = 1

    ACTIVE_PROFILE = 0x00

    def __init__(self):
        self.usb_device = usb.core.find(idVendor=self.CMMK_USB_VENDOR)
        if self.usb_device is None:
            raise ValueError('CoolerMaster is not connected')

        self.iface = usb.core.Interface(self.usb_device, self.CMMK_USB_INTERFACE)
        self.kernel_detach()
        # self.usb_device.set_configuration()

    def kernel_detach(self):
        '''
        don't know if it may be usefull ...
        '''
        if self.usb_device.is_kernel_driver_active(1):
            try:
                self.usb_device.detach_kernel_driver(1)
            except usb.core.USBError as e:
                sys.exit("Could not detach kernel driver: ")



    def claim_interface(self):
        usb.util.claim_interface(self.usb_device, self.iface)
        # self.configuration = usb.core.Configuration(self.usb_device)
        self.configuration = self.usb_device.get_active_configuration()
        self.endpoints = self.iface.endpoints()
        if self.endpoints[0].bEndpointAddress != 4:
            self.writer = self.endpoints[1]
            self.reader = self.endpoints[0]
        else:
            self.writer = self.endpoints[0]
            self.reader = self.endpoints[1]

    def print_interface(self):
        print(self.iface)

    def read(self, data):
        r = self.writer.read(data)
        print(data)
        return r

    def get( self, prop ):
        buff = array.array('B',[0x52,prop,0x00,0x00,0x00 ])
        return self.read(buff)

    def write(self, data):
        self.writer.write(data)

    def start(self):
        self.write([0x01,0x02])

    def get_firmware_version(self):
        buff = array.array('B',[0x05,0x00,0x00,0x00])
        return self.read(buff)


    def set_firmware_control(self):
        self.write([0x41,0x00])

    def set_effect_control(self):
        self.write([0x41,0x01])

    def set_manual_control(self):
        self.write([0x41,0x02])

    def set_profile_control(self):
        self.write([0x41,0x03])



    def set( self, prop, value ):
        self.read([0x51] + prop + value)

    def set_active_profile(self,n):
        self.write([0x51,0x00,0x00,n])


    def dispose(self):
        usb.util.dispose_resources(self.usb_device)


if __name__ == "__main__":

    c = CoolerMaster()
    c.claim_interface()

    c.start()
    # c.set_firmware_control()
    c.set_active_profile(0x02)
    print( c.get_firmware_version() )
    # value = c.get(c.ACTIVE_PROFILE)
    # print( value )
    c.dispose()

