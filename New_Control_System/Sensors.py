import GPIO as gpio
import Config as cfg

from Movement import RobotDirection

go = RobotDirection()

class Sensors(object):
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
        if (gpio.digital_read(gpio.IR_L) == 0) and (gpio.digital_read(gpio.IR_R) == 0):  # Black line is high, ground is low
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
        if (gpio.digital_read(gpio.IRF_L) == 0 and gpio.digital_read(gpio.IRF_R) == 0 and gpio.digital_read(gpio.IR_M) == 1):
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
            elif (gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 1) or (gpio.digital_read(gpio.IRF_L) == 1 and gpio.digital_read(gpio.IRF_R) == 1):
                cfg.LEFT_SPEED = 50
                cfg.RIGHT_SPEED = 50
                go.forward()  # Forward: Only the middle sensor detects an obstacle

    def avoiddrop(self):
        """
        Infrared anti-drop
        """
        cfg.LEFT_SPEED = 25
        cfg.RIGHT_SPEED = 25
        if (gpio.digital_read(gpio.IR_L) == 0) and (gpio.digital_read(gpio.IR_R) == 0):  # When both infrared sensors detect the ground
            cfg.AVOIDDROP_CHANGER = 1  # Set the flag to 1, the serial port parsing direction judges this flag
        else:
            if cfg.AVOIDDROP_CHANGER == 1:  # Only when the previous state is normal will the stop be executed, avoiding repeated execution of the stop and unable to proceed with remote control
                go.stop()
                cfg.AVOIDDROP_CHANGER = 0
