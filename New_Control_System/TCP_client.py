import socket
import time
from time import sleep

#m = Movement()

HOST = "localhost"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        s.sendall(b'0')
        time.sleep(10)
        s.sendall(b'0')
        time.sleep(1)
        data = s.recv(1024)
        data.decode('utf-8')
        print(data)

