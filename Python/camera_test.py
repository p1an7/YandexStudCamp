from builtins import range, len, int
import os
from subprocess import call
import time
import math
import pyzbar.pyzbar as pyzbar
import xr_config as cfg


while True:
    if .cap_open == 0:  # Camera is not open
        try:
            # self.cap = cv2.VideoCapture(0) # Open the camera
            self.cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
        except Exception as e:
            print('opencv camera open error:', e)
        self.cap_open = 1  # Set the flag to 1