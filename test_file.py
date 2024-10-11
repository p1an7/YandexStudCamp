import smbus
import time

bus = smbus.SMBus(1)

servo_address_1 = 0x18
#servo_address_2 = 0x19


def set_servo_angle(address, angle):
    value = int(angle / 180.0 * 255)
    buf = [0xff, 0x08, 8, value, 0xff]
    bus.write_i2c_block_data(address, buf[0], buf[1:len(buf)])


try:
    while True:

        set_servo_angle(servo_address_1, 56)
        print("Work")
        #set_servo_angle(servo_address_2, 45)

        time.sleep(1)

except KeyboardInterrupt:
    print("Программа завершена")
