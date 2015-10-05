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

# Mapping to keyboard events
mapping = {
    G.BUTTON1: "one",
    G.BUTTON2: "two",
    G.BUTTON3: "three",
    G.BUTTON4: "four",
    G.BUTTON5: "five",
    G.BUTTON6: "six",
    G.BUTTON7: "seven",
    G.BUTTON8: "eight",
    G.BUTTON9: "nine",
    G.BUTTON0: "zero",
    G.BUTTONHEK: "HEK",
    G.BUTTONSTER: "STER"
}
# Mapping to keyboard events
kbmapping = {
        G.BUTTON1: "plus",
        G.BUTTON2: "up",
        G.BUTTON3: "3",
        G.BUTTON4: "left",
        G.BUTTON5: "enter",
        G.BUTTON6: "right",
        G.BUTTON7: "minus",
        G.BUTTON8: "down",
        G.BUTTON9: "space",
        G.BUTTON0: "esc",
        G.BUTTONHEK: "a",
        G.BUTTONSTER: "backspace"
}

#logging.basicConfig(filename=addonFolder + 'keypad.log',level=logging.INFO)
logging.basicConfig(level=logging.INFO)

config = ConfigParser.RawConfigParser()
configFile = addonFolder + 'keypad.config'
logging.info("reading config file " + configFile)
config.read(configFile)

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

def send_key(key):
    try:
        global mapping
        print(kbmapping[channelVal])
        xbmc.send_keyboard_button(button=kbmapping[channelVal])
    except:
        logging.warning("value invalid")

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
            key = keys[str(row) + "," + str(column)]
            print("key: " + key)
            send_key(key)

    # Set row and columns back to original setup
    GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    for column in rows[row]:
        GPIO.setup(column, GPIO.OUT)
        GPIO.output(column, 1)

    GPIO.add_event_detect(row, GPIO.RISING, callback=row_changed) 

gpiokeymappings = config.options("gpiokeymapping")

GPIO.cleanup()

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

print("waiting for everything to be set up...")
sleep(1)

logging.info("Setting up Kodi client")

host = config.get("xbmc", "host")
port = config.getint("xbmc", "port")

logging.info("host: " + str(host))
logging.info("port: " + str(port))

# Create an XBMCClient object and connect
xbmc = XBMCClient("OldPhone", "/etc/lirc/osmc-remote-lircd.png")
xbmc.connect()

while 0 < 1:
    try:
        sleep(0.05)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise
pass 