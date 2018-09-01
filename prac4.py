# Practical 4 Python File

# CTTKIE001
# DMNSTE001

#!/usr/bin/python3


import RPi.GPIO as GPIO
import Adafruit_MCP3008
import time
import os

GPIO.setmode(GPIO.BCM)
# pin definition
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
