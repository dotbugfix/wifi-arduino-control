#!/usr/bin/env python
# coding=utf-8

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.curdir, '..', '..')))

from webserver import flask_app
from webclient.device_control import ArduinoDevice
from flask import jsonify, request, json
import util.version as version
import util.logger as logger

log = logger.get_logger(__name__)

HTTP_OK         = 200
HTTP_CREATED    = 201
HTTP_NOT_FOUND  = 404
HTTP_BAD_INPUT  = 400

@flask_app.route("/api/version", methods=['GET'])
def get_version():
    log.debug('Current version = %s' % (version.__pretty_version__))
    return (jsonify({'version': version.__pretty_version__}),
              HTTP_OK,
              {'ContentType':'application/json'})

@flask_app.route("/api/device/data", methods=['POST'])
def post_data_from_device():
    data = json.loads(request.data)

    log.info("Data from device: %s", data)

@flask_app.route("/api/device/blink", methods=['GET'])
def blink_device_led():
    device = ArduinoDevice.get_instance()

    log.info("Toggle the LED on device: %s", device)
    status = device.toggle_led()

    return(jsonify({'success': status}),
          HTTP_OK,
          {'ContentType':'application/json'})
