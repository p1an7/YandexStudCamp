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
@Explain : Encapsulated configuration file
@contact :
@Time    :2020/05/09
@File    :xr_configparser.py
@Software: PyCharm
"""
from configparser import ConfigParser

class HandleConfig:
    """
    Encapsulation of configuration file read and write data
    """
    def __init__(self, filename):
        """
        :param filename: Configuration file name
        """
        self.filename = filename
        self.config = ConfigParser()        # Read configuration file 1. Create configuration parser
        self.config.read(self.filename, encoding="utf-8")   # Read configuration file 2. Specify the configuration file to read

    def save_data(self, group, key, data):
        if not self.config.has_section(group):  # Determine if the section exists
            self.config.add_section(group)      # If not, add it
        self.config.set(group, key, str(data))  # Modify section
        with open(self.filename, "w") as file:  # Save to which file filename=need to specify the file name
            self.config.write(file)

    def get_data(self, group, key):
        data = self.get_value(group, key)  # Read what content
        data = str(data)[1:-1].split(',')
        data = list(map(int, data))
        return data

    # get_value gets all strings, section area name, option name
    def get_value(self, section, option):
        return self.config.get(section, option)
