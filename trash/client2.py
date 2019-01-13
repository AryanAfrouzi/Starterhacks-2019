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

privkey = RSA.import_key(b'-----BEGIN ENCRYPTED PRIVATE KEY-----\nMIIFJTBPBgkqhkiG9w0BBQ0wQjAhBgkrBgEEAdpHBAswFAQIP0QYarjAi/MCAkAA\nAgEIAgEBMB0GCWCGSAFlAwQBAgQQyc1x/JAkrsDDG4t1NHnRYwSCBNC8naPb7HIB\nARLukUyQyetpetxdP98fEZdvH9D/soOFE5aCQuUYS/sBkqJ92Nn0nKVDW+F0NrFG\nH3cyHA/XCZYinJhC2oTKpziEhMmrXYOKFpecKx4/05oOTTDhuxhwwRfXCaYNn/gp\nG92XSUebyNLJyduqnl510P5F/8AEOBbDs/onrQGDEW0LB5lKCVYPb2gsb9HkXXI4\ndBQ8hgVnQmY1kXRr9ZCAeTzRhuMhPL+7V1bBrwkPAsbtwzNYygTRefS5JeeMVfQF\nRmv/nBH77YirDZr4yX0pfHfg9ZV17j6Uvmrei3eeLfV9dpIXKSYgJVJCz88v7kQB\nbYiyYWmZA7kKaArdGW1vR2oJVOpeDzWjo3FZzXOEpNOsp/Fk3Ck61liGWdFsZ2J9\nx3W4dTMtqDvECx8F9r2qX5MslpaH/e6XoRo0BGfWAvby1xT06OaikFB94CTaHv2j\nVXme9bRt/gkW3CONbEdXtTDjRli4Rq1ACpNmmBOnx0Bf+rrbmAlmsF6bv4X0FxXm\n+U+NdGPiiBmlj8v6SvnLJa0XXYNW7HZZ8fG9E6H2XvKJaEd9PHs89WU26tbBN6lF\nbOeN4n53+7UVY3/B9Jx49i6Xjo9K9VyNyXY2zCEUzaDDxqiDPNgFJBmC49581M4Y\nBqASa3TtR3/aOxB+k8LTkw4wLN9d5pJOGloBuSPlY3rCtYXtwlImamEFa4KRTX5+\nUwLosIIZEFh0SHUIjbopH6/LyXaI5x6WRbaqyVZFV1W0cjg9xGiceDcnDzFvbXNR\nsxTAWxxH+XRPH4ssCtVFdfKr6dx5EDMihU6QuMlHMUtO7yrCMp2vOHNIx8dLR4dF\n4onqkx87aSREaoGi/2BEqSbrrXlK0hMwwOpIx44ReTErKxeeiRGCYW9qt6SAnHh5\n1LiZ3mIUHXrkgimHm2K7qLsPpFqG46mRw1//KCDgbuF2WOsrP90ik7wzRSbU5QTs\nzF61P2zwJzU+5qZbWx8CnZ3DcBCZhVDiYGJNtAomUlKj+Ms11Dyu8TBCdz01tPTs\ngze8AO7lmbw+qnPugxCSEkwoeeZy1guyfPKav8SfNktbTWyxRJ95r8Yk4DuirAU9\nzuS1VJb3dhMuy61cRPjxCbbaCHro6E/6XT0di5qyiA/lxNJuV+6extMvwuIcHSsA\njclsDuxjYUndbPj6kq8rlvGYT4zaTe9P8m4BMo/kZTK/QuOMXW507BrjXfczl3nn\n4QT4iHs61c1cC2rasmAiOgUni73BWrHDZZKBNvpL9Zw6UDx/5ALTuPR5/2G/HEeQ\nYZuG54O2QlDdd/a5VtF5ZYs55/dJ3M0VDDcb/8Y+CnQz5YxTXZrF/FUbwczLjiJy\nONgl9JJT+QmBOv5B7K1G9C8+SiHFpHvpzSzm1LY9/pvzv0+qqUGJZzL4oZmDA6Qv\nrooWptPEQyblrhm0pFhFOV+1TVSUATf+W3v6qHsKlZwkhLl1PKOIRiRohaU9WvJQ\nHg82735kllufWfNbrd939uT+UrBLNJLvuPMNxmxZnPBt30N9n3F8Bq/juFFd+n4S\n8n+FQ580Gax2KmcUw+v99bhOHowtroxWvdxkpDWE0ziZ2KcU+zO3shNBrJBMKbr4\n3RPE48Q6yq7x8m3Nn0fc8AqyVlPqzpwRzQ==\n-----END ENCRYPTED PRIVATE KEY-----', passphrase='test')
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
    bmaily = pubkey.exportKey()
    data = encrypt((encrypt(message, privkey).decode()+'||'+bmaily), bmailt).decode()
    bmailt= bmaily.exportKey()
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
        sendMessage(inp.split('send ').split(' '))
