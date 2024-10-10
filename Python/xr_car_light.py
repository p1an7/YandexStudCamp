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
@Explain : Car light related functions
@contact :
@Time    :2020/05/09
@File    :xr_car_light.py
@Software: PyCharm
"""

from builtins import int, range
import xr_config as cfg

import time
from xr_i2c import I2c

i2c = I2c()

class Car_light(object):
    def __init__(self):
        pass

    def set_led(self, group, num, color):
        """
        Set the state of the RGB light
        :param group: Light group, equals 1 for power light, 2 for car light
        :param num: Light index
        :param color: Set color, in config COLOR can choose corresponding color, can only set defined color
        :return:
        """
        if 0 < num < 9 and 0 < group < 3 and color < 9:
            sendbuf = [0xff, group + 3, num, color, 0xff]
            i2c.writedata(i2c.mcu_address, sendbuf)
            time.sleep(0.005)
        # print("set_led group%d, LED%d, color%d  :OK \r\n", group, num, color)

    def set_ledgroup(self, group, count, color):
        """
        Set the state of the number of RGB lights
        :param group: Light group, equals 1 for power light, 2 for car light
        :param count: Number of lights
        :param color: Set color, in config COLOR can choose corresponding color, can only set defined color
        :return:
        """
        if 0 < count < 9 and 0 < group < 3 and color < 9:
            sendbuf = [0xff, group + 1, count, color, 0xff]
            i2c.writedata(i2c.mcu_address, sendbuf)
            time.sleep(0.005)
        # print("set_led group%d, LED%d, color%d  :OK \r\n", group, count, color)

    def open_light(self):
        """
        Turn on all car lights
        :return:
        """
        # print("All car lights are on")
        self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['white'])
        time.sleep(0.01)

    def close_light(self):
        """
        Turn off all car lights
        :return:
        """
        # print("All car lights are off")
        self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
        time.sleep(0.01)

    def left_turn_light(self):
        """
        Left turn flowing light
        :return:
        """
        # print("Turn left")
        self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['red'])
        time.sleep(0.12)
        self.set_led(cfg.CAR_LIGHT, 7, cfg.COLOR['red'])
        time.sleep(0.12)
        self.set_led(cfg.CAR_LIGHT, 8, cfg.COLOR['red'])
        time.sleep(0.12)
        self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
        time.sleep(0.12)

    def right_turn_light(self):
        """
        Right turn flowing light
        :return:
        """
        self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['red'])
        time.sleep(0.12)
        self.set_led(cfg.CAR_LIGHT, 2, cfg.COLOR['red'])
        time.sleep(0.12)
        self.set_led(cfg.CAR_LIGHT, 1, cfg.COLOR['red'])
        time.sleep(0.12)
        self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
        time.sleep(0.12)

    def forward_turn_light(self):
        self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['green'])
        time.sleep(0.05)
        self.set_led(cfg.CAR_LIGHT, 4, cfg.COLOR['green'])
        time.sleep(0.05)
        self.set_led(cfg.CAR_LIGHT, 5, cfg.COLOR['green'])
        time.sleep(0.05)
        self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['green'])
        time.sleep(0.12)

    def back_turn_light(self):
        self.set_led(cfg.CAR_LIGHT, 3, cfg.COLOR['red'])
        time.sleep(0.05)
        self.set_led(cfg.CAR_LIGHT, 4, cfg.COLOR['red'])
        time.sleep(0.05)
        self.set_led(cfg.CAR_LIGHT, 5, cfg.COLOR['red'])
        time.sleep(0.05)
        self.set_led(cfg.CAR_LIGHT, 6, cfg.COLOR['red'])
        time.sleep(0.12)

    def init_led(self):
        """
        Startup state car light
        :return:
        """
        self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
        for j in range(8):
            for i in range(8):
                self.set_led(cfg.CAR_LIGHT, i + 1, j + 1)
                time.sleep(0.05)
                self.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])
                time.sleep(0.05)

            for i in range(4):
                self.set_led(cfg.CAR_LIGHT, i + 1, j + 1)
                self.set_led(cfg.CAR_LIGHT, 8 - i, j + 1)
                time.sleep(0.05)

            for i in range(4):
                self.set_led(cfg.CAR_LIGHT, i + 1, cfg.COLOR['black'])
                self.set_led(cfg.CAR_LIGHT, 8 - i, cfg.COLOR['black'])
                time.sleep(0.05)
