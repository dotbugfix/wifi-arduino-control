#!/usr/bin/env python
# coding=utf-8

import os, sys
sys.path.insert(0, os.path.abspath('..'))

# This should be the first import to bootstrap the runtime env
import util.bootstrap

import util.logger as logger
from werkzeug.serving import make_server

_logger = logger.get_logger(__name__)

FLASK_SERVER_PORT = "5000"

def parse_cmd_args():
    import argparse
    import util.version as version

    parser = argparse.ArgumentParser()
    pretty_version = version.__pretty_version__
    parser.add_argument("--version", "-v", action = 'version', version = pretty_version)
    args = parser.parse_args()

    _logger.debug("CLI args: %s", args)
    return args

def start_flask_server():
    # See webserver/__init__.py for the Flask app bootstrap
    import webserver
    flask_app = webserver.flask_app
    
    flask_server = make_server("0.0.0.0", FLASK_SERVER_PORT, flask_app)
    flask_server.serve_forever()

def main():
    ''' Main entry point for WittyMail
        - Start the REST API server
        - Open a browser window with the GUI
    '''
    try:
        args = parse_cmd_args()
        _logger.info("Open the following URL in a browser: http://localhost:%s", FLASK_SERVER_PORT)

        # This call will block forever
        start_flask_server()
        
    except Exception:
        _logger.exception("Failed to start the webserver")
        sys.exit(1)
      
if __name__ == "__main__":
    main()