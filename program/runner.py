import os
import xbmc
import logging

import xbmc
 
xbmc.executebuiltin('Notification(Hello World,This is a simple example of notifications,5000,/script.hellow.world.png)')

addonFolder = "/home/osmc/.kodi/addons/service.keypad/" 

os.system('sudo python ' + addonFolder + 'keypad.py')
