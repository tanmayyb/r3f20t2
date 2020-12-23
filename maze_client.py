#!/usr/bin/env python
import socket


BUFFER_SIZE = 1024
MESSAGE = 'request'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5004))
i = 0
while 1:
    s.send(str(i).encode('ascii'))
    data = s.recv(BUFFER_SIZE).decode()
    if data == "stop":
        print("received stop: client closing")
        s.close()
        break
    print("received: ", data)
    i+=1
