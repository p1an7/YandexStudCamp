import smbus
import time

bus = smbus.SMBus(1)

servo_address_1 = 0x18
servo_address_2 = 0x19


def set_servo_angle(address, angle):
    value = int(angle / 180.0 * 255)
    buf = [0xff, 0x01, 0x05, value, 0xff]
    bus.write_i2c_block_data(address, buf[0], buf[1:len(buf)])
    return buf


try:
    while True:
        testbuf = []
        testbuf = set_servo_angle(servo_address_2, 30)
        # set_servo_angle(servo_address_1, 45)
        print("Work")
        print(testbuf)
        set_servo_angle(servo_address_1, 70)
        # set_servo_angle(servo_address_2, 30)
        time.sleep(1)

except KeyboardInterrupt:
    print("Программа завершена")