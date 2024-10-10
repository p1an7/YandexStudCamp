# coding:utf-8
"""
WiFi Wireless Video Car Robot Driver Source Code
Author: Sence
Copyright: Xiaor Technology (Shenzhen Xiaor Technology Co., Ltd. www.xiao-r.com); WIFI Robot Forum www.wifi-robots.com
This code can be freely modified, but it is prohibited to use it for commercial profit purposes!
This code has applied for software copyright protection, and if any infringement is found, it will be prosecuted immediately!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain : Camera recognition related functions
@contact :
@Time    :2020/05/09
@File    :xr_camera.py
@Software: PyCharm
"""

from builtins import range, len, int
import os
from subprocess import call
import time
import math
import pyzbar.pyzbar as pyzbar
import xr_config as cfg

from xr_motor import RobotDirection

go = RobotDirection()
import cv2

from xr_servo import Servo

servo = Servo()

from xr_pid import PID

class Camera(object):
    def __init__(self):
        self.fre_count = 1  # Number of samples
        self.px_sum = 0  # Accumulated value of sample point x coordinates
        self.cap_open = 0  # Flag indicating whether the camera is open
        self.cap = None

        self.servo_X = 7
        self.servo_Y = 8

        self.angle_X = 90
        self.angle_Y = 20

        self.X_pid = PID(0.03, 0.09, 0.0005)  # Instance of a PID algorithm for X-axis coordinates, PID parameters: the first represents the P value, the second represents the I value, and the third represents the D value
        self.X_pid.setSampleTime(0.005)  # Set the PID algorithm cycle
        self.X_pid.setPoint(240)  # Set the PID algorithm target value, which is the target value, here 160 refers to the x-axis center point of the screen, the x-axis pixels are 320, half is 160

        self.Y_pid = PID(0.035, 0.08, 0.002)  # Instance of a PID algorithm for Y-axis coordinates, PID parameters: the first represents the P value, the second represents the I value, and the third represents the D value
        self.Y_pid.setSampleTime(0.005)  # Set the PID algorithm cycle
        self.Y_pid.setPoint(160)  # Set the PID algorithm target value, which is the target value, here 160 refers to the y-axis center point of the screen, the y-axis pixels are 320, half is 160

    def linepatrol_processing(self):
        """
        Camera line patrol data collection
        :return:
        """
        while True:
            if self.cap_open == 0:  # Camera is not open
                try:
                    # self.cap = cv2.VideoCapture(0) # Open the camera
                    self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                except Exception as e:
                    print('opencv camera open error:', e)
                self.cap_open = 1  # Set the flag to 1
            else:
                try:
                    ret, frame = self.cap.read()  # Get the camera frame data
                    if ret:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert RGB to GRAY color space
                        if cfg.PATH_DECT_FLAG == 0:
                            ret, thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)  # Patrol black line
                        else:
                            ret, thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)  # Patrol white line
                        for j in range(0, 640, 5):  # X-axis horizontal sampling, sampling points interval 5 pixels
                            if thresh1[350, j] == 0:  # Take the image y-axis middle upper value 350, perform binary judgment on the sampling points
                                self.px_sum = self.px_sum + j  # Accumulate the x coordinates of the sampling points that meet the line color
                                self.fre_count = self.fre_count + 1  # Accumulate the number of samples
                        cfg.LINE_POINT_ONE = self.px_sum / self.fre_count  # Use x coordinate accumulated value / number of samples = average value of sampling points that meet the line color, equivalent to the actual position point of the line x coordinate
                        self.px_sum = 0  # Clear the accumulated value
                        self.fre_count = 1  # Clear the number of samples, minimum is 1
                        for j in range(0, 640, 5):  # X-axis horizontal sampling, sampling points interval 5 pixels
                            if thresh1[200, j] == 0:  # Take the image y-axis middle lower value 200, perform binary judgment on the sampling points
                                self.px_sum = self.px_sum + j  # Accumulate the x coordinates of the sampling points that meet the line color
                                self.fre_count = self.fre_count + 1  # Accumulate the number of samples
                        cfg.LINE_POINT_TWO = self.px_sum / self.fre_count  # Use x coordinate accumulated value / number of samples = average value of sampling points that meet the line color, equivalent to the actual position point of the line x coordinate
                        self.px_sum = 0  # Clear the accumulated value
                        self.fre_count = 1  # Clear the number of samples, minimum is 1
                        print("point1 = %d ,point2 = %d"%(cfg.LINE_POINT_ONE,cfg.LINE_POINT_TWO))
                except Exception as e:  # Capture and print error information
                    go.stop()  # Exit, stop the car
                    self.cap_open = 0  # Close flag
                    self.cap.release()  # Release the camera
                    print('linepatrol_processing error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # If exiting line patrol mode
                go.stop()  # Exit line patrol, stop the car
                self.cap_open = 0  # Close flag
                self.cap.release()  # Release the camera
                break  # Exit the loop

    def facefollow(self):
        """
        Face detection and camera follow
        :return:
        """
        time.sleep(3)
        while True:

            if self.cap_open == 0:  # Camera is not open
                try:
                    # self.cap = cv2.VideoCapture(0)	# Open the camera
                    self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                    self.cap_open = 1  # Set the flag to 1
                    self.cap.set(3, 320)  # Set the image width to 320 pixels
                    self.cap.set(4, 320)  # Set the image height to 320 pixels
                    face_cascade = cv2.CascadeClassifier(
                        '/home/pi/work/python_src/face.xml')  # Face recognition OpenCV cascade detector, can also be changed to other feature detectors, such as nose
                except Exception as e:
                    print('opencv camera open error:', e)
                    break

            else:
                try:
                    ret, frame = self.cap.read()  # Get the camera video stream
                    if ret == 1:  # Determine if the camera is working
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # First convert each frame to grayscale, then search in the grayscale image
                        faces = face_cascade.detectMultiScale(gray)  # Search for faces
                        if len(faces) > 0:  # When there are face contours in the video
                            print('face found!')
                            for (x, y, w, h) in faces:
                                # Parameters are "target frame", "rectangle", "rectangle size", "line color", "width"
                                cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
                                result = (x, y, w, h)
                                x_middle = result[0] + w / 2  # x-axis center
                                y_middle = result[1] + h / 2  # y-axis center

                                self.X_pid.update(x_middle)  # Put the X-axis data into the PID to calculate the output value
                                self.Y_pid.update(y_middle)  # Put the Y-axis data into the PID to calculate the output value
                                # print("X_pid.output==%d"%self.X_pid.output)     # Print X output
                                # print("Y_pid.output==%d"%self.Y_pid.output)     # Print Y output
                                self.angle_X = math.ceil(self.angle_X + 1 * self.X_pid.output)  # Update the X-axis servo angle, use the last servo angle plus a certain proportion of the increment value to update the servo angle
                                self.angle_Y = math.ceil(
                                    self.angle_Y + 0.8 * self.Y_pid.output)  # Update the Y-axis servo angle, use the last servo angle plus a certain proportion of the increment value to update the servo angle

                                # if self.angle_X > 180:  # Limit the maximum angle of the X-axis
                                #     self.angle_X = 180
                                # if self.angle_X < 0:  # Limit the minimum angle of the X-axis
                                #     self.angle_X = 0
                                # if self.angle_Y > 180:  # Limit the maximum angle of the Y-axis
                                #     self.angle_Y = 180
                                # if self.angle_Y < 0:  # Limit the minimum angle of the Y-axis
                                #     self.angle_Y = 0
                                self.angle_X = min(180, max(0, self.angle_X))
                                self.angle_Y = min(180, max(0, self.angle_Y))
                                print("angle_X: %d" % self.angle_X)  # Print X-axis servo angle
                                print("angle_Y: %d" % self.angle_Y)  # Print Y-axis servo angle
                                servo.set(self.servo_X, self.angle_X)  # Set X-axis servo
                                servo.set(self.servo_Y, self.angle_Y)  # Set Y-axis servo
                    # cv2.imshow("capture", frame)  # Display the image
                except Exception as e:  # Capture and print error information
                    go.stop()  # Exit, stop the car
                    self.cap_open = 0  # Close flag
                    self.cap.release()  # Release the camera
                    print('facefollow error:', e)
            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # If exiting face recognition mode
                go.stop()  # Exit, stop the car
                self.cap_open = 0  # Close flag
                self.cap.release()  # Release the camera
                # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'  # Command to end the camera video stream
                # # call("%s" % path_sh, shell=True)  # Start the shell command to end the camera video stream, the camera face detection will use opencv to occupy the camera
                # try:
                #     call("%s" % path_sh, shell=True)  # Start the shell command to end the camera video stream, the camera color detection will use opencv to occupy the camera
                # except Exception as e:
                #     print(e.message)
                time.sleep(2)
                break  # Exit the loop

    def colorfollow(self):
        """
        Color detection camera follow
        :return:
        """
        while True:
            if self.cap_open == 0:  # Camera is not open
                # self.cap = cv2.VideoCapture(0)		# Open the camera
                self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                self.cap_open = 1  # Set the flag to 1
                self.cap.set(3, 320)  # Set the image width to 320 pixels
                self.cap.set(4, 320)  # Set the image height to 320 pixels
            else:
                try:
                    ret, frame = self.cap.read()  # Get the camera video stream
                    if ret == 1:  # Determine if the camera is working
                        frame = cv2.GaussianBlur(frame, (5, 5), 0)  # Gaussian filtering GaussianBlur() makes the image blurry
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the image color space to HSV style for detection
                        mask = cv2.inRange(hsv, cfg.COLOR_LOWER[cfg.COLOR_INDEX],
                                           cfg.COLOR_UPPER[cfg.COLOR_INDEX])  # Set the threshold to remove the background and retain the set color

                        mask = cv2.erode(mask, None, iterations=2)  # Display the eroded image
                        mask = cv2.GaussianBlur(mask, (3, 3), 0)  # Gaussian blur
                        res = cv2.bitwise_and(frame, frame, mask=mask)  # Image merge

                        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]  # Edge detection

                        if len(cnts) > 0:  # Determine the position information of the recognized object through edge detection to obtain the relative coordinates
                            cnt = max(cnts, key=cv2.contourArea)
                            (x, y), radius = cv2.minEnclosingCircle(cnt)
                            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)  # Draw a circle
                            # print(int(x), int(y))

                            self.X_pid.update(x)  # Put the X-axis data into the PID to calculate the output value
                            self.Y_pid.update(y)  # Put the Y-axis data into the PID to calculate the output value
                            # print("X_pid.output==%d"%X_pid.output)		# Print X output
                            # print("Y_pid.output==%d"%Y_pid.output)		# Print Y output
                            self.angle_X = math.ceil(
                                self.angle_X + 1 * self.X_pid.output)  # Update the X-axis servo angle, use the last servo angle plus a certain proportion of the increment value to update the servo angle
                            self.angle_Y = math.ceil(
                                self.angle_Y + 0.8 * self.Y_pid.output)  # Update the Y-axis servo angle, use the last servo angle plus a certain proportion of the increment value to update the servo angle
                            # print("angle_X-----%d" % self.angle_X)	# Print X-axis servo angle
                            # print("angle_Y-----%d" % self.angle_Y)	# Print Y-axis servo angle
                            if self.angle_X > 180:  # Limit the maximum angle of the X-axis
                                self.angle_X = 180
                            if self.angle_X < 0:  # Limit the minimum angle of the X-axis
                                self.angle_X = 0
                            if self.angle_Y > 180:  # Limit the maximum angle of the Y-axis
                                self.angle_Y = 180
                            if self.angle_Y < 0:  # Limit the minimum angle of the Y-axis
                                self.angle_Y = 0
                            servo.set(self.servo_X, self.angle_X)  # Set X-axis servo
                            servo.set(self.servo_Y, self.angle_Y)  # Set Y-axis servo
                except Exception as e:  # Capture and print error information
                    go.stop()  # Exit, stop the car
                    self.cap_open = 0  # Close flag
                    self.cap.release()  # Release the camera
                    print('colorfollow error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # If exiting camera color detection follow mode
                go.stop()  # Exit, stop the car
                self.cap_open = 0  # Close flag
                self.cap.release()  # Release the camera
                break  # Exit the loop

    def decodeDisplay(self, image):
        """
        QR code recognition
        :param image: Camera data frame
        :return: image Recognized image data frame
        """
        barcodes = pyzbar.decode(image)
        if barcodes == []:
            cfg.BARCODE_DATE = None
            cfg.BARCODE_TYPE = None
        else:
            for barcode in barcodes:
                # Extract the boundary box position of the barcode
                # Draw the boundary box of the barcode in the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # The barcode data is a byte object, so if we want to draw it out on the output image
                # We need to convert it to a string first
                cfg.BARCODE_DATE = barcode.data.decode("utf-8")
                cfg.BARCODE_TYPE = barcode.type

                # Draw the barcode data and barcode type on the image
                text = "{} ({})".format(cfg.BARCODE_DATE, cfg.BARCODE_TYPE)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            .5, (0, 0, 125), 2)

            # Print the barcode data and barcode type to the terminal
        # print("[INFO] Found {} barcode: {}".format(cfg.BARCODE_TYPE, cfg.BARCODE_DATE))
        return image

    def qrcode_detection(self):
        """
        Camera QR code recognition movement
        :return:
        """
        while True:
            if self.cap_open == 0:  # Camera is not open
                # self.cap = cv2.VideoCapture(0)	# Open the camera
                self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
                self.cap_open = 1  # Set the flag to 1
            else:
                try:
                    ret, frame = self.cap.read()  # Get the camera video stream
                    if ret == 1:  # Determine if the camera is working
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale image
                        img = self.decodeDisplay(gray)  # Recognize QR code
                # cv2.imshow("qrcode", img)	# Display in the window
                except Exception as e:  # Capture and print error information
                    go.stop()  # Exit, stop the car
                    self.cap_open = 0  # Close flag
                    self.cap.release()  # Release the camera
                    print('qrcode_detection error:', e)

            if self.cap_open == 1 and cfg.CAMERA_MOD == 0:  # If exiting camera QR code detection mode
                go.stop()  # Exit, stop the car
                self.cap_open = 0  # Close flag
                self.cap.release()  # Release the camera
                break  # Exit the loop

    def run(self):
        """
        Camera mode switching
        :return:
        """
        while True:
            if cfg.CAMERA_MOD == 1:  # Camera line patrol mode
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.LEFT_SPEED = 45  # Lower the speed during camera line patrol
                cfg.RIGHT_SPEED = 45
                self.linepatrol_processing()
            elif cfg.CAMERA_MOD == 2:  # Camera face detection follow
                self.facefollow()
            elif cfg.CAMERA_MOD == 3:  # Camera color detection follow
                self.colorfollow()
            elif cfg.CAMERA_MOD == 4:  # Camera QR code detection
                self.qrcode_detection()
            else:
                pass
            time.sleep(0.05)
