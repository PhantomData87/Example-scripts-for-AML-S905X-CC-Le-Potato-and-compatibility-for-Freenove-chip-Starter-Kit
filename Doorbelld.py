#!/usr/bin/env python3
#############################################################################
# Filename	: Doorbelld.py
# Description	: Control buzzer with button via Libreboard
# auther	: Alonzo Ortiz-Sanchez
# modification	: 2023/01/25
# gpio physical : 12, 16
# gpio offset	:  6, 93
# gpio BCM/RPI	: GPIO18,   GPIO23
# gpio libre	: GPIOAO_6, GPIOX_14
# chip		: gpiochip0 gpiochip1
#############################################################################
import gpiod

# Define parameters
chip0 = gpiod.Chip("gpiochip0")
chip1 = gpiod.Chip("gpiochip1")
button_current = chip0.get_line(6)
buzzer_notify = chip1.get_line(93)

# Functions
def setup():
	global buzzer_notify, button_current
	"""
	This will initialize the variables used throughout the program.
	Am new to gpio so this is a bit more commentated than usual
	"""
	buzzer_notify.request(consumer='Used to cause buzzer to react on breadboard',
	type=gpiod.LINE_REQ_DIR_OUT, #Declaring that it will make current
	default_vals=[0]) #Declaring what will appear when I run `gpioinfo`
	
	button_current.request(consumer='Used to redirect power away from button',
	type=gpiod.LINE_REQ_DIR_IN, #Declaring that it will read values
	default_vals=[0],
	flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

	# Since, we want the state of the read to be consistant, this flag will keep anything read as a stable voltage
	#button_current.set_flags(gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

def run():
	"""
	Keeps running to detect when user has pressed button that causes
	button_current to stop receiving such strong power, to play a fun sound
	"""
	global buzzer_notify, button_current
	known = True
	while True:
		if not button_current.get_value(): # Button pressed
			if not known:
				buzzer_notify.set_value(1)	# Buzzer turned on
				print("buzzer sound >>>")
				known = True
		elif button_current.get_value(): # Button released / not pressed
			if known:
				buzzer_notify.set_value(0) # Buzzer turned off
				print("buzzer stopped<<<")
				known = False

def halt():
	"""
	We safely clean up, and stop using any gpio's currently used by the system
	"""
	global chip0, chip1, buzzer_notify, button_current
	print("\rProgram has ended, setting pins back to initial state") #\r added To hide pressing Ctrl-c
	if buzzer_notify.active_state():
		buzzer_notify.set_value(0)
	buzzer_notify.release()
	button_current.release()
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
