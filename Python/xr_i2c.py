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
@Explain : i2c
@contact :
@Time    :2020/05/09
@File    :xr_i2c.py
@Software: PyCharm
"""
import os
import time
from builtins import IOError, object, len

import smbus

# # smbus
# self.device = smbus.SMBus(1)  # 0 represents /dev/i2c0, 1 represents /dev/i2c1
# # I2C communication address
# address = 0x18

class I2c(object):
    def __init__(self):
        self.mcu_address = 0x18
        self.ps2_address = 0x19
        self.device = smbus.SMBus(1)
        pass

    def writedata(self, address, values):
        """
        # Write command to I2C address
        """
        try:
            self.device.write_i2c_block_data(address, values[0],
                                             values[1:len(values)])  # Continuous write, first parameter: device address, second parameter: write register address,
            # Xiaor's MCU does not have a register address, so the first frame of data is written, third parameter: data to be written
            time.sleep(0.005)
        except Exception as e:  # Write error
            pass
            # print('i2c write error:', e)
            # os.system('sudo i2cdetect -y 1')

    def readdata(self, address, index):
        """
        # Read one byte of data from I2C
        """
        try:
            value = self.device.read_byte_data(address, index)  # Read one byte from the slave device offset index
            time.sleep(0.005)
            return value  # Return the read data
        except Exception as e:  # Read error
            pass
            # print('i2c read error:', e)
            # os.system('sudo i2cdetect -y 1')
