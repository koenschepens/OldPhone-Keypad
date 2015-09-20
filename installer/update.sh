#!/bin/sh

now=$(date +"%m_%d_%Y_%T")
echo "********* update.sh **********" >> ~/keypadUpdater2.log

cd /usr/bin/oldphone/OldPhone-Keypad

git pull 

cd /usr/bin/oldphone/OldPhone-Keypad/installer
./install.sh
