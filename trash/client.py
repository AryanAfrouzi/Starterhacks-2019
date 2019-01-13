import socket
import threading
import requests
import random
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

prdata = []
inbox = []

privkey = RSA.import_key(b'-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFJTBPBgkqhkiG9w0BBQ0wQjAhBgkrBgEEAdpHBAswFAQIWbvhb8nXlscCAkAA\nAgEIAgEBMB0GCWCGSAFlAwQBAgQQZ+4L/0kCBNzP02kImuF5sgSCBNDW3cH8ySlO\nykFht+J5jj8mmYDnUZ9uus+ioJ8V0R7H8q3YGAtxtUqM1DQZcoQVZsoXhCgDcnRV\nHB7gu7VCaV+P7/r5JQ8tUmnmcJyCCKQxAeyGDQuRVtiNJRfWyKa2kx9B31KwaIcd\nQ+ws/faiM/YX1IiaKraCUy+8eR5j3yKYHM20XL4ZXGOEYRhND8IOB/52IOfbDDEC\nAh5YgcbiiMjauKvrR+EsL9vnZSAEv2edWnQPGDBo569JAOmJIikLVwgYhByGGizj\nXJEOYK6BMvyq1v0nhH12J15keSLo68lidP6aCESAFZ25wRUWvndB7Yfu7sojIpGx\n5Auktlo3rbsqjWtzLpMGBPsdxEA6s6Ud25bSBY0ghel/bV+f5PVxGhxi6nBxNYLi\nllhMO708GKjijoG/Pn53LNZqAV4rLI2BfMdwZSD3eWEVr023U0qjmBNE6Jn2Ls3k\nvkgPws+9H3nvpHXXsZzL1A2eu6mv6Qi0KHX/O7hW2Zd39/rQCc6Mz6Dn5CTocGIO\ns3Cg1EktVbpy5DADhG2mf4dLUzVmPjnGLG2SPn9Dv168QUj8RcDuudYB1wbINcS4\nWTHmUIqSvlE5cLkDWiRyw8jjwHVeBEUvxGhqNdBbJAi1nUYW9MVEKNAid80+36Ht\n2I5W7h/r4P8oYry8v2emqGiTQXamEQzNC0WVKm5f0lDrA3l/TR8hkWB+LnBEVZ32\nKgBMw+TTgMRxfedHWX63D94G9vnLypBFVNespdHWE+3OxWoydhEPPvMYCiyXC7cW\nWGP3T6+6CLVWOx5/k1ScMlW2wnLN+uIT13PbcU38KrCC6WY7KIoCrifhTlprAAld\nBMdlb5lXiJr3axLiZh9LDh3Zzy0jS0aiPyv/Grs+qIvK50bYop2//BmZFt10W5Lk\nLrVt1+KPhy9+DEm4LQtf0ZO51a3mMt3XW9HxGjBIiMelkqznL2OtfYJERUoDtSBD\n+JH8LLLywPvgf4D9qWwr/xtTYMElcSvy+8RmKxGOJC92tbe6dDNgfFQEyQAtKY9Z\nPfWA4/zdaTQyOWLk2LYjaNRA2dwJmgGr07Eh8gcO333DDkVXt1/aAlgPA2pCjB+Y\nffYNq2u1ha60blVZazcV6bsbHM6lu7j4D2Y30H/d/iDsRM2ZDguWigHIrxsMK1di\nkm9CwOW22Dq4b1SSoC7HOdTvJUoEL35HSFuIHdPp6LJ4aFnYo0HjNF36eIDZcFN8\nT19vCRMpl8unzy8JwgjKHxXNKGmbW/RmGvllbUH4nd1osMxgpBOI41UDYMsy3SDx\nETsKGvc5V2GMNXvQXNIN8mkWoSa7WsfwoUQEQBPBUtfHDeHafXXAj2oLiCPWE72D\n0qvGSm54A5hvDV5fXOisXIQvvP5fG59B9BQ9WCMMuGgLm4u9Jz/+QPXseAiZjHad\ninr5qLpQveOBl6tqmX7MS6DC+pJt4o7DeEkZrWnk/NYoM9ibURsBTBjcd6TMs85B\n+/QP295bUmwgiE6I93WD1GMSM23a8hL0WktQsQCHEIOTOl67OyJiJNDZQrWTjpxS\nRb/fF/grO9Uo2gfPoVAXALmgaHV4ZQvOvtKGfO2NPE0aZBuj24A4mrvVICz2ySys\nGsYQeeOuNZmxQrp6IIq9TNE5gUkGjm627w==\n-----END ENCRYPTED PRIVATE KEY-----', passphrase='test')
pubkey = privkey.publickey()

def encrypt(key, message):
    encryptor = PKCS1_OAEP.new(key)
    return base64.b64encode( encryptor.encrypt( message.encode() ) )

def decrypt(key, ct):
    decryptor = PKCS1_OAEP.new(key)
    return decryptor.decrypt( base64.b64decode( ct ) ).decode()

def send(data, address):
    s = socket.socket()
    s.settimeout(5)
    s.connect((address, 11219))
    s.send(data)

def sendMessage(message, bmailt):
    global privkey, pubkey
    bmaily = pubkey.exportKey().decode()
    print(bmailt)
    bmailt2 = RSA.importKey(bmailt.replace('\r', ''))
    data = encrypt(bmailt2, (encrypt(privkey, message).decode()+'||'+bmaily)).decode()
    data += '||'+bmailt

    unSampledIPlist = requests.get('https://byte-mail-backend.appspot.com/iplist').text.split(', ')

    if len(unSampledIPlist) > 6:
        ipList = random.sample(unSampledIPlist, 6)+"127.0.0.1"
    else:
        ipList = unSampledIPlist[:]
    
    for each in ipList:
        unSampledIPlist.remove(each)

    for ip in ipList:
        if ip != '':
            print('sending to '+str(ip))
            try:
                send(data, ip)
            except:
                print('failed')
                try:
                    rand = random.sample(unSampledIPlist, 1)
                    unSampledIPlist.remove(rand)
                    ipList.append(rand)
                except:
                    pass
    print('Done forwarding.')

def decryptMessage(ct, privkey, bmaily):
    inner, bmailp = message.split('||')
    bmailp = RSA.import_key(bmailp)
    if bmailp !=  bmaily:
        return 0
    else:
        me, bmailt = decrypt(privkey, inner).split('||')
        bmailt = RSA.import_key(bmailp)
        message = decrypt(bmailt, me)
        return message, bmailt.exportKey()

def forwardThread():
    global prdata, inbox
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 11219))
    s.listen(5)
    while True:
        client, address = s.accept()
        print("Connection established with "+str(address))
        data = client.recv(1024)
        if data not in prdata:
            print("Data received..")
            msg = 0
            try:
                msg, bmail = decryptMessage(data, privkey, pubkey)
            except:
                pass

            if msg != 0:
                inbox += [msg, bmail]
            else:
                unSampledIPlist = requests.get('https://byte-mail-backend.appspot.com/iplist').text.split(', ')

                try:
                    unSampledIPlist.remove(address[0])
                except:
                    pass

                if len(unSampledIPlist) > 6:
                    ipList = random.sample(unSampledIPlist, 6)+"127.0.0.1"
                else:
                    ipList = unSampledIPlist[:]
                
                for each in ipList:
                    unSampledIPlist.remove(each)

                for ip in ipList:
                    if ip != '':
                        print('sending to '+str(ip))
                        try:
                            send(data, ip)
                        except:
                            print('failed')
                            try:
                                rand = random.sample(unSampledIPlist, 1)
                                unSampledIPlist.remove(rand)
                                ipList.append(rand)
                            except:
                                pass
                print('Done forwarding.')

def keepRegistered():
    global prdata
    while True:
        requests.post('https://byte-mail-backend.appspot.com/addip')
        time.sleep(270)
        prdata = []

t1 = threading.Thread(target=forwardThread)
t1.start()

t2 = threading.Thread(target=keepRegistered)
t2.start()

print("Forwarding thread initiated..")
print("Registration thread initiated..")

while True:
    print(inbox)
    inp = str(input())
    if 'send' in inp:
        sendMessage(inp.split('send ')[1].split(' ')[0], inp.split('send ')[1].split('||')[1])
