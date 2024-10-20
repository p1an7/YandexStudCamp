import socket
import threading

from Detect_and_rotation import Detection_object

HOST = "127.0.0.1"
PORT = 65432
buf = "1"
detection_object = Detection_object()
lock = threading.Lock()


# "127.0.0.1"
# "192.168.2.173"
def detect():
    global buf, detection_object
    while True:
        try:
            detection_object.get_coordinate_from_model()
        except Exception as e:
            print(f"Ошибка в detect: {e}")


def newss():
    global buf
    print("Start")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Подключено к {addr}")
            while True:
                try:
                    print("1")
                    data = conn.recv(1024)
                    if not data:
                        break

                    with lock:  # Используем блокировку для защиты buf
                        buf = detection_object.for_send

                    conn.sendall(buf.encode('utf-8'))
                except Exception as e:
                    print(f"Ошибка в newss: {e}")
                    break


t1 = threading.Thread(target=detect)
t2 = threading.Thread(target=newss)
t1.start()
t2.start()

t1.join()  # Ждем завершения первого потока
t2.join()  # Ждем завершения второго потока
