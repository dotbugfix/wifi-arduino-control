#!/usr/bin/env python
# coding=utf-8

import util.logger as logger

log = logger.get_logger(__name__)

class ArduinoDevice():
    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            raise Exception("Arduino Device object not yet created")

        return cls._instance

    @classmethod
    def create_instance(cls, ip_address):
        log.info("Creating a new instance of Arduino Device with IP: %s",
                 ip_address)

        cls._instance = ArduinoDevice(ip_address)

    def __init__(self, ip_address):
        self.ip_address = ip_address

    def __repr__(self):
        return("ArduinoDevice<IP:%s>" % (self.ip_address))

    def toggle_led(self):
        log.info("Toggle LED")
