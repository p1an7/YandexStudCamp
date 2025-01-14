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
@Explain : PID adjustment
@Time    : 2020/05/09
@File    : xr_pid.py
@Software: PyCharm
"""
import time

class PID:
    def __init__(self, P=0.2, I=0.0, D=0.0):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.sample_time = 0.00
        self.current_time = time.time()
        self.last_time = self.current_time

        self.point = 160
        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.error = 0.0
        self.last_error = 0.0
        self.delta_error = 0.0
        self.int_error = 0.0
        self.windup_guard = 20.0
        self.output = 0.0

    def update(self, feedback_value):
        self.error = self.point - feedback_value
        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        self.delta_error = self.error - self.last_error

        if delta_time >= self.sample_time:
            self.PTerm = self.Kp * self.error  # Proportional
            self.ITerm += self.error * delta_time  # Integral
            if self.ITerm < - self.windup_guard:
                self.ITerm = - self.windup_guard
            elif self.ITerm > self.windup_guard:
                self.ITerm = self.windup_guard
            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = self.delta_error / delta_time
            self.last_time = self.current_time
            self.last_error = self.error
            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setPoint(self, point_gain):
        self.point = point_gain

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time
