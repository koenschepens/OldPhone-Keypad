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

def row_changed(row):
    global rows
    print('Row changed: ' + str(row))
    print('Contains columns: ' + str(rows[row]))
    GPIO.setup(row, GPIO.OUT)
    GPIO.remove_event_detect(row)

    # Set columns as in
    for column in rows[row]:
        GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Send signal from row to columns
    GPIO.output(row, 1)

    # Read which column it was
    for column in rows[row]:
        columnValue = GPIO.input(column)
        if(columnValue):
            print(keys[str(row) + "," + str(column)])

    GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for column in rows[row]:
        GPIO.setup(column, GPIO.OUT)
        GPIO.output(column, 1)

def main():
    # Read all GPIO key mappings and ad them to the keys dictionary 
    for option in gpiokeymappings:
        print (option)
        row = int(config.get("gpiokeymapping", option).split(",")[0])
        column = int(config.get("gpiokeymapping", option).split(",")[1])

        # define key for later retrieval
        keys[config.get("gpiokeymapping", option)] = option

        print("row " + str(row))
        if row not in rows:
            rows[row] = [column]
            GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed) 
        else:
            rows[row].append(column)

        if column not in columns:
            print("col " + str(column))
            columns.append(column)
            GPIO.setup(column, GPIO.OUT)
            GPIO.output(column, 1)   

gpiokeymappings = config.options("gpiokeymapping")

main()

while True:
    try:
        sleep(0.05)
    except KeyboardInterrupt:
        print "okbye"
        raise
    except:
        GPIO.cleanup()
        raise
    pass   