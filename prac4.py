# Practical 4 Python File

# CTTKIE001
# DMNSTE001

#!/usr/bin/python3

import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import threading
import os

###---SETUP---###

GPIO.setmode(GPIO.BCM)

# Buttons
resetPin = 26
frequencyPin = 19
stopPin = 13
displayPin = 6

GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(frequencyPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(stopPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(displayPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# SPI - ADC
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

mcp = Adafruit_MCP3008.MCP3008(clk=SPICLK, cs=SPICS, mosi=SPIMOSI, miso=SPIMISO) #ADC object

# Global Variables
values = [0]*8 #data from ADC

upTime = 0
monEnabled = true
monDelay = 0.5

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
		switch (monitoringDelay) {
			case (0.5):
				monitoringDelay = 1
				break
			case (1):
				monitoringDelay = 2
				break
			case (2):
				monitoringDelay = 0.5
				break
		}
		# Clean the console
		os.system('clear')
		print("Frequency button pushed")
		

def stopPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		# Start/Stop monitoring, leave timer alone
		monEnabled = !monEnabled

		# Clean the console
		os.system('clear')
		print("Stop button pushed")

def displayPush(channel):
	if (GPIO.input(channel) == GPIO.LOW): #avoid trigger on button realease
		os.system('clear')
		print("Display button pushed")
		print(mcp.read_adc(1))

def timer():
	if (monEnable):
		#Stuff

	
	#start timer in new thread, delay and recall function
	threading.Timer(monDelay, timer).start()
	upTime += monDelay
	

# Interrupt Event Detection
GPIO.add_event_detect(resetPin, GPIO.FALLING, callback=resetPush, bouncetime=100)
GPIO.add_event_detect(frequencyPin, GPIO.FALLING, callback=frequencyPush, bouncetime=100)
GPIO.add_event_detect(stopPin, GPIO.FALLING, callback=stopPush, bouncetime=100)
GPIO.add_event_detect(displayPin, GPIO.FALLING, callback=displayPush, bouncetime=100)


###---LOOP---###
try:
	print("Ready!")
	#keep the program running, waiting for button presses
	while(1):
		pass

except KeyboardInterrupt:
	print("Finishing")
	#release all resources being used by this program
	GPIO.cleanup()