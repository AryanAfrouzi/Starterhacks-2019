import socket

rdata = []

def send(data):
    s = socket.socket()
    s.settimeout(5)
    s.connect(('34.73.41.149', 11219))
    s.send('send'.encode())
    s.send(data)

def sync():
    global rdata
    s = socket.socket()
    s.connect(('34.73.41.149', 11219))
    s.send('sync'.encode())
    rdata += s.recv(1024).decode().split('; ')

sync()
#send('test'.encode())
