"""
Raspberry Pi WiFi Wireless Video Car Robot Driver Source Code
Author: Sence
Copyright: XiaoR Technology (Shenzhen XiaoR Technology Co., Ltd. www.xiao-r.com); WIFI Robot Network Forum www.wifi-robots.com
This code can be freely modified, but it is prohibited to use it for commercial profit purposes!
This code has applied for software copyright protection, and any infringement will be prosecuted immediately!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain : Control servo
@contact :
@Time    : 2020/05/09
@File    : XiaoR_servo.py
@Software: PyCharm
"""
from builtins import hex, eval, int, object
from xr_i2c import I2c
import os

i2c = I2c()
import xr_config as cfg

from xr_configparser import HandleConfig
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)

class Servo(object):
    """
    Servo control class
    """
    def __init__(self):
        pass

    def angle_limit(self, angle):
        """
        Limit the servo angle to prevent the servo from jamming and burning out
        """
        if angle > cfg.ANGLE_MAX:  # Limit the maximum angle value
            angle = cfg.ANGLE_MAX
        elif angle < cfg.ANGLE_MIN:  # Limit the minimum angle value
            angle = cfg.ANGLE_MIN
        return angle

    def set(self, servonum, servoangle):
        """
        Set the servo angle
        :param servonum: Servo number
        :param servoangle: Servo angle
        :return:
        """
        angle = self.angle_limit(servoangle)
        buf = [0xff, 0x01, servonum, angle, 0xff]
        try:
            i2c.writedata(i2c.mcu_address, buf)
        except Exception as e:
            print('servo write error:', e)

    def store(self):
        """
        Store the servo angle
        :return:
        """
        cfgparser.save_data("servo", "angle", cfg.ANGLE)

    def restore(self):
        """
        Restore the servo angle
        :return:
        """
        cfg.ANGLE = cfgparser.get_data("servo", "angle")
        for i in range(0, 8):
            cfg.SERVO_NUM = i + 1
            cfg.SERVO_ANGLE = cfg.ANGLE[i]
            self.set(i + 1, cfg.ANGLE[i])
