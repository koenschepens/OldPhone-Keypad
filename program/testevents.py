from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
from datetime import datetime
import sys
import logging
import ConfigParser

try:
    from xbmc.xbmcclient import XBMCClient
except:
    sys.path.append('/usr/share/pyshared/xbmc')
    from xbmcclient import XBMCClient

addonFolder = "/home/osmc/.kodi/addons/service.keypad/" 

config = ConfigParser.RawConfigParser()
config.read(addonFolder + 'keypad.config')

#logging.basicConfig(filename=addonFolder + 'keypad.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)

now = datetime.now().isoformat()

logging.info(str(now))

#logging.info("Cleanup GPIO")
#GPIO.cleanup()
logging.info("Setting GPIO mode to BCM")
GPIO.setmode(GPIO.BCM)

#contains a dictionary of each row an array of columns for that row
rows = {}

#keep seperate array with columns to check if already set up
columns = []
keys = {}
i = 1

gpiokeymappings = config.options("gpiokeymapping")

def row_changed(row):
    global rows
    GPIO.remove_event_detect(row)
    GPIO.setup(row, GPIO.OUT)

    # Set columns as in
    for column in rows[row]:
        GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Send signal from row to columns
    GPIO.output(row, 1)
    sleep(0.05)

    # Read which column it was
    for column in rows[row]:
        columnValue = GPIO.input(column)

        if(columnValue):
            print("key: " + keys[str(row) + "," + str(column)])

    # Set row and columns back to original setup
    GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for column in rows[row]:
        GPIO.setup(column, GPIO.OUT)
        GPIO.output(column, 1)

    GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed) 

# Read all GPIO key mappings and ad them to the keys dictionary 
for option in gpiokeymappings:
    print (option)
    row = int(config.get("gpiokeymapping", option).split(",")[0])
    column = int(config.get("gpiokeymapping", option).split(",")[1])

    # define key for later retrieval
    keys[config.get("gpiokeymapping", option)] = option
    logging.info("setting up " + option + " as [" + str(row) + "," + str(column) + "]")

    if row not in rows:
        rows[row] = [column]
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed) 
    else:
        rows[row].append(column)

    if column not in columns:
        columns.append(column)
        GPIO.setup(column, GPIO.OUT)
        GPIO.output(column, 1)  

def main():
    while True:
        print("a")
        try:
            sleep(1)
        except KeyboardInterrupt:
            print "okbye"
            raise
        except:
            print "Exit:", sys.exc_info()[0]
            GPIO.cleanup()
            raise
        pass

main()