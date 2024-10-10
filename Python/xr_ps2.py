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
@Explain : PS2 controller module
@Time    : 2020/05/09
@File    : xr_ps2.py
@Software: PyCharm
"""
import time
import xr_config as cfg
from xr_i2c import I2c

i2c = I2c()

from xr_motor import RobotDirection

go = RobotDirection()

from xr_servo import Servo
servo = Servo()

class PS2(object):
    def __init__(self):
        pass

    def ps2_button(self):
        """
        Get the button value of the PS2 controller
        :return: cfg.PS2_READ_KEY parsed button value
        """
        ps2check = i2c.readdata(i2c.ps2_address, 0x01)  # Get the mode value returned by PS2
        read_key = i2c.readdata(i2c.ps2_address, 0x03)  # Get the button value returned by PS2
        read_key1 = i2c.readdata(i2c.ps2_address, 0x04)  # Get the button value returned by PS2
        cfg.PS2_READ_KEY = 0
        if ps2check == 0x41 or ps2check == 0xC1 or ps2check == 0x73 or ps2check == 0xF3:  # PS2 normal mode
            if read_key == 0xef:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_UP']
            elif read_key == 0xbf:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_DOWN']
            elif read_key == 0xcf:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_LEFT']
            elif read_key == 0xdf:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PAD_RIGHT']
            elif read_key1 == 0xef:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_BLUE']
            elif read_key1 == 0xbf:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_GREEN']
            elif read_key1 == 0xcf:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_RED']
            elif read_key1 == 0xdf:
                cfg.PS2_READ_KEY = cfg.PS2_KEY['PSB_PINK']
        return cfg.PS2_READ_KEY

    def control(self):
        """
        PS2 controller control function
        :return:
        """

        read_ps2 = self.ps2_button()  # Get button value
        add = 5
        if cfg.PS2_LASTKEY != read_ps2 and cfg.PS2_LASTKEY != 0:  # If the previous value is not 0 and not equal to the current value, the button value has changed and is not 0
            go.stop()  # Execute stop once when the button value changes
            cfg.LIGHT_STATUS = cfg.STOP  # Set the button status to stop
            cfg.PS2_LASTKEY = 0  # Assign the previous status a value of 0 to avoid stopping again

        else:
            if read_ps2 == cfg.PS2_KEY['PSB_PAD_UP']:  # Equal to the left button up
                go.forward()
                time.sleep(0.02)
                cfg.PS2_LASTKEY = read_ps2  # Update the previous value

            elif read_ps2 == cfg.PS2_KEY['PSB_PAD_DOWN']:  # Equal to the left button down
                go.back()
                time.sleep(0.02)
                cfg.PS2_LASTKEY = read_ps2

            elif read_ps2 == cfg.PS2_KEY['PSB_PAD_LEFT']:  # Equal to the left button left
                go.left()
                cfg.LIGHT_STATUS = cfg.TURN_LEFT
                time.sleep(0.02)
                cfg.PS2_LASTKEY = read_ps2

            elif read_ps2 == cfg.PS2_KEY['PSB_PAD_RIGHT']:  # Equal to the left button right
                go.right()
                cfg.LIGHT_STATUS = cfg.TURN_RIGHT
                time.sleep(0.02)
                cfg.PS2_LASTKEY = read_ps2

            if read_ps2 == cfg.PS2_KEY['PSB_RED']:  # Equal to the red button
                if (cfg.ANGLE[6] - add) < 180:
                    cfg.ANGLE[6] = cfg.ANGLE[6] + add
                else:
                    cfg.ANGLE[6] = 180
                servo.set(7, cfg.ANGLE[6])

            elif read_ps2 == cfg.PS2_KEY['PSB_PINK']:  # Equal to the pink button
                if (cfg.ANGLE[6] - add) > 0:
                    cfg.ANGLE[6] = cfg.ANGLE[6] - add
                else:
                    cfg.ANGLE[6] = 0
                servo.set(7, cfg.ANGLE[6])

            elif read_ps2 == cfg.PS2_KEY['PSB_GREEN']:  # Equal to the green button
                if (cfg.ANGLE[7] - add) < 155:
                    cfg.ANGLE[7] = cfg.ANGLE[7] + add
                else:
                    cfg.ANGLE[7] = 155
                servo.set(8, cfg.ANGLE[7])

            elif read_ps2 == cfg.PS2_KEY['PSB_BLUE']:  # Equal to the blue button
                if (cfg.ANGLE[7] - add) > 0:
                    cfg.ANGLE[7] = cfg.ANGLE[7] - add
                else:
                    cfg.ANGLE[7] = 0
                servo.set(8, cfg.ANGLE[7])
