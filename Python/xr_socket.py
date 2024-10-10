# coding:utf-8
"""
Raspberry Pi WiFi Wireless Video Car Robot Driver Source Code
Author: Sence
Copyright: XiaoR Technology (Shenzhen XiaoR Technology Co., Ltd. www.xiao-r.com); WIFI Robot Forum www.wifi-robots.com
This code can be freely modified, but commercial use for profit is prohibited!
This code has been applied for software copyright protection, and legal action will be taken immediately upon discovery of infringement!
"""
"""
@version: python3.7
@Author  : xiaor
@Explain :socket data reception and transmission
@Time    :2020/05/09
@File    :xr_socket.py
@Software: PyCharm
"""
from builtins import range, str, eval, hex, int, object, type, abs, Exception, repr, bytes, len

import os
import time
import xr_config as cfg

from subprocess import call

from xr_motor import RobotDirection
go = RobotDirection()

from xr_servo import Servo
servo = Servo()

from xr_car_light import Car_light
car_light = Car_light()

from xr_music import Beep
beep = Beep()

class Socket:
    def __init__(self):
        self.rec_flag = 0  # 0xff byte reception flag
        self.count = 0  # Data reception counter flag
        self.client = None

    def sendbuf(self, buf):
        time.sleep(0.2)
        # print('TCP_CLIENT:%s++++++++BT_CLIENT:%s' % (cfg.TCP_CLIENT, cfg.BT_CLIENT))
        if cfg.TCP_CLIENT != False:
                try:
                    cfg.TCP_CLIENT.send(buf)
                    time.sleep(0.005)
                    print('tcp send ok!!!')
                except Exception as e:  # Send error
                    print('tcp send error:', e)  # Print error information

        if cfg.BT_CLIENT != False:
                try:
                    cfg.BT_CLIENT.send(buf)
                    time.sleep(0.005)
                    print('bluetooth send ok!!!')
                except Exception as e:  # Send error
                    print('bluetooth send error:', e)  # Print error information

    def load_server(self, server, servername):
        """
        Socket service function
        Parameters: self instance class, parameter server service to start, buf received data, servername service type name to start
        """
        while True:
            time.sleep(0.1)
            print("waiting for %s connection..." % servername, "\r")

            if servername == 'bluetooth':  # If bluetooth communication is selected
                cfg.BT_CLIENT = False		# Close the bluetooth service when starting the bluetooth service
                cfg.BT_CLIENT, socket_address = server.accept()  # Initialize socket and create a client and address
                client = cfg.BT_CLIENT
                time.sleep(0.1)
                print(str(socket_address[0]) + " %s connected!" % servername + "\r")  # Print client and address

            elif servername == 'tcp':  # If wifi communication is selected
                cfg.TCP_CLIENT = False	# Close the tcp service when starting the tcp service
                cfg.TCP_CLIENT, socket_address = server.accept()  # Initialize socket and create a client and address
                client = cfg.TCP_CLIENT
                time.sleep(0.1)
                print(str(socket_address[0]) + "%s connected!" % servername + "\r")  # Print client and address

            while True:
                try:
                    data = client.recv(cfg.RECV_LEN)  # cfg.RECV_LEN length of characters received at one time
                    #print(data)
                    if len(data) < cfg.RECV_LEN:  # Does not meet the reception length standard
                        #print('data len %d:'%len(data))
                        break
                    if data[0] == 0xff and data[len(data) - 1] == 0xff:  # If the header and tail of the packet are 0xff, it meets the XiaoR Technology communication protocol
                        buf = []  # Define a list
                        for i in range(1, 4):  # Get the middle 3 bits of data in the protocol packet
                            buf.append(data[i])  # Add data to buf
                        self.communication_decode(buf)  # Run serial port parsing data
                except Exception as e:  # Reception error
                    time.sleep(0.1)
                    print('socket received error:', e)  # Print error information

            client.close()		# Close the client
            client = None
            go.stop()
        go.stop()
        server.close()

    def communication_decode(self, buffer):
        """
        Data parsing function, parses the data filtered by socket, i.e., the XiaoR Technology communication protocol, into corresponding functions and actions according to the bits
        Protocol format---------------------0xff		0xXX		0xXX		0xXX		0xff
        Meaning----------------------------Header		Type bit	Control bit	Data bit		Tail
        Socket filtered data buffer[]---		   buffer[0]   buffer[1]   buffer[2]
        """
        print(buffer)
        if buffer[0] == 0x00:  # buffer[0] represents the type bit, equal to 0x00 indicates that this data packet is a motor control command data packet
            if buffer[1] == 0x01:  # buffer[1] represents the control bit, equal to 0x01 indicates a forward data packet
                if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:	# Judge whether the ultrasonic obstacle avoidance and infrared anti-drop status are obstacle-free or normal road surface without drop edges, these two flags default to 1, ensuring that it will not move forward if there are obstacles in front or if there are drop edges during anti-drop
                    go.forward()  # Move forward

            elif buffer[1] == 0x02:
                go.back()  # Move backward

            elif buffer[1] == 0x03:
                if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:
                    cfg.LIGHT_STATUS = cfg.TURN_LEFT
                    go.left()  # Turn left

            elif buffer[1] == 0x04:
                if cfg.AVOID_CHANGER == 1 and cfg.AVOIDDROP_CHANGER == 1:
                    cfg.LIGHT_STATUS = cfg.TURN_RIGHT
                    go.right()  # Turn right

            elif buffer[1] == 0x00:
                cfg.LIGHT_STATUS = cfg.STOP
                go.stop()  # Stop

            else:
                go.stop()

        elif buffer[0] == 0x01:  # Control servo command
            cfg.SERVO_NUM = buffer[1]  # Get servo number
            cfg.SERVO_ANGLE = buffer[2]  # Get servo angle
            if abs(cfg.SERVO_ANGLE - cfg.SERVO_ANGLE_LAST) > 2:  # Limit servo repeated angle commands
                cfg.ANGLE[cfg.SERVO_NUM-1] = cfg.SERVO_ANGLE
                servo.set(cfg.SERVO_NUM, cfg.SERVO_ANGLE)

        elif buffer[0] == 0x02:  # Adjust motor speed
            if buffer[1] == 0x01:  # Adjust left motor speed
                cfg.LEFT_SPEED = buffer[2]
                go.set_speed(1, cfg.LEFT_SPEED)	 # Set left speed
                go.save_speed()

            elif buffer[1] == 0x02:  # Adjust right motor speed
                cfg.RIGHT_SPEED = buffer[2]
                go.set_speed(2, cfg.RIGHT_SPEED)  # Set right speed
                go.save_speed()

        elif buffer[0] == 0x06:  # Set the color to follow in the color detection follow function
            if buffer[1] == 0x01:
                cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['red']		# Set the color detection color range to red
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['red'])	 # Set the car light to red, for indication
            elif buffer[1] == 0x02:
                cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['green']
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['green'])
            elif buffer[1] == 0x03:
                cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['blue']
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['blue'])
            elif buffer[1] == 0x04:
                cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['violet']
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['violet'])
            elif buffer[1] == 0x05:
                cfg.COLOR_INDEX = cfg.COLOR_FOLLOW_SET['orange']
                car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['orange'])
            time.sleep(1)

        elif buffer[0] == 0x13:
            if buffer[1] == 0x01 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['irfollow']  	 # Enter infrared follow mode

            elif buffer[1] == 0x02 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']: 	 # Enter infrared line tracking mode
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['trackline']

            elif buffer[1] == 0x03 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']: 	 # Enter infrared anti-drop mode
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['avoiddrop']

            elif buffer[1] == 0x04 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  	 # Enter ultrasonic obstacle avoidance mode
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['avoidbyragar']

            elif buffer[1] == 0x05 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:  	 # Enter ultrasonic distance app display
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['send_distance']

            elif buffer[1] == 0x06 and cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:		 # Enter ultrasonic maze walking
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                servo.set(1, 165)
                servo.set(2, 15)
                servo.set(3, 90)
                servo.set(4, 90)
                servo.set(7, 90)
                servo.set(8, 0)
                cfg.MAZE_TURN_TIME = buffer[2]*10
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['maze']

            elif buffer[1] == 0x07:
                cfg.PROGRAM_ABLE = True
                servo.set(1, 165)
                servo.set(2, 15)
                servo.set(3, 90)
                servo.set(4, 90)
                servo.set(7, 90)
                servo.set(8, 0)
                if buffer[2] == 0x00:  	 # Camera line tracking debug mode, i.e., normal video transmission mode
                    go.stop()  # Stop
                    cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # Reset the saved speed
                    cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
                    cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['camera_normal']
                    cfg.CRUISING_FLAG = cfg.CRUISING_SET['camera_normal']
                    car_light.set_ledgroup(cfg.CAR_LIGHT, 8, cfg.COLOR['black'])	 # Exiting color detection recognition follow mode requires turning off the car light

                elif buffer[2] == 0x01:  # Camera line tracking mode
                    cfg.PROGRAM_ABLE = False
                    cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                    cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED
                    cfg.CRUISING_FLAG = cfg.CRUISING_SET['camera_linepatrol']
                    cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['camera_linepatrol']
                    # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'	# Command to end camera video stream
                    #call("%s" % path_sh, shell=True)	 # Start shell command to end camera video stream, the camera will be used for line tracking using opencv
                    time.sleep(2)
            elif buffer[1] == 0x08:	 # Camera face detection follow mode
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['facefollow']
                cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['facefollow']
                # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Command to end camera video stream
                #call("%s" % path_sh, shell=True)  # Start shell command to end camera video stream, the camera will be used for face detection using opencv
                # try:
                # 	call("%s" % path_sh, shell=True)  # Start shell command to end camera video stream, the camera will be used for color detection using opencv
                # except Exception as e:
                # 	print(e.message)
                time.sleep(2)

            elif buffer[1] == 0x09:	 # Camera color detection follow mode
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['colorfollow']
                cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['colorfollow']
                # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Command to end camera video stream
                #call("%s" % path_sh, shell=True)  # Start shell command to end camera video stream, the camera will be used for color detection using opencv
                time.sleep(2)

            elif buffer[1] == 0x0A:	 # Camera QR code detection recognition
                cfg.LASRT_LEFT_SPEED = cfg.LEFT_SPEED  # Save the current speed
                cfg.LASRT_RIGHT_SPEED = cfg.RIGHT_SPEED

                cfg.CRUISING_FLAG = cfg.CRUISING_SET['qrcode_detection']
                cfg.CAMERA_MOD = cfg.CAMERA_MOD_SET['qrcode_detection']
                # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/stop_mjpg_streamer.sh &'  # Command to end camera video stream
                #call("%s" % path_sh, shell=True)  # Start shell command to end camera video stream, the camera will be used for color detection using opencv
                time.sleep(2)
            elif buffer[1] == 0x0B:  # light
                car_light.init_led()  # Car light show

            elif buffer[1] == 0x00:		# Normal mode
                cfg.PROGRAM_ABLE = True
                cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # Reset the saved speed
                cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
                cfg.AVOIDDROP_CHANGER = 1
                cfg.AVOID_CHANGER = 1
                cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']
                print("CRUISING_FLAG normal mode %d " % cfg.CRUISING_FLAG)

        elif buffer == [0x31, 0x00, 0x00]:  # Query power information
            buf = bytes([0xff, 0x31, 0x01, cfg.POWER, 0xff])
            self.sendbuf(buf)

        elif buffer[0] == 0x32:  # Store angle
            servo.store()

        elif buffer[0] == 0x33:  # Read angle
            servo.restore()

        elif buffer[0] == 0x40:  # Light mode switch FF040000FF turn on light  FF040100FF turn off light
            if buffer[1] == 0x00:
                car_light.open_light()  # Turn on all car lights, white
                cfg.LIGHT_OPEN_STATUS = 1
            elif buffer[1] == 0x01:
                car_light.close_light()  # Turn off all car lights, black
                cfg.LIGHT_OPEN_STATUS = 0
            else:
                lednum = buffer[1]  # Get light quantity command information
                ledcolor = buffer[2]  # Get light color command information

                if lednum < 10:  # Multi-light mode light up
                    car_light.set_ledgroup(cfg.CAR_LIGHT, lednum - 1, ledcolor)
                elif 9 < lednum < 18:  # Single-light mode light up
                    car_light.set_led(cfg.CAR_LIGHT, lednum - 9, ledcolor)

        elif buffer[0] == 0x41:
            if buffer[1] == 0x00:
                tune = buffer[2]
                cfg.TUNE = tune
            # beep.tone(beep.tone_all)
            elif buffer[1] == 0x01:  # Received is low pitch
                beet1 = buffer[2]
                beep.tone(beep.tone_all[cfg.TUNE][beet1 + 14], 0.5)
            elif buffer[1] == 0x02:  # Received is middle pitch
                beet2 = buffer[2]
                beep.tone(beep.tone_all[cfg.TUNE][beet2], 0.5)
            elif buffer[1] == 0x03:  # Received is high pitch
                beet3 = buffer[2]
                beep.tone(beep.tone_all[cfg.TUNE][beet3 + 7], 0.5)

        elif buffer == [0xef, 0xef, 0xee]:
            print("Heartbeat Packet!")

        elif buffer[0] == 0xfc:  # FFFC0000FF  shutdown
            os.system("sudo shutdown -h now")

        else:
            print("error command!")

    def bluetooth_server(self):
        """
        Start bluetooth reception service
        Parameters: The first parameter represents the service to start, the second parameter represents the service name to start
        """
        # print("load bluetooth_server")
        self.load_server(cfg.BT_SERVER, 'bluetooth')

    def tcp_server(self):
        """
        Start tcp reception service
        Parameters: The first parameter represents the service to start, the second parameter represents the service name to start
        """
        # print("load tcp_server")
        self.load_server(cfg.TCP_SERVER, 'tcp')
