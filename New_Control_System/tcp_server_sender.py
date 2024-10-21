import socket
import threading

from Detect_and_rotation import Detection_object

HOST = "192.168.2.173"
PORT = 65432
buf = "1"
detection_object = Detection_object()
lock = threading.Lock()

# "127.0.0.1"
# "192.168.2.173"

flag_what_work = "m"  # m - motors, s - servo
motor_command = 0  # 0 - time, 1 - angle
robot_movement = "f"  # f, r, l, b - forward, right, left, back
time = 0.2  # in seconds
angle = 90  # in degrees
delemitr_symbol = "/"
sms_for_servo = "o"


def front_camera():
    global buf, detection_object
    while True:
        try:
            detection_object.get_coordinate_from_model()
        except Exception as e:
            print(f"Ошибка в detect: {e}")
    # TODO YOLO from front camera


def top_camera():
    global buf
    pass
    # TODO YOLO from top camera


def make_massage():
    global flag_what_work, motor_command, robot_movement, time, angle, delemitr_symbol, sms_for_servo
    if flag_what_work == "m":
        if motor_command == 0:
            result = flag_what_work + delemitr_symbol + str(
                motor_command) + delemitr_symbol + robot_movement + delemitr_symbol + str(time)
            return result
        elif motor_command == 1:
            if robot_movement == "r" or robot_movement == "l":
                result = flag_what_work + delemitr_symbol + str(
                    motor_command) + delemitr_symbol + robot_movement + delemitr_symbol + str(angle)
                return result
        else:
            return None
    elif flag_what_work == "s":
        return flag_what_work + delemitr_symbol + sms_for_servo


def protocol():
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


t1 = threading.Thread(target=front_camera)
t1.start()
t2 = threading.Thread(target=protocol)

t2.start()

t1.join()  # Ждем завершения первого потока
t2.join()  # Ждем завершения второго потока
