# coding:utf-8
"""
树莓派WiFi无线视频小车机器人驱动源码
作者：Sence
版权所有：小R科技（深圳市小二极客科技有限公司www.xiao-r.com）；WIFI机器人网论坛 www.wifi-robots.com
本代码可以自由修改，但禁止用作商业盈利目的！
本代码已申请软件著作权保护，如有侵权一经发现立即起诉！
"""
"""
@version: python3.7
@Author  : xiaor
@Explain :树莓派GPIO配置文件
@contact :
@Time    :2020/05/09
@File    :xr_gpio.py
@Software: PyCharm
"""

import RPi.GPIO as GPIO

# Set pin mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Buzzer pin
BUZZER = 10

# Set the motor pin
ENA = 13  	# //L298 enable A
ENB = 20  	# //L298 enable B
IN1 = 16  	# //Motor interface 1
IN2 = 19  	# //Motor interface 2
IN3 = 26  	# //Motor interface 3
IN4 = 21  	# //Motor interface 4

# Setting up the Ultrasonic Pin
ECHO = 4  	# Ultrasonic receiving pin
TRIG = 17  	# Ultrasonic transmitting pin

# Setting up the infrared pins
IR_R = 18  	# Infrared line patrol on the right side of the car
IR_L = 27  	# The left side of the car patrols the infrared
IR_M = 22  	# Infrared obstacle avoidance in the middle of the car
IRF_R = 25  # The car follows the right infrared
IRF_L = 1  # The car follows the left infrared

# Pin initialization enable
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
ENA_pwm = GPIO.PWM(ENA, 1000)
ENA_pwm.start(0)
ENA_pwm.ChangeDutyCycle(100)
ENB_pwm = GPIO.PWM(ENB, 1000)
ENB_pwm.start(0)
ENB_pwm.ChangeDutyCycle(100)

# 红外引脚初始化使能
GPIO.setup(IR_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Infrared pin initialization enable
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)  			# Ultrasonic module transmitter pin settings trig
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  	# Ultrasonic module receiving end pin setting echo
# Buzzer pin initialization enable
GPIO.setup(BUZZER, GPIO.OUT, initial=GPIO.LOW)			# The buzzer is set to low level


def digital_write(gpio, status):
	"""
	Set the gpio port to level
	Parameters: gpio is the port to be set, status is the status value which can only be True (high level) or False (low level)
	"""
	GPIO.output(gpio, status)

def digital_read(gpio):
	"""
	Read the level of the gpio port
	"""
	return GPIO.input(gpio)

def ena_pwm(pwm):
	"""
		Set the PWM of the motor speed control port ena
	"""
	ENA_pwm.ChangeDutyCycle(pwm)

def enb_pwm(pwm):
	"""
	Set the pwm of the motor speed control port enb
	"""
	ENB_pwm.ChangeDutyCycle(pwm)
