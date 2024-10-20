from builtins import float, object
import os
from socket import *
import numpy as np
import GPIO as gpio
import Config as cfg
import keyboard
import time

from New_Control_System.Config_parser import HandleConfig

from Navigation import getAngle

path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)

class Movement(object):
    def __init__(self):
        pass

    def set_speed(self, num, speed):
        """
        Set motor speed, num indicates left or right side, 1 for left side, 2 for right side, speed indicates the set speed value (0-100)
        """
        # print(speed)
        if num == 1:  # Adjust left side
            gpio.ena_pwm(speed)
        elif num == 2:  # Adjust right side
            gpio.enb_pwm(speed)

    def motor_init(self):
        """
        Get the robot's stored speed
        """
        print("Get the robot's stored speed")
        speed = cfgparser.get_data('motor', 'speed')
        cfg.LEFT_SPEED = speed[0]
        cfg.RIGHT_SPEED = speed[1]
        print(speed[0])
        print(speed[1])

    def save_speed(self):
        speed = [0, 0]
        speed[0] = cfg.LEFT_SPEED
        speed[1] = cfg.RIGHT_SPEED
        cfgparser.save_data('motor', 'speed', speed)

    def m1m2_forward(self):
        # Set motor group M1, M2 to forward
        gpio.digital_write(gpio.IN1, True)
        gpio.digital_write(gpio.IN2, False)

    def m1m2_reverse(self):
        # Set motor group M1, M2 to reverse
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, True)

    def m1m2_stop(self):
        # Set motor group M1, M2 to stop
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, False)

    def m3m4_forward(self):
        # Set motor group M3, M4 to forward
        gpio.digital_write(gpio.IN3, True)
        gpio.digital_write(gpio.IN4, False)

    def m3m4_reverse(self):
        # Set motor group M3, M4 to reverse
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, True)

    def m3m4_stop(self):
        # Set motor group M3, M4 to stop
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, False)

    def back(self):
        """
        Set the robot's movement direction to forward
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_forward()
        self.m3m4_forward()

    def forward(self):
        """
        Set the robot's movement direction to backward
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_reverse()
        self.m3m4_reverse()
    def forwardslow(self):
        """
        Set the robot's movement direction to backward
        """
        self.set_speed(1, 50)
        self.set_speed(2, 50)
        self.m1m2_reverse()
        self.m3m4_reverse()
    def right(self):
        """
        Set the robot's movement direction to turn left
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_reverse()
        self.m3m4_forward()

    def rightslow(self):
        """
        Set the robot's movement direction to turn left
        """
        self.set_speed(1, 40)
        self.set_speed(2,40)
        self.m1m2_reverse()
        self.m3m4_forward()

    def left(self):
        """
        Set the robot's movement direction to turn right
        """
        self.set_speed(1, cfg.LEFT_SPEED)
        self.set_speed(2, cfg.RIGHT_SPEED)
        self.m1m2_forward()
        self.m3m4_reverse()
    def leftslow(self):
        """
        Set the robot's movement direction to turn right
        """
        self.set_speed(1, 40)
        self.set_speed(2, 40)
        self.m1m2_forward()
        self.m3m4_reverse()
    def stop(self):
        """
        Set the robot's movement direction to stop
        """
        self.set_speed(1, 0)
        self.set_speed(2, 0)
        self.m1m2_stop()
        self.m3m4_stop()

    def control_with_keyboard(self):
        """
        Control the robot using keyboard inputs
        """
        while True:
            if keyboard.is_pressed('w'):
                self.forward()
            elif keyboard.is_pressed('s'):
                self.back()
            elif keyboard.is_pressed('a'):
                self.left()
            elif keyboard.is_pressed('d'):
                self.right()
            elif keyboard.is_pressed(' '):
                self.stop()
            elif keyboard.is_pressed('q'):
                break
    def angelrotate(self , turnspeed, angel ):
        start_time = time.time()

        while time.time()-start_time<=angel/turnspeed:
            if angel<0:
                self.left()
            else:
                self.right()
        else:
            self.stop()
    def rotate(self):
        while True:
            self.angelrotate(self, похуй_константа_какая-то_псчитаем , getangel())
            time.sleep(2)
            if -0,0174533<getangel()<0,0174533:
                break





