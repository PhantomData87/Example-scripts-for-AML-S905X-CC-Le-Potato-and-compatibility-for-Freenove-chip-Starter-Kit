#!/usr/bin/env python3
#############################################################################
# Filename	: Alertord.py
# Description	: Control passive buzzer by poor mans PWM with Libreboard
# auther	: Alonzo Ortiz-Sanchez
# modification	: 2023/01/25
# gpio physical : 12, 16
# gpio offset	:  6, 93
# gpio BCM/RPI	: GPIO18,   GPIO23
# gpio libre	: GPIOAO_6, GPIOX_14
# chip		: gpiochip0 gpiochip1
#############################################################################
import gpiod, time
from multiprocessing import Process

# Define parameters
chip0 = gpiod.Chip("gpiochip0")
chip1 = gpiod.Chip("gpiochip1")
button_current = chip0.get_line(6)
buzzer_notify = chip1.get_line(93)

cycleTime = 0.01 # Lower this number for worse and worse sounds
alarmDuration = 1


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

def pmw_run(pin, cycleTime):
	# Inspired by RTTTL format (doesn't really work since am scared of not using a pause)
	a = (cycleTime*9) / 10
	b = (cycleTime*8) / 10
	c = (cycleTime*7) / 10
	d = (cycleTime*6) / 10
	e = (cycleTime*5) / 10
	f = (cycleTime*4) / 10
	g = (cycleTime*3) / 10
	h = (cycleTime*2) / 10
	j = cycleTime / 10
	#p = 0.05
	def play(pin, cycleTime, note):
		""" Helper function for playing notes and readability """
		time.sleep(note)
		pin.set_value(0)
		time.sleep(cycleTime - note)
		pin.set_value(1)
	def pause(pin,pausing):
		""" Helper function for pausing quickly """
		pin.set_value(0)
		time.sleep(p)
	while True:
		pin.set_value(1)
		play(pin, cycleTime, a)
		play(pin, cycleTime, b)
		play(pin, cycleTime, c)
		play(pin, cycleTime, d)
		play(pin, cycleTime, c)
		play(pin, cycleTime, b)
		play(pin, cycleTime, c)
		play(pin, cycleTime, e)
		play(pin, cycleTime, f)
		play(pin, cycleTime, g)
		play(pin, cycleTime, h)
		play(pin, cycleTime, j)
		#pause(pin, p)

def run():
	"""
	Keeps running to detect when user has pressed button that causes
	button_current to stop receiving such strong power, to play a fun sound
	"""
	global buzzer_notify, button_current, alarmDuration, cycleTime
	known = True
	buzz = Process(target=pmw_run, args=(buzzer_notify, cycleTime,))
	while True:
		if not button_current.get_value(): # Button pressed
			if not known:
				print("buzzer sound >>> ACTIVATED")
				buzz.start()	# Starting thread
				known = True
				time.sleep(alarmDuration)
				print("buzzer sound >>> DEACTIVATED")
				buzz.kill() 	# Stopping thread
		elif button_current.get_value(): # Button released / not pressed
			if known and not buzz.is_alive():
				buzz = Process(target=pmw_run, args=(buzzer_notify, cycleTime,)) # Since you cannot reuse it twice, I will recreate it
				print("buzzer restarted<<<")
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
