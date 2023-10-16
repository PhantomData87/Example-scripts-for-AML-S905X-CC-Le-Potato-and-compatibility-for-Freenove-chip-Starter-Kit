#!/usr/bin/env python3
#############################################################################
# Filename      : ColorfulLEDd.py
# Description   : Make an RGB LED change color by flipping 0 and 1s. PWM poor mans replication
# auther        : Alonzo Ortiz-Sanchez
# modification  : 2023/01/23
# gpio physical :  7, 10, 16
# gpio offset   : 98, 92, 93
# gpio BCM/RPI  : GPIO4, GPIO15, GPIO23
# gpio libre    : GPIOCLK_0, GPIOX_13, GPIOX_14
# chip          : gpiochip0
#############################################################################
import gpiod, time, random
from multiprocessing import Process

# Defining parameters
chip1 = gpiod.Chip("gpiochip1")
rPin = chip1.get_line(98)		# We want gpio, therefore we use gpio
gPin = chip1.get_line(93) 	# We want gpio18, therefore we use gpio AO_6
bPin = chip1.get_line(92)		# We want gpio, therefore we use gpio
cycleTime = 1             	# How fast is each cycle

# Functions
def setup():
	"""
	This will initialize the variables used throughout the program.
	Am new to gpio so this is a bit more commentated than usual
	"""
	global ledPin
	rPin.request(consumer='Used to change the frequency of the LED via semi analog signals', #Declaring what will appear when I run `gpioinfo`
			type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make current
			default_vals=[0])
	gPin.request(consumer='Used to change the frequency of the LED via semi analog signals',
                        type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make cu>
                        default_vals=[0])
	bPin.request(consumer='Used to change the frequency of the LED via semi analog signals',
                        type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make cu>
                        default_vals=[0])
	print("Program started")

def pmw_run(pin, percentage, cycleTime):
	cycleTime = cycleTime / 100
	awake = (1 - percentage) * cycleTime
	sleep = percentage * cycleTime
	#print("A: ", awake, "S:", sleep, "C:", cycleTime)
	while True:
		time.sleep(awake) # When powered, it turns that color off from the LED
		pin.set_value(0)
		time.sleep(sleep) # When not powered, it turns on that color for the LED
		pin.set_value(1)

def run():
	"""
	Keeps running the while loop below to acomplish our end goal.
	Usually some LED stuff
	"""
	global rPin, gPin, bPin, cycleTime
	rRan = random.randint(0,255)
	gRan = random.randint(0,255)
	bRan = random.randint(0,255)
	print(f"RGB values are:\n Red: {rRan}\n Green: {gRan}\n Blue: {bRan}")
	print(f"RGB value: #{hex(rRan)[2:].zfill(2)+hex(gRan)[2:].zfill(2)+hex(bRan)[2:].zfill(2)}")
	rRan = rRan / 255
	gRan = gRan / 255
	bRan = bRan / 255
	# Starting 3 processes to control their own timings
	r = Process(target=pmw_run, args=(rPin, rRan, cycleTime,))
	g = Process(target=pmw_run, args=(gPin, gRan, cycleTime,))
	b = Process(target=pmw_run, args=(bPin, bRan, cycleTime,))
	r.start()
	g.start()
	b.start()
	b.join()

def halt():
	"""
	We safely clean up, and stop using any gpio's currently used by the system
	"""
	global chip1, rPin, gPin, bPin
	print("\rProgram has ended, setting pins back to initial state") #\r added To prevent Ctrl+C to appear on terminal
	for pin in [rPin, gPin, bPin]:
		if pin.active_state():
			pin.set_value(0)
			pin.release()
	chip1.close()
	print("Succesfully terminated")

if __name__ == "__main__":
	"""
	Where our program execution starts
	"""
	print("Program is starting")
	setup()
	try:
		run()
	except KeyboardInterrupt: #Setting up to only close by pressing Ctrl+c
		halt()
	halt()
