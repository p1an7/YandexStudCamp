# coding:utf-8
"""
Raspberry Pi WiFi Wireless Video Car Robot Driver Source Code
Author: Sence
Copyright: XiaoR Technology (Shenzhen XiaoR Technology Co., Ltd. www.xiao-r.com); WIFI Robot Forum www.wifi-robots.com
This code can be freely modified, but commercial use for profit is prohibited!
This code has been applied for software copyright protection, and legal action will be taken immediately upon discovery of infringement!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain : Ultrasonic module
@Time    : 2020/05/09
@File    : xr_ultrasonic.py
@Software: PyCharm
"""
import time
from builtins import int, chr, object

import xr_gpio as gpio
import xr_config as cfg

from xr_motor import RobotDirection
go = RobotDirection()

from xr_servo import Servo
servo = Servo()

from xr_socket import Socket
socket = Socket()

class Ultrasonic(object):
    def __init__(self):
        self.MAZE_ABLE = 0
        self.MAZE_CNT = 0
        self.MAZE_TURN_TIME = 0
        self.dis = 0
        self.s_L = 0
        self.s_R = 0

    def get_distance(self):
        """
        Function to get ultrasonic distance, returns distance in cm
        """
        time_count = 0
        time.sleep(0.01)
        gpio.digital_write(gpio.TRIG, True)  # Pull up the ultrasonic Trig pin
        time.sleep(0.000015)  # Send a high-level pulse wave of more than 10um
        gpio.digital_write(gpio.TRIG, False)  # Pull down
        while not gpio.digital_read(gpio.ECHO):  # Wait for the Echo pin to change from low to high
            pass
        t1 = time.time()  # Record the start time of the Echo pin high level
        while gpio.digital_read(gpio.ECHO):  # Wait for the Echo pin to change from high to low
            if time_count < 2000:  # Timeout detection to prevent infinite loop
                time_count = time_count + 1
                time.sleep(0.000001)
                pass
            else:
                print("NO ECHO receive! Please check connection")
                break
        t2 = time.time()  # Record the end time of the Echo pin high level
        distance = (t2 - t1) * 340 / 2 * 100  # The duration of the Echo pin high level is the time for the ultrasonic wave to travel from transmission to return, i.e., the distance value of the ultrasonic wave from the object
        # t2-t1 time unit s, sound speed 340m/s, x100 converts the distance value unit from m to cm
        # print("distance is %d" % distance)  # Print distance value
        if distance < 500:  # Normal detection distance value
            # print("distance is %d"%distance)
            cfg.DISTANCE = round(distance, 2)
            return cfg.DISTANCE
        else:
            # print("distance is 0")  # If the distance value is greater than 5m, it is out of the detection range
            cfg.DISTANCE = 0
            return 0

    def avoidbyragar(self):
        """
        Ultrasonic obstacle avoidance function
        """
        cfg.LEFT_SPEED = 30
        cfg.RIGHT_SPEED = 30
        dis = self.get_distance()
        if 25 < dis < 300 or dis == 0:  # Distance greater than 25cm and less than 300cm within the ultrasonic detection range, equal to 0 when far distance exceeds the ultrasonic detection range
            cfg.AVOID_CHANGER = 1
        else:
            if cfg.AVOID_CHANGER == 1:
                go.stop()
                cfg.AVOID_CHANGER = 0

    def send_distance(self):
        """
        Send ultrasonic data to the host computer
        """
        dis_send = int(self.get_distance())
        # print(dis_send)
        if 1 < dis_send < 255:
            buf = bytes([0xff, 0x31, 0x02, dis_send, 0xff])  # Upload the ultrasonic distance value to the host computer
            try:
                socket.sendbuf(buf)
            except Exception as e:  # Send error
                print('send_distance error:', e)  # Print error information
        else:
            buf = []

    def maze(self):
        """
        Ultrasonic maze walking function
        """
        cfg.LEFT_SPEED = 35
        cfg.RIGHT_SPEED = 35
        # print("Ultrasonic maze walking function")
        self.dis = self.get_distance()  # Get distance value
        if self.MAZE_ABLE == 0 and ((self.dis > 30) or self.dis == 0):  # No obstacles in front and not a dead end
            while ((self.dis > 30) or self.dis == 0) and cfg.CRUISING_FLAG:
                self.dis = self.get_distance()
                go.forward()
            if cfg.CRUISING_FLAG:  # Do not run this when exiting the mode to avoid not stopping the car after exiting the mode
                self.MAZE_CNT = self.MAZE_CNT + 1
                print(self.MAZE_CNT)
                go.stop()
                time.sleep(0.05)
                go.back()  # Back up a little
                time.sleep(0.15)
                go.stop()
                time.sleep(0.05)
                if self.MAZE_CNT > 3:  # Multiple checks if the front is an obstacle to avoid misdetection
                    self.MAZE_CNT = 0
                    self.MAZE_ABLE = 1  # If the front is a dead end

        else:
            go.stop()
            self.s_L = 0
            self.s_R = 0
            time.sleep(0.1)
            servo.set(7, 5)  # First, turn the servo that rotates the ultrasonic to the right
            if cfg.CRUISING_FLAG:
                time.sleep(0.25)
            self.s_R = self.get_distance()
            if cfg.CRUISING_FLAG:
                time.sleep(0.2)

            servo.set(7, 175)  # Then, turn the servo to the left
            if cfg.CRUISING_FLAG:
                time.sleep(0.3)
            self.s_L = self.get_distance()
            if cfg.CRUISING_FLAG:
                time.sleep(0.2)
            servo.set(7, 80)  # Then, turn the servo to the middle
            time.sleep(0.1)

            if (self.s_R == 0) or (self.s_R > self.s_L and self.s_R > 20):  # If the right side is wide and the obstacle distance is greater than 20, and the right side is greater than the left side
                self.MAZE_ABLE = 0
                cfg.LEFT_SPEED = 99  # Turning speed, if on different surfaces, manually adjust the speed to meet the turning force, this is the speed on the carpet which needs to be higher
                cfg.RIGHT_SPEED = 99
                go.right()
                if cfg.CRUISING_FLAG:
                    time.sleep(cfg.MAZE_TURN_TIME / 1000)  # Turning time, adjust according to the above turning speed, actual test to turn to about 90 degrees
                cfg.LEFT_SPEED = 45
                cfg.RIGHT_SPEED = 45

            elif (self.s_L == 0) or (self.s_R < self.s_L and self.s_L > 20):  # If the left side is wide and the obstacle distance is greater than 20, and the left side is greater than the right side
                self.MAZE_ABLE = 0
                cfg.LEFT_SPEED = 99  # Turning speed, if on different surfaces, manually adjust the speed to meet the turning force, this is the speed on the carpet which needs to be higher
                cfg.RIGHT_SPEED = 99
                go.left()
                if cfg.CRUISING_FLAG:
                    time.sleep(cfg.MAZE_TURN_TIME / 1000)  # Turning time, adjust according to the above turning speed, actual test to turn to about 90 degrees
                cfg.LEFT_SPEED = 45
                cfg.RIGHT_SPEED = 45

            else:  # Cannot go forward, cannot go left or right, i.e., entered a dead end, can only return the same way
                self.MAZE_ABLE = 1  # Set the flag to 1 to avoid re-entering the dead end, can only back up a little and then check left and right to see if there are other passages, when any side passage is clear, set the flag to 0, then can go forward
                go.back()
                if cfg.CRUISING_FLAG:
                    time.sleep(0.3)

            go.stop()
            time.sleep(0.1)
