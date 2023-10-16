#!/usr/bin/env python3
#############################################################################
# Filename      : BreathingLEDd.py
# Description   : Make an LED dim and brighten via poor mans replication of PWM by spamming 0 and 1 really quickly
# auther        : Alonzo Ortiz-Sanchez
# modification  : 2023/01/22
# gpio physical : 12
# gpio offset   : 6
# gpio BCM/RPI  : GPIO18
# gpio libre    : GPIOAO_6
# chip          : gpiochip0
#############################################################################
import gpiod, time

# Defining parameters
chip0 = gpiod.Chip("gpiochip0")
ledPin = chip0.get_line(6) 	# We want gpio18, therefore we use gpio AO_6
cycleTime = 0.005             	# How fast is each cycle
numOfCycles = 1000 		# How many cycles to perform
step = cycleTime/numOfCycles 	# How much gain does it change per cycle

# Functions
def setup():
	"""
	This will initialize the variables used throughout the program.
	Am new to gpio so this is a bit more commentated than usual
	"""
	global chip0, ledPin
	ledPin.request(consumer='Used to change the frequency of the LED via semi analog signals', #Declaring what will appear when I run `gpioinfo`
			type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make current
			default_vals=[0])
	print("Program started")

def run():
	"""
	Keeps running the while loop below to acomplish our end goal.
	Usually some LED stuff
	"""
	global ledPin, step, cycleTime
	# By changing very fast between each state, we effectively control the light the LED can show
	while True:
		print("Becoming lighter")
		freqAwake = 0		# How long the LED is on
		freqSleep = cycleTime	# How long the LED is off
		while freqAwake < cycleTime: # Making the LED slowly brighten up
			time.sleep(freqAwake)
			ledPin.set_value(0)
			time.sleep(freqSleep)
			ledPin.set_value(1)
			freqSleep -= step
			freqAwake += step
		print("Becoming darker")
		freqAwake = cycleTime
		freqSleep = 0
		while freqSleep < cycleTime: # Making the LED slowly darken down
			time.sleep(freqAwake)
			ledPin.set_value(0)
			time.sleep(freqSleep)
			ledPin.set_value(1)
			freqSleep += step
			freqAwake -= step
		ledPin.set_value(0)
		print("cycle over")
		time.sleep(1)

def halt():
	"""
	We safely clean up, and stop using any gpio's currently used by the system
	"""
	global ledPin, chip0
	print("\rProgram has ended, setting pins back to initial state") #\r added To prevent Ctrl+C to appear on terminal
	if ledPin.active_state():
		ledPin.set_value(0)
		ledPin.release()
	chip0.close()
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
