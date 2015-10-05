import os
import xbmc
import logging

addonFolder = "/home/osmc/.kodi/addons/service.keypad/" 

config = ConfigParser.RawConfigParser()
configFile = addonFolder + 'keypad.config'
config.read(configFile)

host = config.get("xbmc", "host")
port = config.getint("xbmc", "port")

xbmc = XBMCClient("OldPhone", "/etc/lirc/osmc-remote-lircd.png")
xbmc.connect()

xbmc.executebuiltin("Notification('Title','Message')")

os.system('sudo python keypad.py')
