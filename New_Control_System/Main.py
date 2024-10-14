import time

from Servo import Servo


s = Servo(0x18, 0x04)
s.set_templates_for_protocol([0xff, 0x04, 8, 0xff], 2)
g = s.get_templates_for_protocol()
print(g)
while True:
    s.send_to_servo(90)
    print("work")
    time.sleep(1)

