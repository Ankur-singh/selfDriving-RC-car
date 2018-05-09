import RPi.GPIO as gpio
import time

echo = 19
trans = 26
#led_p = 21
#led_n = 20
def distance():
	try:
		global echo, trans
		gpio.setmode(gpio.BCM)
		#gpio.setup(led_p, gpio.OUT)
		#gpio.setup(led_n, gpio.OUT)
		gpio.setup(trans, gpio.OUT)
		gpio.setup(echo, gpio.IN)

		gpio.output(trans, True)
		time.sleep(0.00001)
		gpio.output(trans, False)
			
		while gpio.input(echo) == 0:
			nosig = time.time()

		while gpio.input(echo) == 1:
			sig = time.time()

		t1 = sig - nosig

		distance = t1/0.000058
			
		gpio.cleanup()
		return distance

	except KeyboardInterrupt:
		print 'stopped by user'
		gpio.cleanup()
	
