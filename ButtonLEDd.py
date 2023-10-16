#!/usr/bin/env python3
#############################################################################
# Filename	: ButtonLEDd.py
# Description	: Control led with button via Libreboard
# auther	: Alonzo Ortiz-Sanchez
# modification	: 2023/01/13
# gpio physical : Pins 12 & 13
# gpio BCM/RPI	: Pins GPIO18 & GPIO27
# gpio libre	: Pins GPIOAO_6 & GPIOAO_9
# chip		: gpiochip0
#############################################################################
import gpiod

# Define parameters
chip = None
led_notify = None
button_current = None

# Functions
def setup():
	global chip, led_notify, button_current
	"""
	This will initialize the variables used throughout the program.
	Am new to gpio so this is a bit more commentated than usual
	"""
	chip = gpiod.Chip("gpiochip0")	 # I personally have between chip0 to chip1
	#lines = gpiod.find_line("7J1 Header Pin3") # This is used to find the offset in the chip to determine the right line we wish
	led_notify = chip.get_line(9)	 # Since I know the input, it should be safe
	button_current = chip.get_line(6)
	
	led_notify.request(consumer='Used to light up LED on breadboard',
	type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make current
	default_vals=[0]) #Declaring what will appear when I run `gpioinfo`
	
	button_current.request(consumer='Used to redirect power away from button',
	type=gpiod.LINE_REQ_DIR_IN, #Declaring that it will read values
	default_vals=[0])

def run():
	"""
	Keeps running to detect when user has pressed button that causes
	button_current to stop receiving such strong power
	"""
	global chip, led_notify, button_current
	known = True
	while True:
		if not button_current.get_value(): # Button pressed
			if not known:
				led_notify.set_value(1)	# LED turned on
				print("led turned on >>>")
				known = True
		elif button_current.get_value(): # Button released / not pressed
			if known:
				led_notify.set_value(0) # LED turned off
				print("led turned off<<<")
				known = False

def halt():
	"""
	We safely clean up, and stop using any gpio's currently used by the system
	"""
	global chip, led_notify, button_current
	print("\rProgram has ended, setting pins back to initial state") #\r added To hide pressing Ctrl-c
	if led_notify.active_state():
		led_notify.set_value(0)
	led_notify.release()
	button_current.release()
	chip.close()
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
