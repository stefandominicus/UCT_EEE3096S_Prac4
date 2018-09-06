# Practical 4 Python File

# CTTKIE001
# DMNSTE001

#!/usr/bin/python3

###---IMPORTS---###
import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import threading
import os
import datetime
###-------------###

###---VARIABLES---###
# Button Pins
resetPin = 26
frequencyPin = 19
stopPin = 13
displayPin = 6

# SPI Pins
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

# ADC Inputs
TEMP = 0
LDR = 1
POT = 2

# References for LDR lightness %
LDR_MAX = 1023
LDR_MIN = 0

# References for Thermister
T0 = 0,5
Tc = 10

# General
state = ["empty"]*5 # Could probably replace "empty" with "" instead
readBuffer = [state]*5 # Readings to be displayed
upTime = 0 # Time sice timer was reset
monEnabled = True # Is the system allowed to record new values
monDelay = 0.5 # Monitoring interval
terminating = False # Is the system trying to close
###-------------###

###---SETUP---###
# Pinmode
GPIO.setmode(GPIO.BCM)

# Button Pins IO
GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequencyPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(displayPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# SPI Pins IO
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# ADC Object
mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO) #ADC object
###-------------###

###---BUTTONS---###
# Interrupt Methods
def resetPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): # Avoid trigger on button realease
		# Reset the timer
		global upTime
		upTime = 0
		# Clean the console
		os.system('clear')
		print("Reset button pushed. Timer has been reset.") # DEBUG

def frequencyPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): # Avoid trigger on button realease
		# Change the monitoring frequency
		global monDelay
		if (monDelay == 0.5): monDelay = 1
		elif (monDelay == 1): monDelay = 2
		elif (monDelay == 2): monDelay = 0.5
		# Clean the console
		os.system('clear')
		print("Frequency button pushed. Monitoring interval is now {}s.".format(monDelay)) # DEBUG

def stopPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): # Avoid trigger on button realease
		# Start/Stop monitoring, leave timer alone
		global monEnabled
		monEnabled = not monEnabled
		# Clean the console
		os.system('clear')
		if (monEnabled): print("Start/Stop button pushed. Monitoring resumed.") # DEBUG
		else: print("Start/Stop button pushed. Monitoring stopped") # DEBUG

def displayPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): # Avoid trigger on button realease
		# Clean the console
		os.system('clear')
		#print("Display button pushed") # DEBUG
		# Display recent entries
		print("{:<15}{:<15}{:<15}{:<15}{:<15}".format("Time", "Timer", "Pot", "Temp", "Light"))
		for entry in readBuffer:
			# each entry is a state
			print("{:<15}{:<15}{:<15}{:<15}{:<15}".format(entry[0], entry[1], entry[2], entry[3], entry[4]))

# Interrupt Event Detection
GPIO.add_event_detect(resetPin, GPIO.FALLING, callback=resetPush, bouncetime=100)
GPIO.add_event_detect(frequencyPin, GPIO.FALLING, callback=frequencyPush, bouncetime=100)
GPIO.add_event_detect(stopPin, GPIO.FALLING, callback=stopPush, bouncetime=100)
GPIO.add_event_detect(displayPin, GPIO.FALLING, callback=displayPush, bouncetime=100)
###-------------###

###---TIMER---###
def timer():
	if (not terminating): # Only continue if the parent thread is still running
		global upTime
		if (monEnabled):
			#print("Testing... UpTime = ", upTime) # DEBUG
			# Add store current state
			addToBuffer(getCurrentState())
		# Start timer in new thread, delay and recall function
		threading.Timer(monDelay, timer).start()
		upTime += monDelay
###-------------###

###---ADC---###
def getADCValue(chan):
	#return value from ADC channel
	return mcp.read_adc(chan)

def convertPot(value):
	voltage = value * (3.3/1023) # Scale ADC value to a fraction of 3.3V
	return "{:.2f} V".format(voltage)

def convertTemp(value):
	# convert to degrees
	voltage = value * (3.3/1023)

	degrees = (voltage-V0)/Tc # From datasheet
	return "{:.1f} C".format(degrees)

def convertLDR(value):
	# convert to percentage
	percentage = 100*(value - LDR_MIN)/(LDR_MAX-LDR_MIN)

	if (percentage > 100):
		percentage = 100
	if (percentage < 0):
		percentage = 0

	return "{:.0f}%".format(percentage)
###-------------###

###---BUFFER---###
def getCurrentState():
	min, sec = divmod(upTime, 60)
	hrs, min = divmod(min, 60)

	realTime = datetime.datetime.now().strftime("%H:%M:%S")
	timerValue = "{:02.0f}:{:02.0f}:{:04.1f}".format(hrs, min, sec)
	potValue = convertPot(getADCValue(POT))
	tempValue = convertTemp(getADCValue(TEMP))
	ldrValue = convertLDR(getADCValue(LDR))

	#return current parameters
	return [realTime, timerValue, potValue, tempValue, ldrValue]

def addToBuffer(state):
	#shift values in array
	for i in range(0, 4):
		readBuffer[i] = readBuffer[i+1]
	#add new value
	readBuffer[4] = state
###-------------###

###---LOOP---###
try:
	os.system('clear')
	print("Ready!")
	timer()
	# Keep the program running, waiting for button presses
	while(1):
		pass
except KeyboardInterrupt:
	print("losing")
	# Release all resources being used by this program
	terminating = True
	GPIO.cleanup()
###-------------###
