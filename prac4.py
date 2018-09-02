# Practical 4 Python File

# CTTKIE001
# DMNSTE001

#!/usr/bin/python3


import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os

###---SETUP---###
# Pins
GPIO.setmode(GPIO.BCM)

resetPin = 26
frequencyPin = 19
stopPin = 13
displayPin = 6

GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequencyPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(displayPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO)

# global variable
values = [0]*8



# Interrupt Methods
def resetPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		os.system('clear')
		print("Reset button pushed")

def frequencyPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		os.system('clear')
		print("Frequency button pushed")

def stopPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		os.system('clear')
		print("Stop button pushed")

def displayPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		os.system('clear')
		print("Display button pushed")

# Interrupt Setup
GPIO.add_event_detect(resetPin, GPIO.FALLING, callback=resetPush, bouncetime=100)
GPIO.add_event_detect(frequencyPin, GPIO.FALLING, callback=frequencyPush, bouncetime=100)
GPIO.add_event_detect(stopPin, GPIO.FALLING, callback=stopPush, bouncetime=100)
GPIO.add_event_detect(displayPin, GPIO.FALLING, callback=displayPush, bouncetime=100)


try:
	print("Ready!")
	#keep the program running, waiting for button presses
	while(1):
		pass

except KeyboardInterrupt:
	print("Finishing")
	#release all resources being used by this program
	GPIO.cleanup()