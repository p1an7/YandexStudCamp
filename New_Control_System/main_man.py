from Manipulator import Manipulator
from Sensors import Ultrasonic

u_s = Ultrasonic()
manipulator = Manipulator(55, 95, 120)
r = u_s.get_distance()
r = r * 10 + 40
angles = manipulator.get_angles(r, -10)
manipulator.set_angle_servo_arm(angles[0], angles[1])
