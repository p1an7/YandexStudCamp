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
@Explain : Voice module
@Time    : 2020/05/09
@File    : xr_voice.py
@Software: PyCharm
"""
import serial
import time
import xr_config as cfg

class Voice(object):
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyS0", 9600)
        pass

    def run(self):
        while True:
            while self.ser.inWaiting() > 0:
                time.sleep(0.05)
                n = self.ser.inWaiting()
                myout = self.ser.read(n)
                self.get_voice(myout)
                dat = int.from_bytes(myout, byteorder='big')
                print('%#x' % dat)

            time.sleep(0.5)

    def get_voice(self, data):
        cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        if len(data) < cfg.RECV_LEN:  # Does not meet the reception length standard
            # print('data len %d:'%len(data))
            return cfg.VOICE_MOD
        if data[0] == 0xff and data[len(data) - 1] == 0xff:  # If the header and tail of the packet are 0xff, it meets the XiaoR Technology communication protocol
            buf = []  # Define a list
            for i in range(1, 4):  # Get the middle 3 bits of data in the protocol packet
                buf.append(data[i])  # Add data to buf
            if buf[0] == 0xf5 and buf[1] == 0x01:
                if buf[2] == 0x01:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
                elif buf[2] == 0x02:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['openlight']
                elif buf[2] == 0x03:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['closelight']
                elif buf[2] == 0x06:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['forward']
                elif buf[2] == 0x07:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['back']
                elif buf[2] == 0x08:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['left']
                elif buf[2] == 0x09:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['right']
                elif buf[2] == 0x0A:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['stop']
                elif buf[2] == 0x0B:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['nodhead']
                elif buf[2] == 0x0C:
                    cfg.VOICE_MOD = cfg.VOICE_MOD_SET['shakehead']
        return cfg.VOICE_MOD

if __name__ == "__main__":
    ser = Voice()
    while True:
        print("run voice ctl")
        ser.run()
