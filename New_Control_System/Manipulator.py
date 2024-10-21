import math as mt
import time
from time import sleep
from Servo import Servo


class Manipulator():

    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.__s1 = Servo(0x18, 0x01)
        self.__s2 = Servo(0x18, 0x02)
        self.__s3 = Servo(0x18, 0x03)
        self.__s4 = Servo(0x18, 0x04)
        self.__s1.set_templates_for_protocol([0xff, 0x01, 1, 0xff], 3)
        self.__s2.set_templates_for_protocol([0xff, 0x01, 2, 0xff], 3)
        self.__s3.set_templates_for_protocol([0xff, 0x01, 3, 0xff], 3)
        self.__s4.set_templates_for_protocol([0xff, 0x01, 4, 0xff], 3)
        self.q1 = 140
        self.q2 = 30

    def get_coordinate(self, q1, q2):
        y = self.l1 + mt.sin(q1 * mt.pi / 180) * self.l2 + mt.sin(
            (q2 * mt.pi / 180) - mt.pi + (q1 * mt.pi / 180)) * self.l3
        x = self.l2 * mt.cos(q1 * mt.pi / 180) + self.l3 * mt.cos((q2 * mt.pi / 180) - mt.pi + (q1 * mt.pi / 180))

        self.q1 = q1
        self.q2 = q2

        return (x, y)

    def get_angles(self, x, y):
        d = mt.sqrt(x ** 2 + (y - self.l1) ** 2)
        q1 = mt.atan((y - self.l1) / x)
        q2 = mt.acos((d ** 2 + self.l2 ** 2 - self.l3 ** 2) / (2 * self.l2 * d))
        q3 = mt.acos((self.l2 ** 2 + self.l3 ** 2 - d ** 2) / (2 * self.l2 * self.l3))
        result1 = (q1 + q2) * 180 / mt.pi
        result2 = q3 * 180 / mt.pi

        return (result1, result2)

    def set_angle_servo_arm(self, q1, q2):
        self.__s1.send_to_servo(q1)
        self.__s2.send_to_servo(q2)

    def set_circle_arm(self, q3):
        self.__s3.send_to_servo(q3)

    def set_open_close_arm(self, q4):
        self.__s4.send_to_servo(q4)



    def take_object_return(self, x, y, q4, end_q1, end_q2):
        self.set_open_close_arm(45)
        angles = self.get_angles(x, y)
        self.set_angle_servo_arm(angles[0], angles[1])
        time.sleep(0.2)
        self.set_open_close_arm(q4)
        time.sleep(0.2)
        self.set_angle_servo_arm(end_q1, end_q2)
        time.sleep(0.2)
        return self.get_coordinate(end_q1, end_q2)


