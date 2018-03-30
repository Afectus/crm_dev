#!/usr/bin/python

from evdev import InputDevice, categorize, ecodes

import os

devlist =  os.listdir("/dev/input")

for i in devlist:
	#print '/dev/input/%s' % (i)
	try:
		device = InputDevice('/dev/input/%s' % (i))
	except:
		print "ERROR DEVICE OR NO DEVICE"
	else:
		if device.name == 'Touch__KiT Touch  Computer INC.':
			print device.fn

#for event in device.read_loop():
#	 if event.type == ecodes.EV_KEY:
#	print(categorize(event))
