#!/usr/bin/env python
# coding=utf-8

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.curdir, '..', '..')))

import traceback
import tempfile

# 3rd party imports
try:
    from flask import Flask
    from flask_cors import CORS, cross_origin
except Exception as e:
    sys.stderr.write("Failed to import some Python modules, use requirements.txt "
                 "to install 3rd party external dependencies: {}".format(e))
    traceback.print_exc()
    sys.exit(1)

# Internal imports
import util.logger as logger

_logger = logger.get_logger(__name__)

try:
    # Create the Flask app and init config
    flask_app = Flask('wifi-arduino-control')

    # Need Cross-origin headers for local development
    CORS(flask_app)

    # Import other Flask sub-modules containing URL handlers
    import webserver.default_routes
    import webserver.rest_api
except:
    _logger.exception("REST API startup failed")
    sys.exit(1)
