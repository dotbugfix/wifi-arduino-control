#!/usr/bin/env python
# coding=utf-8

import requests
import util.logger as logger

log = logger.get_logger(__name__)

class ArduinoDevice():
    '''
    Represents actions that can be performed on the device
    '''

    # Singleton instance
    _instance = None

    @classmethod
    def get_instance(cls):
        '''
        Get the current singleton instance, otherwise raise an exception
        '''
        if not cls._instance:
            raise Exception("Arduino Device object not yet created")

        return cls._instance

    @classmethod
    def create_instance(cls, ip_address):
        '''
        Create a new instance of ArduinoDevice with the specified IP

        :param ip_address: IP address of the device
        '''
        log.info("Creating a new instance of Arduino Device with IP: %s",
                 ip_address)

        cls._instance = ArduinoDevice(ip_address)

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def __repr__(self):
        return("ArduinoDevice<IP:%s>" % (self.ip_address))

    def toggle_led(self):
        '''
        Call an HTTP POST API on the device to toggle its LED

        :return: True if the device reports that the LED was toggled, false otherwise
        '''
        url = 'http://%s/api/device/led/toggle' % (self.ip_address)
        log.info("Making a HTTP GET request on %s", url)
        response = requests.get(url)
        if not response:
            log.error("API call failed on device: %s", response)
            return False
        
        log.info("Response: %s", response.content)
        return True
