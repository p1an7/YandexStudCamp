import socket

HOST = "192.168.2.104"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        s.sendall(b"Hello world")
        data = s.recv(1024)
        print(data.decode('utf-8'))
