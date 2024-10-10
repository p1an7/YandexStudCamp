# coding:utf-8
"""
Raspberry Pi WiFi Wireless Video Car Robot Driver Source Code
Author: Sence
Copyright: Xiaor Technology (Shenzhen Xiaor Technology Co., Ltd. www.xiao-r.com); WIFI Robot Forum www.wifi-robots.com
This code can be freely modified, but it is prohibited to use it for commercial profit purposes!
This code has applied for software copyright protection, and if any infringement is found, it will be prosecuted immediately!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain : Camera recognition and car movement functions
@contact :
@Time    :2020/05/09
@File    :xr_function.py
@Software: PyCharm
"""

from builtins import float, object, bytes

import time
import xr_config as cfg

from xr_socket import Socket
socket = Socket()

from xr_motor import RobotDirection
go = RobotDirection()

from xr_car_light import Car_light

car_light = Car_light()

class Function(object):
    def __init__(self):
        pass

    def linepatrol_control(self):
        """
        Camera line patrol car movement
        :return:
        """
        while cfg.CAMERA_MOD == 1:
            dx = cfg.LINE_POINT_TWO - cfg.LINE_POINT_ONE  # Difference in center coordinates of upper and lower sampling points
            mid = int(cfg.LINE_POINT_ONE + cfg.LINE_POINT_TWO) / 2  # Average center coordinates of upper and lower sampling points

            print("dx==%d" % dx)  # Print the difference in center coordinates of upper and lower sampling points
            print("mid==%s" % mid)  # Print the average center coordinates of upper and lower sampling points

            if 0 < mid < 260:  # If the line patrol center point is biased to the left, indicating the car is deviating to the right, it needs to turn left to correct.
                print("turn left")
                go.left()
            elif mid > 420:  # If the line patrol center point is biased to the right, indicating the car is deviating to the left, it needs to turn right to correct.
                print("turn right")
                go.right()
            else:  # If the line patrol center point is centered
                if dx > 45:
                    print("turn left")  # The line has a tendency to tilt to the right
                    go.left()
                elif dx < -45:
                    print("turn right")  # The line has a tendency to tilt to the left
                    go.right()
                else:
                    print("go straight")  # The line is in the center position and is in a vertical state
                    go.forward()
            time.sleep(0.007)
            go.stop()
            time.sleep(0.007)

    def qrcode_control(self):
        """
        QR code detection and recognition control car movement
        :return:
        """
        cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
        cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
        cfg.LEFT_SPEED = 30  # Set an appropriate speed
        cfg.RIGHT_SPEED = 30
        code_status = 0
        while cfg.CAMERA_MOD == 4:
            time.sleep(0.05)
            if cfg.BARCODE_DATE == 'start':  # Detect the start signal, the start QR code
                #print(cfg.BARCODE_DATE)
                buf = bytes([0xff, 0x13, 0x0a, 0x00, 0xff])
                socket.sendbuf(buf)
                #cfg.LIGHT_STATUS = cfg.TURN_FORWARD
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['blue'])
                time.sleep(1.5)
                code_status = 1  # code_status
            elif cfg.BARCODE_DATE == 'stop':  # Detect the stop signal, the stop QR code
                #print(cfg.BARCODE_DATE)
                buf = bytes([0xff, 0x13, 0x0a, 0x01, 0xff])
                socket.sendbuf(buf)
                #cfg.LIGHT_STATUS = cfg.STOP
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['white'])
                time.sleep(1.5)
                code_status = 0  # code_status

            if code_status:
                if cfg.BARCODE_DATE == 'forward':  # Detect the forward QR code, the car moves forward
                    #print("forward")
                    buf = bytes([0xff, 0x13, 0x0a, 0x02, 0xff])
                    socket.sendbuf(buf)
                    cfg.LIGHT_STATUS = cfg.TURN_FORWARD
                    go.forward()
                    time.sleep(2.5)
                    go.stop()
                    time.sleep(0.5)
                elif cfg.BARCODE_DATE == 'back':  # Detect the back QR code, the car moves backward
                    #print("back")
                    buf = bytes([0xff, 0x13, 0x0a, 0x03, 0xff])
                    socket.sendbuf(buf)
                    cfg.LIGHT_STATUS = cfg.TURN_BACK
                    go.back()
                    time.sleep(2.5)
                    go.stop()
                    time.sleep(0.5)
                elif cfg.BARCODE_DATE == 'left':  # Detect the left QR code, the car turns left
                    #print("left")
                    buf = bytes([0xff, 0x13, 0x0a, 0x04, 0xff])
                    socket.sendbuf(buf)
                    cfg.LIGHT_STATUS = cfg.TURN_LEFT
                    go.left()
                    time.sleep(1.5)
                    go.stop()
                    time.sleep(0.5)
                elif cfg.BARCODE_DATE == 'right':  # Detect the right QR code, the car turns right
                    #print("right")
                    buf = bytes([0xff, 0x13, 0x0a, 0x05, 0xff])
                    socket.sendbuf(buf)
                    cfg.LIGHT_STATUS = cfg.TURN_RIGHT
                    go.right()
                    time.sleep(1.5)
                    go.stop()
                    time.sleep(0.5)
                else:
                    #print("go.forward")
                    cfg.LIGHT_STATUS = cfg.STOP
                    #go.forward()
            else:
                go.stop()
                time.sleep(0.05)
        go.stop()
