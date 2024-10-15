ир # coding:utf-8
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
@Explain :Main thread
@Time    :2020/05/09
@File    :xr_startmain.py
@Software: PyCharm
"""
from builtins import bytes, int

import os
import time
import threading
from threading import Timer
from subprocess import call
from xr_car_light import Car_light
car_light = Car_light()
import xr_config as cfg
from xr_motor import RobotDirection
go = RobotDirection()
from xr_socket import Socket
socket = Socket()
from xr_infrared import Infrared
infrared = Infrared()
from xr_ultrasonic import Ultrasonic
ultrasonic = Ultrasonic()
from xr_camera import Camera
camera = Camera()
from xr_function import Function
function = Function()
from xr_oled import Oled
try:
    oled = Oled()
except:
    print('oled initialization fail')
from xr_music import Beep
beep = Beep()
from xr_power import Power
power = Power()
from xr_servo import Servo
servo = Servo()
from xr_ps2 import PS2
ps2 = PS2()
from xr_i2c import I2c
i2c = I2c()
from xr_voice import Voice
voice = Voice()

def cruising_mode():
    """
    Mode switching function
    :return:none
    """
    # print('pre_CRUISING_FLAG：{}'.format(cfg.PRE_CRUISING_FLAG))
    time.sleep(0.001)
    if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_FLAG:  # If the loop mode changes
        cfg.LEFT_SPEED = cfg.LASRT_LEFT_SPEED  # When switching to other modes, restore the previously saved speed value
        cfg.RIGHT_SPEED = cfg.LASRT_RIGHT_SPEED
        if cfg.PRE_CRUISING_FLAG != cfg.CRUISING_SET['normal']:	 # If the loop mode changes and the previous mode is not normal
            go.stop()	  # Stop the car first
        cfg.PRE_CRUISING_FLAG = cfg.CRUISING_FLAG	 # Reassign the previous mode flag

    if cfg.CRUISING_FLAG == cfg.CRUISING_SET['irfollow']:  # Enter infrared follow mode
        # print("Infrared.irfollow")
        infrared.irfollow()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['trackline']:  # Enter infrared line tracking mode
        # print("Infrared.trackline")
        infrared.trackline()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['avoiddrop']:  # Enter infrared anti-drop mode
        # print("Infrared.avoiddrop")
        infrared.avoiddrop()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['avoidbyragar']:  # Enter ultrasonic obstacle avoidance mode
        # print("Ultrasonic.avoidbyragar")
        ultrasonic.avoidbyragar()
        time.sleep(0.5)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['send_distance']:  # Enter ultrasonic distance measurement mode
        # print("Ultrasonic.send_distance")
        ultrasonic.send_distance()
        time.sleep(1)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['maze']:  # Enter ultrasonic maze walking mode
        # print("Ultrasonic.maze")
        ultrasonic.maze()
        time.sleep(0.05)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['camera_normal']:  # Enter debug mode
        time.sleep(2)
        print("CRUISING_FLAG == 7")
        # path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'
        #call("%s" % path_sh, shell=True)
        cfg.CRUISING_FLAG = cfg.CRUISING_SET['normal']

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['camera_linepatrol']:  # Enter camera line tracking operation
        function.linepatrol_control()
        time.sleep(0.01)

    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['qrcode_detection']:  # Enter camera QR code detection recognition application
        function.qrcode_control()
        time.sleep(0.01)
    elif cfg.CRUISING_FLAG == cfg.CRUISING_SET['normal']:
        if cfg.VOICE_MOD == cfg.VOICE_MOD_SET['normal']:
            time.sleep(0.001)
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['openlight']:	 # Turn on lights
            car_light.open_light()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['closelight']:	 # Turn off lights
            car_light.close_light()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['forward']:		# Move forward
            go.forward()
            time.sleep(2)
            go.stop()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['back']:		# Move backward
            go.back()
            time.sleep(2)
            go.stop()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['left']:		# Turn left
            cfg.LIGHT_STATUS = cfg.TURN_LEFT
            go.left()
            time.sleep(0.8)
            go.stop()
            cfg.LIGHT_STATUS = cfg.STOP
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['right']:		# Turn right
            cfg.LIGHT_STATUS = cfg.TURN_RIGHT
            go.right()
            time.sleep(0.8)
            go.stop()
            cfg.LIGHT_STATUS = cfg.STOP
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['stop']:		# Stop
            go.stop()
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['nodhead']:		# Nod
            for i in range(1, 4):
                if i:
                    for j in range(90, 0, -5):
                        print(j)
                        servo.set(8, j)
                        time.sleep(0.04)
                    time.sleep(0.1)
            servo.set(8, 0)
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']
        elif cfg.VOICE_MOD == cfg.VOICE_MOD_SET['shakehead']:	 # Shake head
            for i in range(1, 3):
                if i:
                    for j in range(45, 135, 5):
                        # print(j)
                        servo.set(7, j)
                        time.sleep(0.02)
                    time.sleep(0.1)
                    for j in range(135, 45, -5):
                        # print(j)
                        servo.set(7, j)
                        time.sleep(0.02)
                    time.sleep(0.1)
            servo.set(7, 90)
            cfg.VOICE_MOD = cfg.VOICE_MOD_SET['normal']

    else:
        time.sleep(0.001)

def status():
    """
    Status update function, such as car lights, OLED need to be updated periodically, can be written here
    :return:
    """
    if cfg.PROGRAM_ABLE:	 # If the system program flag is enabled
        if cfg.LOOPS > 30:   # The update function is entered every 0.1 seconds, here it is 0.3 seconds to detect the car direction and turn on the corresponding turn signal light based on the car direction
            if cfg.LIGHT_STATUS == cfg.TURN_FORWARD:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS	 # Every time you enter the control direction, assign this status to the previous status
                car_light.forward_turn_light()
            elif cfg.LIGHT_STATUS == cfg.TURN_BACK:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
                car_light.back_turn_light()
            elif cfg.LIGHT_STATUS == cfg.TURN_LEFT:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
                car_light.left_turn_light()
            elif cfg.LIGHT_STATUS == cfg.TURN_RIGHT:
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
                car_light.right_turn_light()
            elif cfg.LIGHT_STATUS == cfg.STOP and cfg.LIGHT_LAST_STATUS != cfg.LIGHT_STATUS:	 # Let the STOP light only execute once in the continuous STOP situation
                cfg.LIGHT_LAST_STATUS = cfg.LIGHT_STATUS
                if cfg.LIGHT_OPEN_STATUS == 1:
                    car_light.open_light()
                else:
                    car_light.close_light()
        if cfg.LOOPS > 100:  		# The timer is set to enter every 0.01 seconds, greater than 100 means it has incremented 100 times, i.e., 1 second, some data display functions that do not need to be updated too quickly can be placed here
            cfg.LOOPS = 0			# Clear LOOPS
            power.show_vol()    	# Power level bar power display
            try:
                oled.disp_cruising_mode()  	# oled display mode
            except:
                print('oled initialization fail')

    loops = cfg.LOOPS   # Assign to an intermediate value for increment
    loops = loops + 1   # Increment
    cfg.LOOPS = loops   # Assign back

    loops = cfg.PS2_LOOPS   # Assign to an intermediate value for increment
    loops = loops + 1   # Increment
    cfg.PS2_LOOPS = loops   # Assign back

    Timer(0.01, status).start()  # Every time you enter, you need to restart the timer

if __name__ == '__main__':
    '''
    Main program entry
    '''
    print("....wifirobots start!...")

    os.system("sudo hciconfig hci0 name XiaoRGEEK")  # Set Bluetooth name
    time.sleep(0.1)
    os.system("sudo hciconfig hci0 reset")  # Restart Bluetooth
    time.sleep(0.3)
    os.system("sudo hciconfig hci0 piscan")  # Restore Bluetooth scanning function
    time.sleep(0.2)
    print("now bluetooth discoverable")

    servo.restore()  		# Reset servo
    try:
        oled.disp_default()		# oled display initialization information
    except:
        print('oled initialization fail')
    car_light.init_led() 	# Car light show
    time.sleep(0.1)

    threads = []  # Create a thread list
    t1 = threading.Thread(target=camera.run, args=())  # Camera data collection processing thread
    threads.append(t1)  # Add the thread to the thread queue
    t2 = threading.Thread(target=socket.bluetooth_server, args=())  # New Bluetooth thread
    threads.append(t2)
    t3 = threading.Thread(target=socket.tcp_server, args=())  # New wifi tcp communication thread
    threads.append(t3)
    t4 = threading.Thread(target=voice.run, args=())  	# Voice module thread
    threads.append(t4)

    ti = threading.Timer(0.1, status)		# New timer
    ti.start()		# Start timer

    path_sh = 'sh ' + os.path.split(os.path.abspath(__file__))[0] + '/start_mjpg_streamer.sh &'  # start_mjpg_streamer startup command
    call("%s" % path_sh, shell=True)  # Run start_mjpg_streamer in a new process
    time.sleep(1)

    for t in threads:
        #print("theads %s ready to start..." % t)
        t.setDaemon(True)  # Set the thread as a daemon thread
        t.start()  # Start the thread
        time.sleep(0.05)
    # print("theads %s start..." %t)
    print("all theads start...>>>>>>>>>>>>")
    servo.store()		# Restore the car's saved servo angle
    go.motor_init()		# Restore the car's saved motor speed
    while True:
        '''
        Main program loop
        '''
        try:
            if cfg.PROGRAM_ABLE:	 # If the system program flag is enabled
                cfg.PS2_LOOPS = cfg.PS2_LOOPS + 1
                if cfg.PS2_LOOPS > 20:
                    ps2.control()
                    cfg.PS2_LOOPS = 0
            cruising_mode() 										# Run mode switching function in the main thread
        except Exception as e:										# Capture and print error information
            time.sleep(0.1)
            print('cruising_mod error:', e)
