import socket
import time
from time import sleep
from Package_parser import parse
#m = Movement()

HOST = "localhost"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        s.sendall(b'0')
        data = s.recv(1024)
        data.decode('utf-8')
        print(data)
        parse(data)


