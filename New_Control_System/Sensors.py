import GPIO as gpio
import Config as cfg
from builtins import int, chr, object
from Movement import Movement
import time

go = Movement()


class InfraRed(object):
    def __init__(self):
        pass

    def trackline(self):
        """
        Infrared line tracking
        """
        cfg.LEFT_SPEED = 30
        cfg.RIGHT_SPEED = 30
        # print('ir_trackline run...')
        # If neither side detects a black line
        if (gpio.digital_read(gpio.IR_L) == 0) and (
                gpio.digital_read(gpio.IR_R) == 0):  # Black line is high, ground is low
            go.forward()
        # If the right infrared sensor detects a black line
        elif (gpio.digital_read(gpio.IR_L) == 0) and (gpio.digital_read(gpio.IR_R) == 1):
            go.right()
        # If the left sensor detects a black line
        elif (gpio.digital_read(gpio.IR_L) == 1) and (gpio.digital_read(gpio.IR_R) == 0):
            go.left()
        # If both sides detect a black line
        elif (gpio.digital_read(gpio.IR_L) == 1) and (gpio.digital_read(gpio.IR_R) == 1):
            go.stop()

    def infrastatus_Midle(self):
        status_Midle = gpio.digital_read(gpio.IR_M)
        print(status_Midle)

    def infrastatus_Left(self):
        status_Left = gpio.digital_read(gpio.IR_L)
        print(status_Left)

    def infrastatus_Right(self):
        status_Right = gpio.digital_read(gpio.IR_R)
        print(status_Right)

    def irfollow(self):
        """
        Infrared following
        """
        cfg.LEFT_SPEED = 30
        cfg.RIGHT_SPEED = 30
        if (gpio.digital_read(gpio.IRF_L) == 0 and gpio.digital_read(gpio.IRF_R) == 0 and gpio.digital_read(
                gpio.IR_M) == 1):
            go.stop()  # Stop: Left and right detect obstacles or all do not detect obstacles
        else:
            if gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 0:
                cfg.LEFT_SPEED = 50
                cfg.RIGHT_SPEED = 50
                go.right()  # Left sensor does not detect an obstacle + right sensor detects an obstacle
            elif gpio.digital_read(gpio.IRF_L) == 0 and gpio.digital_read(gpio.IRF_R) == 1:
                cfg.LEFT_SPEED = 50
                cfg.RIGHT_SPEED = 50
                go.left()  # Left sensor detects an obstacle + right sensor does not detect an obstacle
            elif (gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 1) or (
                    gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 1):
                cfg.LEFT_SPEED = 50
                cfg.RIGHT_SPEED = 50
                go.forward()  # Forward: Only the middle sensor detects an obstacle

    def avoiddrop(self):
        """
        Infrared anti-drop
        """
        cfg.LEFT_SPEED = 25
        cfg.RIGHT_SPEED = 25
        if (gpio.digital_read(gpio.IR_L) == 0) and (
                gpio.digital_read(gpio.IR_R) == 0):  # When both infrared sensors detect the ground
            cfg.AVOIDDROP_CHANGER = 1  # Set the flag to 1, the serial port parsing direction judges this flag
        else:
            if cfg.AVOIDDROP_CHANGER == 1:  # Only when the previous state is normal will the stop be executed, avoiding repeated execution of the stop and unable to proceed with remote control
                go.stop()
                cfg.AVOIDDROP_CHANGER = 0

    def stop(self):
        go.stop()


class Ultrasonic(object):
    def __init__(self):
        self.MAZE_ABLE = 0
        self.MAZE_CNT = 0
        self.MAZE_TURN_TIME = 0
        self.dis = 0
        self.s_L = 0
        self.s_R = 0

    def get_distance(self):
        """
        Function to get ultrasonic distance, returns distance in cm
        """
        time_count = 0
        time.sleep(0.01)
        gpio.digital_write(gpio.TRIG, True)  # Pull up the ultrasonic Trig pin
        time.sleep(0.000015)  # Send a high-level pulse wave of more than 10um
        gpio.digital_write(gpio.TRIG, False)  # Pull down
        while not gpio.digital_read(gpio.ECHO):  # Wait for the Echo pin to change from low to high
            pass
        t1 = time.time()  # Record the start time of the Echo pin high level
        while gpio.digital_read(gpio.ECHO):  # Wait for the Echo pin to change from high to low
            if time_count < 2000:  # Timeout detection to prevent infinite loop
                time_count = time_count + 1
                time.sleep(0.000001)
                pass
            else:
                print("NO ECHO receive! Please check connection")
                break
        t2 = time.time()  # Record the end time of the Echo pin high level
        distance = (t2 - t1) * 340 / 2 * 100  # The duration of the Echo pin high level is the time for the ultrasonic
        # wave to travel from transmission to return, i.e., the distance value of the ultrasonic wave from the object

        # t2-t1 time unit s, sound speed 340m/s, x100 converts the distance value unit from m to cm
        # print("distance is %d" % distance)  # Print distance value
        if distance < 500:  # Normal detection distance value
            # print("distance is %d"%distance)
            cfg.DISTANCE = round(distance, 2)
            return cfg.DISTANCE
        else:
            # print("distance is 0")  # If the distance value is greater than 5m, it is out of the detection range
            cfg.DISTANCE = 0
            return 0
