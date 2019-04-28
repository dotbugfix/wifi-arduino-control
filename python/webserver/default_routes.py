#!/usr/bin/env python
# coding=utf-8

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.curdir)))

from webserver import flask_app

from flask import send_file, send_from_directory

import util.logger as logger

_logger = logger.get_logger(__name__)

base_path = logger.WORKING_DIR

@flask_app.route("/")
def index():
    '''
    Serve the 'index.html' page by default
    '''
    return send_file(os.path.join(base_path, "static" , "index.html"))

@flask_app.route('/<path:path>')
def route_static_files(path):
    '''
    Serve all other supporting files (*.js, *.css etc.)
    '''
    return send_from_directory(os.path.join(base_path, "static"), path)
