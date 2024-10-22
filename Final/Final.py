import cv2
from ultralytics import YOLO
from home_camera import TopCamera

model = YOLO('best_up.pt')
cam = TopCamera()

# URL для подключения к IP-камере. Это может быть RTSP или другой протокол потокового видео
ip_camera_url_left = "rtsp://Admin:rtf123@192.168.2.250/251:554/1/1"
cap = cv2.VideoCapture(ip_camera_url_left)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cam.undistort(frame)


