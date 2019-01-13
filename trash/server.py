import socket

#testing script

address = ("34.73.41.149", 11219)

s = socket.socket()
s.connect(address)
s.send('test'.encode())


