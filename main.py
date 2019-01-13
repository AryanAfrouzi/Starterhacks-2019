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

    ips = [x[0] for x in ipList]
    try:
        indx = ips.index(senderIP)
    except:
        indx = -1

    if indx == -1:
        ipList.append([senderIP, time.time()])
        return 'Success', 200 
    else:
        ipList[indx] = [senderIP, time.time()]
        return 'Updated Record', 200 


@app.route('/iplist', methods=['GET'])
def getList():
    ippList = [x[0] for x in getlist()]
    ippList.remove(request.remote_addr)
    return ", ".join(ippList)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
