#!/usr/bin/env python

"""
Current Author: Matthew Carlson
				matthewfcarlson@gmail.com
				
Original Author : pescimoro.mattia@gmail.com
Licence : GPL v3 or any later version

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.
 
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Modifed by Matthew Carlson on 7/3/2014 add new functionality

Using the nmap library (https://pypi.python.org/pypi/python-nmap)
As well as the GPIO port (http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3)
Also the servo library (http://www.raspihub.com/go/aa9b4e13ca60447a26b16470fd5c477df801b00d6fbf7ac7f76e0467801d472e)

Possibly add two transistors to control power to the servo as well as the control signal itself (both should be 5v and the pi uses 3.3v) 
"""

import os
import sys
import nmap                         # import nmap.py
import time
import RPi.GPIO as GPIO

from RPIO import PWM

#setup GPIO
GPIO.setmode(GPIO.BCM)

#setup knock detection
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

#setup servo
servo = PWM.Servo()
servo.set_servo(17, 1200)
sleep (2)
servo.stop_servo(17)

#this is the time since the last authentications
last_auth = time.time()
#this is the number of hosts since the last scan
last_found = 0

#A rudimentary semaphore to prevent seeking from running twice
seeking = false
#another semaphore for making sure it doesn't open twice
opening = false

#add the knock detector on pin 23
GPIO.add_event_detect(23, GPIO.FALLING, callback=knock_detected, bouncetime=300)  

try:
    nm = nmap.PortScanner()         # creates an'instance of nmap.PortScanner
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)

# defines a function to analize the network
def seek():
	if seeking:
		return last_found
	seeking = true
    count = 0
    nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -T5')
    # executes a ping scan

    hosts_list = [(nm[x]['addresses']) for x in nm.all_hosts()]
    # saves the host list

    localtime = time.asctime(time.localtime(time.time()))
    print('============ {0} ============'.format(localtime))
    # print out system time
    
    for addresses in hosts_list:
        count = count + 1
        print('FOUND {0}'.format(addresses))
	
	previous_count = last_found
	last_found = count
	seeking = false
    return previous_count - count                 # returns the host number

def beep():                        # no sound dependency
    print ('\a')

#interrup handler for the knock
def knock_detected(self):
	print ('We got a knock!')
	open()

def open():
	if time.time()-last_auth < 100 :
		open_doorknob()
		print ("Open the door with the servo!")
	else:
		#do a quick scan
		diff = seek()
		#check to make sure we didn't just go on top of an already running seek
		if seeking:
			sleep(1) #wait until it's done if that's the case
		
		if (difference > 0):
			print ("Didn't see you there. Let me get that for ya")
			authorize()
			open_doorknob()
		else:
			print ("You are not authorized!")

def open_doorknob():
	if opening:
		return false
	opening = true
	print("Actuate servo!")
	#Possibly have a transistor to turn current to the servo on?
	servo.set_servo(17, 1200) #turn the doorknob
	sleep(2) #wait for a few seconds
	servo.stop_servo(17) #stop the turning
	sleep(2)
	#servo.set_servo(17,) #this is to reverse the servo back to where it was
	#possible turn off transitor to servo?
	opening = false
	
def authorize():
	last_auth = time.time()
	print ("Authorized!")
    
if __name__ == '__main__':
    count = new_count = seek()

    # main loop
    while (true):
		
        difference = seek()
		if (difference > 0):
			authorize()
		elif (difference < 0):
			print ("Goodbye Roommate. Do not mourn for me.")
        time.sleep(1);
	GPIO.cleanup()