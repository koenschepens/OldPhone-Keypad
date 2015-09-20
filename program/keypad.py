from time import sleep
import RPi.GPIO as GPIO
from enum import Enum
from subprocess import call
import time
import sys
import logging
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('/usr/share/keypad/keypad.config')

try:
    from xbmc.xbmcclient import XBMCClient
except:
    sys.path.append('../../lib/python')
    from xbmcclient import XBMCClient

class G(Enum):
    NONE = 0
    BCM08 = 1
    BCM07 = 2
    BCM05 = 4
    BCM06 = 8
    BCM12 = 16
    BCM13 = 32
    BCM19 = 64
    BCM16 = 128
    BCM26 = 256
    BCM20 = 512
    BCM21 = 1024
    BUTTON1 = BCM13+BCM20
    BUTTON2 = BCM13+BCM26
    BUTTON3 = BCM13+BCM16
    BUTTON4 = BCM12+BCM20
    BUTTON5 = BCM12+BCM26
    BUTTON6 = BCM12+BCM16
    BUTTON7 = BCM06+BCM20
    BUTTON8 = BCM05+BCM06
    BUTTON9 = BCM06+BCM16
    BUTTON0 = BCM13+BCM07
    BUTTONSTER = BCM20+BCM07
    BUTTONHEK = BCM21+BCM08

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

logging.basicConfig(filename='/var/log/keypad.log',level=logging.INFO)
#logging.basicConfig(level=logging.INFO)

logging.info("Setting GPIO mode to BCM")
GPIO.setmode(GPIO.BCM)

def setReadWrite(channelsToDown, channelsToUp):
    sleep(0.1)
    for row in channelsToDown:
        #logging.info("Setting up channel " + str(row) + " to PUD_DOWN. ")
        GPIO.setup(row, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for column in channelsToUp:
        #logging.info("Setting up channel " + str(column) + " to PUD_UP. ")
        GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.setup(column, GPIO.OUT)


rows = [7,6,12,13,19]
columns = [21,8,5,16,26,20]
channelEnums = [G.BCM21,G.BCM07,G.BCM06,G.BCM12,G.BCM13,G.BCM19,G.BCM08,G.BCM05,G.BCM16,G.BCM26,G.BCM20]
values = [0,0,0,0,0,0,0,0,0,0]

lock = False

logging.info("Setting up Kodi client")

host = config.get("xbmc", "host")
port = config.getint("xbmc", "port")

logging.info("host: " + str(host))
logging.info("port: " + str(port))

# Create an XBMCClient object and connect
xbmc = XBMCClient("OldPhone", "/etc/lirc/osmc-remote-lircd.png")
xbmc.connect()

setReadWrite(rows, columns)

channelVal = G.NONE
previousChannelVal = G.NONE
previousRow = G.NONE

def row_changed(button, i):
    global channelVal
    
    #switch columns to input to read the values
    setReadWrite(columns, rows)
    
    #now read columns
    for column in columns:
        value = GPIO.input(column)
        if value:
            logging.info("column " + str(channelEnums[i]))
            channelVal = channelVal + channelEnums[i]
        i = i + 1;

    logging.info("Button event: " + str(channelVal))
    if button == G.NONE:
        xbmc.release_button()
    else:
        try:
            global mapping
            print(kbmapping[channelVal])
            xbmc.send_keyboard_button(button=kbmapping[channelVal])
        except:
            logging.warning("value invalid")
        sleep(0.025)

    #switch back to reading rows  
    setReadWrite(rows, columns)


def start():
    global channelVal
    global previousChannelVal
    global previousRow

    setReadWrite(rows, columns)

    i = 0
    for row in rows:
        value = GPIO.input(row)
        if value:
            logging.info("row " + str(channelEnums[i]))
            channelVal = channelVal + channelEnums[i]
        i = i + 1

    if previousRow <> channelVal & channelVal:
        # Keep track of row to check changes
        previousRow = channelVal;
        row_changed(channelVal, i)
        previousChannelVal = channelVal    
    
    channelVal = G.NONE
    lock = False

lock = False

channelVal = G.NONE
previousChannelVal = G.NONE

while True:
    start()
    sleep(0.05)
    pass
