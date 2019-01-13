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

def getlist():
    global ipList
    tipList = ipList[:]
    for user in tipList:
        if time.time()-user[1] >= 300:
            ipList.remove(user)
    return ipList

@app.route('/addip', methods=['POST', 'PUT'])
def recordIp():
    
    global ipList

    senderIP = request.remote_addr

    if senderIP not in [x[0] for x in ipList]:
        ipList.append([senderIP, time.time()])
        return 'Success', 200 
    else:
        return 'Already Added', 500 


@app.route('/iplist', methods=['GET'])
def getList():
    return ", ".join([x[0] for x in getlist()])


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
