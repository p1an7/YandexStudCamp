import socket
import time

import threading

#from Detect_and_rotation import Detection_object

HOST = "192.168.2.173"
PORT = 65432
buf = "1"
#detection_object = Detection_object()
lock = threading.Lock()



def newss():
    global buf
    print("Start")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Подключено к {addr}")
            conn.settimeout(300)  # Установите таймаут для recv
            while True:
                try:
                    data = conn.recv(1024)
                    print(data.decode('utf-8'))
                    if not data:
                        break
                    with lock:
                        buf = "1"

                    conn.sendall(buf.encode('utf-8'))

                    # Проверка на пинг

                except socket.timeout:
                    print("Таймаут соединения, проверяем активность...")

                except Exception as e:
                    print(f"Ошибка в newss: {e}")
                    break

if __name__ == "__main__":
    newss()