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
@Explain : OLED panel display
@contact :
@Time    : 2020/05/09
@File    : xr_oled.py
@Software: PyCharm
"""
import time
import os
import subprocess
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from xr_ultrasonic import Ultrasonic

ultrasonic = Ultrasonic()

import xr_config as cfg

class Oled():
    def __init__(self):
        # Get OLED instance
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)
        # Initialize, clear screen
        self.disp.begin()
        self.disp.clear()
        self.disp.display()

        # Create a new image with the size of the OLED
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))

        # Load the image into the drawing object, equivalent to loading it onto the canvas
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw some shapes.
        # First define some constants to allow easy resizing of shapes.
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height - self.padding
        # Move left to right keeping track of the current x position for drawing shapes.

        # Font selection
        # Default font in the library, in ImageFont
        self.font = ImageFont.load_default()
        # Font library on the Raspberry Pi, can set font size
        self.font1 = ImageFont.truetype('/home/pi/work/python_src/simhei.ttf', 14)
        pass

    def cpu_temp(self):
        '''
        Get Raspberry Pi temperature
        '''
        # Raspberry Pi CPU temperature is stored in this file, open the file
        tempFile = open('/sys/class/thermal/thermal_zone0/temp')
        # Read the file
        cputemp = tempFile.read()
        # Close the file
        tempFile.close()
        # Round to the nearest integer
        tem = round(float(cputemp) / 1000, 1)
        return str(tem)

    def get_network_interface_state(self, interface):
        '''
        Get the network interface connection status, returns 'up' if connected, otherwise returns 'down'
        '''
        return subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[:-1]

    def get_ip_address(self, interface):
        '''
        Get network IP address
        '''
        if self.get_network_interface_state(interface) == 'down':  # Check if connected
            return None
        cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface  # Match the IP information output by the corresponding network card
        return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

    def get_ip_address_wlan(self, interface):
        '''
        Get network IP address
        '''
        if self.get_network_interface_state(interface) == 'down':  # Check if connected
            return None
        cmd = "ip a show dev %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | grep -v '169'"  % interface  # Match the IP information output by the corresponding network card
        return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

    def draw_row_column(self, row, column, strs):
        '''
        Row display, row represents the row number, column represents the column number, strs represents the string to be displayed
        '''
        if row == 1:
            self.draw.text((column, self.top), strs, font=self.font, fill=255)
        elif row == 2:
            self.draw.text((column, self.top + 8), strs, font=self.font, fill=255)
        elif row == 3:
            self.draw.text((column, self.top + 16), strs, font=self.font, fill=255)
        elif row == 4:
            self.draw.text((column, self.top + 25), strs, font=self.font, fill=255)

    def disp_default(self):
        '''
        Display basic information after startup, the first row displays the IP of the wired network port
        The second row displays the IP of the wireless network port
        The third row displays memory usage information and usage rate
        The fourth row displays SD card storage information and usage rate
        '''
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.1f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True)
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell=True)

        # Write two lines of text.
        self.draw_row_column(1, 0, "eth0: " + str(self.get_ip_address('eth0')))
        self.draw_row_column(2, 0, "wlan0: " + str(self.get_ip_address('wlan0')))
        self.draw_row_column(3, 0, str(MemUsage.decode('utf-8')))
        self.draw_row_column(4, 0, str(Disk.decode('utf-8')))

        # Display image.
        self.disp.image(self.image)
        self.disp.display()
        time.sleep(0.1)

    def disp_cruising_mode(self):
        '''
        Display mode after entering control function
        :return: none
        '''
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        dispmod = cfg.OLED_DISP_MOD[cfg.CRUISING_FLAG]  # Display the corresponding mode based on the selected mode
        dispmodlength = len(dispmod) * cfg.OLED_DISP_MOD_SIZE  # Get the length of the string
        positionmod = (128 - dispmodlength) / 2 - 1  # Starting position of the character display

        self.draw.text((0, -2), cfg.LOGO, font=self.font, fill=255)  # Display LOGO information
        for line in os.popen("ifconfig wlan0 | awk  '/ether/{print $2 ;exit}' |sed 's/\://g'"):  # Get the MAC address of wlan0
            mac = (line[6:12])  # Take the last 6 digits of the MAC address
            mac = 'id:' + mac
        self.draw.text((74, 8), mac, font=self.font, fill=255)  # Display the last 4 digits of the MAC address
        self.draw.text((0, 8), "Dis:" + str(cfg.DISTANCE) + "cm", font=self.font, fill=255)  # Display distance value
        #self.draw.text((positionmod, 17), dispmod, font=self.font1, fill=255)  # Display mode

        self.draw.line((0, 8, 128, 8), fill=255)  # Horizontal line

        # Draw battery frame
        m = 3  # Number of battery levels
        n = 3  # Pixels per battery level
        batlength = m * n + 2 + 2 + 2  # m*n represents the pixels occupied by the battery core, the first 2 represents the distance from the battery frame to the head and tail of the battery core, the second 2 represents the pixels at the head and tail of the battery frame, the third 2 represents the pixels of the battery head
        x = 128 - batlength - 1  # Starting position of the left side of the battery frame
        y = 0  # Starting position of the top of the battery frame

        # Draw battery frame
        self.draw.line((x, y + 2, x + 2, y + 2), fill=255)
        self.draw.line((x + 2, y + 2, x + 2, y), fill=255)
        self.draw.line((x + 2, y, x + batlength, y), fill=255)
        self.draw.line((x + batlength, y, x + batlength, y + 5), fill=255)
        self.draw.line((x + batlength, y + 5, x + 2, y + 5), fill=255)
        self.draw.line((x + 2, y + 5, x + 2, y + 3), fill=255)
        self.draw.line((x + 2, y + 3, x, y + 3), fill=255)
        self.draw.line((x, y + 3, x, y + 2), fill=255)
        # Calculate battery level
        level = cfg.POWER
        # Clear battery level
        self.draw.line((x + 3, y + 2, x + batlength - 2, y + 2), fill=0)
        self.draw.line((x + 3, y + 3, x + batlength - 2, y + 3), fill=0)
        # Redraw battery level based on the obtained battery level value
        self.draw.line((x + batlength - 2 - level * n, y + 2, x + batlength - 2, y + 2), fill=255)
        self.draw.line((x + batlength - 2 - level * n, y + 3, x + batlength - 2, y + 3), fill=255)
        # Display image information on the OLED
        ip_address = self.get_ip_address_wlan('wlan0').split("\n")
        #print(ip_address)
        for idx, ip in enumerate(ip_address):
            self.draw_row_column(idx+3,0, "wlan:" + str(ip))
        self.disp.image(self.image)
        self.disp.display()
        time.sleep(0.05)
