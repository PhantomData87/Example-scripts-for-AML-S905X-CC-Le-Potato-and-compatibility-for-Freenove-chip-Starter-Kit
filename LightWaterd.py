#!/usr/bin/env python3
#############################################################################
# Filename      : ButtonLEDd.py
# Description   : Make lightwater LED do a nice stream via Libreboard
# auther        : Alonzo Ortiz-Sanchez
# modification  : 2023/01/15
# gpio offset	: 5,	    4,        89,	95,	  6,	    9,        81,       93,       94,       79
# gpio physical : 3,	    5,        24,       32,       12,       13,       36,       16,       18,       22
# gpio BCM/RPI  : SDA1,     SCL1,     CE0,      GPIO12,   GPIO18,   GPIO27,   GPIO16,   GPIO23,   GPIO24,   GPIO25
# gpio libre    : GPIOAO_5, GPIOAO_4, GPIOX_10, GPIOX_16, GPIOAO_6, GPIOAO_9, GPIOX_2,  GPIOX_14, GPIOX_15, GPIOX_0 
# chip          : gpiochip0, gpiochip1
#############################################################################
import gpiod, time

# Define parameters
physicalPinsOffsetChip0 = [5, 4, 6, 9]
physicalPinsOffsetChip1 = [93, 94, 79, 89, 95, 81]
chip0 = gpiod.Chip("gpiochip0")
chip1 = gpiod.Chip("gpiochip1")
pins = []
stopFor = 0.1

# Functions
def setup():
	global physicalPinsOffsetChip0, physicalPinsOffsetChip1, pins, chip0, chip1
	"""
	This will initialize the variables used throughout the program.
	Am new to gpio so this is a bit more commentated than usual
	"""
	pinSet0 = []
	pinSet1 = []
	for offset in physicalPinsOffsetChip0:
		pin = chip0.get_line(offset)
		pin.request(consumer='Used to light up one lightwater LED on breadboard',
		type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make current
		default_vals=[1]) #Declaring what will appear when I run `gpioinfo`
		pinSet0.append(pin)

	for offset in physicalPinsOffsetChip1:
		pin = chip1.get_line(offset)
		pin.request(consumer='Used to light up one lightwater LED on breadboard',
		type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make current
		default_vals=[1]) #Declaring what will appear when I run `gpioinfo`
		pinSet0.append(pin)

	#pinSet0 = chip0.get_lines(physicalPinsOffsetChip0)
	#pinSet1 = chip1.get_lines(physicalPinsOffsetChip1)

	pins = pinSet0 + pinSet1
	print("Program started")

def run():
	"""
	Keeps running the while loop below to acomplish our end goal.
	Usually some LED stuff
	"""
	global pins, stopFor
	choice = int(input("Pick an option for me:\n1. Cascade\n2. Collapse\n> "))
	charge = 1
	while True:
		if choice == 1: #Have one led always turn off and move
			for pin in pins:
				pin.set_value(1) # Turn off LED
				time.sleep(stopFor)  # Sleep
				pin.set_value(0) #Turn on LED
			time.sleep(stopFor)	# Visual pause
			for pin in pins[::-1]:
				pin.set_value(1) # Turn off LED
				time.sleep(stopFor)  # Sleep
				pin.set_value(0) #Turn on LED
			time.sleep(stopFor)	# Visual pause
		elif choice == 2:
			pins[9].set_value(charge)
			pins[0].set_value(charge)
			time.sleep(stopFor)
			pins[8].set_value(charge)
			pins[1].set_value(charge)
			time.sleep(stopFor)
			pins[7].set_value(charge)
			pins[2].set_value(charge)
			time.sleep(stopFor)
			pins[6].set_value(charge)
			pins[3].set_value(charge)
			time.sleep(stopFor)
			pins[5].set_value(charge)
			pins[4].set_value(charge)
			time.sleep(stopFor)

			if charge: # To cycle through on and off for the LED
				charge = 0
			elif not charge:
				charge = 1

def halt():
	"""
	We safely clean up, and stop using any gpio's currently used by the system
	"""
	global pins, chip0, chip1
	print("\rProgram has ended, setting pins back to initial state") #\r added To hide pressing Ctrl-c
	for pin in pins:	# Turning off each pin's voltage
		if pin.active_state():
			pin.set_value(0)
			pin.release()
	chip0.close()
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
