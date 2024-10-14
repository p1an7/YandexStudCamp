import smbus
import time

class Servo:
    def __init__(self, address_to_send_bus, address_in_sendbus, smbus_num=1):
        self.bus = smbus.SMBus(smbus_num)
        self.address_to_send_bus = address_to_send_bus
        self.address_in_sendbus = address_in_sendbus
        self.templates_for_protocol = []
        self.value = 0

    def set_for_address_send_bus(self, address_send_bus):
        self.address_to_send_bus = address_send_bus

    def set_address_in_sendbus(self, address_in_sendbus):
        self.address_in_sendbus = address_in_sendbus

    def set_templates_for_protocol(self, template, position):
        # Example [0xff, 0x08, 8, 0xff] And in what position must be angle
        template.insert(position, self.value)
        self.templates_for_protocol = template
        print(self.templates_for_protocol)

    def get_for_address_send_bus(self):
        return self.address_to_send_bus

    def get_address_in_sendbus(self):
        return self.address_in_sendbus

    def get_templates_for_protocol(self):
        return self.templates_for_protocol

    def send_to_servo(self, angle):
        self.value = int(angle / 180.0 * 255)
        buf = self.templates_for_protocol
        self.bus.write_i2c_block_data(self.address_to_send_bus, buf[0], buf[1: len(buf)])
