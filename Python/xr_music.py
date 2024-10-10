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
@Explain : Buzzer sound
@contact :
@Time    : 2020/05/09
@File    : xr_music.py
@Software: PyCharm
"""
import time
from builtins import range, object, len, int

import xr_gpio as gpio
import xr_config as cfg

class Beep(object):
    def __init__(self):
        # High tones
        self.H1 = 8
        self.H2 = 9
        self.H3 = 10
        self.H4 = 11
        self.H5 = 12
        self.H6 = 13
        self.H7 = 14
        # Low tones
        self.L1 = 15
        self.L2 = 16
        self.L3 = 17
        self.L4 = 18
        self.L5 = 19
        self.L6 = 20
        self.L7 = 21
        # Middle tones
        self.C = 0
        self.D = 1
        self.E = 2
        self.F = 3
        self.G = 4
        self.A = 5
        self.B = 6

        self.tone_all = [
            # '''
            # 2D array [x][y], x represents the pitch, y represents the specific frequency of the note in the pitch
            # '''
            # C key
            [1000,  # 0    Empty sound
             262, 294, 330, 350, 393, 441, 495,     # 1-7   Middle tones
             525, 589, 661, 700, 786, 882, 990,     # H1-H7 High tones
             131, 147, 165, 175, 196, 221, 248      # L1-L7 Low tones
            ],
            # D key
            [1000,  # 0    Empty sound
             294, 330, 350, 393, 441, 495, 556,     # 1-7   Middle tones
             589, 661, 700, 786, 882, 990, 1112,    # 8-14  High tones
             147, 165, 175, 196, 221, 248, 278      # 15-21 Low tones
            ],
            # E key
            [1000,  # 0    Empty sound
             330, 350, 393, 441, 495, 556, 624,     # 1-7   Middle tones
             661, 700, 786, 882, 990, 1112, 1248,    # 8-14  High tones
             165, 175, 196, 221, 248, 278, 312       # 15-21 Low tones
            ],
            # F key
            [1000,  # 0    Empty sound
             350, 393, 441, 495, 556, 624, 661,     # 1-7   Middle tones
             700, 786, 882, 935, 1049, 1178, 1322,  # 8-14  High tones
             175, 196, 221, 234, 262, 294, 330      # 15-21 Low tones
            ],
            # G key
            [1000,  # 0    Empty sound
             393, 441, 495, 556, 624, 661, 742,     # 1-7   Middle tones
             786, 882, 990, 1049, 1178, 1322, 1484, # 8-14  High tones
             196, 221, 234, 262, 294, 330, 371      # 15-21 Low tones
            ],
            # A key
            [1000,  # 0    Empty sound
             441, 495, 556, 589, 661, 742, 833,     # 1-7   Middle tones
             882, 990, 1112, 1178, 1322, 1484, 1665,# 8-14  High tones
             221, 248, 278, 294, 330, 371, 416      # 15-21 Low tones
            ],
            # B key
            [1000,  # 0    Empty sound
             495, 556, 624, 661, 742, 833, 935,     # 1-7   Middle tones
             990, 1112, 1178, 1322, 1484, 1665, 1869,# 8-14  High tones
             248, 278, 294, 330, 371, 416, 467      # 15-21 Low tones
            ]
        ]
        # Birthday song notes
        self.melody_Happy_birthday = [5, 5,
                                      6, 5, self.H1, 7, 5, 5, 6, 5, self.H2, self.H1, 5, 5, self.H5, self.H3, self.H1,
                                      7, 6,
                                      0, 0, self.H4, self.H4, self.H3, self.H1, self.H2, self.H1]
        # Birthday song rhythm
        self.beet_Happy_birthday = [0.5, 0.5,
                                    1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 2, 0.5, 0.5, 1, 1, 1, 1, 2,
                                    0.5, 0.5, 0.5, 0.5, 1, 1, 1, 2]

        pass

    def tone(self, tune, beet):
        '''
        Play the note and corresponding rhythm
        :param pin: Pin
        :param tune: Melody
        :param beet: Rhythm
        :return:
        '''
        tim = 500000 / tune
        duration_count = beet * 60 * tune / cfg.BEET_SPEED / cfg.CLAPPER
        for i in range(int(duration_count)):
            if tune != 1000:
                gpio.digital_write(gpio.BUZZER, False)
                time.sleep(tim / 500000)
                gpio.digital_write(gpio.BUZZER, True)
                time.sleep(tim / 500000)
            else:
                time.sleep(0.001)

    def play_music(self, major, melody, beet):
        '''
        :param melody: Music score
        :param beet: Rhythm
        :return:
        '''
        length = len(melody)
        for i in range(length):
            tone_act = self.tone_all[major][melody[i]]
            self.tone(tone_act, beet[i])
