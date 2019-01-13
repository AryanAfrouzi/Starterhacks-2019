import socket
import threading
import requests
import random
import time

prdata = []
dataforcli = []

def send(data, address):
    s = socket.socket()
    s.settimeout(5)
    s.connect((address, 11219))
    s.send(data)

def forwardThread():
    global dataforcli, prdata
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 11219))
    s.listen(5)
    while True:
        data = ""
        client, address = s.accept()
        cont = 1
        if address[0] == '129.97.124.4':
            instruct = client.recv(1024).decode()
            if instruct == 'send':
                data = client.recv(1024)
            else:
                client.send('; '.join(dataforcli))
                dataforcli = []
                cont = 0
        if cont == 1:
            print("Connection established with "+str(address))
            if data == "":
                data = client.recv(1024)
            print("Data received, proceeding to forward..")
            print("Data = "+str(data.decode()))
            if data not in prdata:
                prdata.append(data)
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
