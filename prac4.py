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

# General
state = ["empty"]*5 # Could probably replace "empty" with "" instead
readBuffer = [state]*5 #readings to be output
upTime = 0
monEnabled = True
monDelay = 0.5
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
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		# Reset the timer
		upTime = 0
		# Clean the console
		os.system('clear')
		print("Reset button pushed")

def frequencyPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		# Change the monitoring frequency
		#---Might need to fiddle with the timer here...?---#
		global monDelay
		if (monDelay == 0.5): monDelay = 1
		elif (monDelay == 1): monDelay = 2
		elif (monDelay == 2): monDelay = 0.5
		# Clean the console
		os.system('clear')
		print("Frequency button pushed")

def stopPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		# Start/Stop monitoring, leave timer alone
		global monEnabled = not monEnabled
		# Clean the console
		os.system('clear')
		print("Stop button pushed")

def displayPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		# Clean the console
		os.system('clear')
		print("Display button pushed")
		# Display recent entries
		print("Time\tTimer\tPot\tTemp\tLight")
		for entry in readBuffer:
			# each entry is a state
			print(entry[0], "\t", entry[1], "\t", entry[2], "\t", entry[3], "\t", entry[4])

# Interrupt Event Detection
GPIO.add_event_detect(resetPin, GPIO.FALLING, callback=resetPush, bouncetime=100)
GPIO.add_event_detect(frequencyPin, GPIO.FALLING, callback=frequencyPush, bouncetime=100)
GPIO.add_event_detect(stopPin, GPIO.FALLING, callback=stopPush, bouncetime=100)
GPIO.add_event_detect(displayPin, GPIO.FALLING, callback=displayPush, bouncetime=100)
###-------------###

###---TIMER---###
def timer():
	if (monEnable):
		#Stuff
		print("testing the timer", upTime)
		#add store current state
		addToBuffer(getCurrentState)
	#start timer in new thread, delay and recall function
	threading.Timer(monDelay, timer).start()
	upTime += monDelay
###-------------###

###---ADC---###
def getADCValue(chan):
	#return value from ADC channel
	return mcp.read_adc(chan)

def convertPot(value):
	voltage = value * (3.3/1023)
	return str(voltage) + " V"

def convertTemp(value):
	degrees = value # Use datasheet
	return str(degrees) + " C"

def convertLDR(value):
	percentage = value # Use datasheet
	return str(percentage) + "%"
###-------------###

###---BUFFER---###
def getCurrentState():
	#get current time
	currentDT = datetime.datetime.now()

	realTime = currentDT.strftime("%H:%M:%S")
	timerValue = upTime.strftime("%H:%M:%S") # Not sure if this will work...
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
	print("Ready!")
	# Keep the program running, waiting for button presses
	while(1):
		pass
except KeyboardInterrupt:
	print("Finishing")
	# Release all resources being used by this program
	GPIO.cleanup()
###-------------###