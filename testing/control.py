import RPi.GPIO as gpio
import time


a_enable = 25
a1 = 18
a2 = 17

b_enable = 9
b1 = 23
b2 = 22

def init():
	gpio.setmode(gpio.BCM)
	gpio.setup(a1, gpio.OUT)
	gpio.setup(a2, gpio.OUT)
	gpio.setup(b1, gpio.OUT)
	gpio.setup(b2, gpio.OUT)
	gpio.setup(a_enable, gpio.OUT)
	gpio.setup(b_enable, gpio.OUT)

def forward(sec):
	init()
	gpio.output(a_enable, True)
	gpio.output(b_enable, True)
	gpio.output(a1, True)
	gpio.output(a2, False)
	gpio.output(b1, False)
	gpio.output(b2, True)

	time.sleep(sec)

	gpio.cleanup()



def reverse(sec):
	init()
	gpio.output(a_enable, True)
	gpio.output(a_enable, True)
	gpio.output(b_enable, True)
	gpio.output(a1, False)
	gpio.output(a2, True)
	gpio.output(b1, True)
	gpio.output(b2, False)

	time.sleep(sec)

	gpio.cleanup()



def left(sec):
	init()
	gpio.output(a_enable, True)
	gpio.output(a_enable, True)
	gpio.output(b_enable, True)
	gpio.output(a1, False)
	gpio.output(a2, False)
	gpio.output(b1, False)
	gpio.output(b2, True)

	time.sleep(sec)

	gpio.cleanup()



def right(sec):
	init()
	gpio.output(a_enable, True)
	gpio.output(a_enable, True)
	gpio.output(b_enable, True)
	gpio.output(a1, True)
	gpio.output(a2, False)
	gpio.output(b1, False)
	gpio.output(b2, False)

	time.sleep(sec)

	gpio.cleanup()


