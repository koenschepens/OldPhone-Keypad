import os
import logging
addonFolder = "/home/osmc/.kodi/addons/service.keypad/" 

logging.basicConfig(filename='keypad.log',level=logging.INFO)

logging.info("starting keypad")

os.system('sudo python keypad.py')
