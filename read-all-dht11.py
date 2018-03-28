#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from pprint import pprint

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop 
from luma.core.render import canvas 
from luma.core.virtual import viewport 
from luma.core.legacy import text, show_message 
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90, rotate=0)
device.contrast(1)

def bin2dec(string_num):
    return str(int(string_num, 2))

gpio_data_pin = 4

while True:
	data = []

	GPIO.cleanup()

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gpio_data_pin,GPIO.OUT)
	GPIO.output(gpio_data_pin,GPIO.HIGH)
	time.sleep(0.025)
	GPIO.output(gpio_data_pin,GPIO.LOW)
	time.sleep(0.025)

	GPIO.setup(gpio_data_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	for i in range(0,500):
	    data.append(GPIO.input(gpio_data_pin))


	bit_count = 0
	tmp = 0
	count = 0
	HumidityBit = ""
	TemperatureBit = ""
	crc = ""
	
	try:
		while data[count] == 1:
			tmp = 1
			count = count + 1


		for i in range(0, 32):
			bit_count = 0

			while data[count] == 0:
				tmp = 1
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 3:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "1"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "1"
			else:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "0"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "0"

	except:
		print "Hiccup!"

	oopsie = False
	try:
		for i in range(0, 8):
			bit_count = 0

			while data[count] == 0:
				tmp = 1
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 3:
				crc = crc + "1"
			else:
				crc = crc + "0"
	except:
		print "Ooops!"
		oopsie = True

	
	if oopsie == False:
		Humidity = bin2dec(HumidityBit)
		Temperature = bin2dec(TemperatureBit)

		print "H:" + Humidity
		print "T:" + Temperature
		with canvas(device) as draw:
		    text(draw, (0, 0), "T{0}C".format(Temperature), fill="white")
		time.sleep(3)
		with canvas(device) as draw:
		    text(draw, (0, 0), "H{0}%".format(Humidity), fill="white")
		time.sleep(2)
	time.sleep(1)