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
@Explain : Car battery information
@Time    : 2020/05/09
@File    : xr_power.py
@Software: PyCharm
"""

import time
from builtins import hex, bytes
from xr_i2c import I2c
from xr_car_light import Car_light
import xr_config as cfg

i2c = I2c()
rgb = Car_light()

class Power():
    def __init__(self):
        pass

    def got_vol(self):
        """
        Get battery voltage information
        :return:
        """
        time.sleep(0.005)
        vol_H = i2c.readdata(i2c.mcu_address, 0x05)  # Read the high 8 bits of the battery voltage value measured by the MCU
        if vol_H == None:
            vol_H = 0
        time.sleep(0.005)
        vol_L = i2c.readdata(i2c.mcu_address, 0x06)  # Read the low 8 bits of the battery voltage value measured by the MCU
        if vol_L == None:
            vol_L = 0
        vol = (vol_H << 8) + vol_L  # Combine the high 8 bits and the low 8 bits, the battery voltage is amplified by 100 times
        return vol  # Return battery voltage

    def show_vol(self):
        """
        RGB light battery display
        :return:
        """
        vol = self.got_vol()
        if (370 < vol < 430) or (760 < vol < 860) or (1120 < vol < 1290):  # 70-100%  8 LEDs green
            rgb.set_ledgroup(cfg.POWER_LIGHT, 8, cfg.COLOR['green'])  # Set the battery light bar to green
            cfg.POWER = 3  # Set the battery level to the highest level 3
        elif (350 < vol < 370) or (720 < vol < 770) or (1080 < vol < 1120):  # 30-70% 6 LEDs orange
            rgb.set_ledgroup(cfg.POWER_LIGHT, 6, cfg.COLOR['orange'])
            cfg.POWER = 2  # Set the battery level to 2
        elif (340 < vol < 350) or (680 < vol < 730) or (1040 < vol < 1080):  # 10-30% 2 LEDs red
            rgb.set_ledgroup(cfg.POWER_LIGHT, 2, cfg.COLOR['red'])
            cfg.POWER = 1  # Set the battery level to 1
        elif (vol < 340) or (vol < 680) or (vol < 1040):  # <10% 1 LED red
            rgb.set_ledgroup(cfg.POWER_LIGHT, 1, cfg.COLOR['red'])
            cfg.POWER = 0  # Set the battery level to 0
