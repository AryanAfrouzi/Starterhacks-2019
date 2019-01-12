# Byte-mail backend

import logging
from flask import Flask, jsonify, request
import flask_cors
import requests_toolbelt.adapters.appengine
import calendar
import time

ipList = []

requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
flask_cors.CORS(app)

@app.route('/addip', methods=['POST', 'PUT'])
def recordIp():
    
    global ipList

    senderIP = request.remote_addr

    if senderIP not in ipList:
        ipList.append(senderIP)
        return 'Success', 200 
    else:
        return 'Already Added', 500 


@app.route('/iplist', methods=['GET'])
def getList():
    global ipList
    return ipList


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
