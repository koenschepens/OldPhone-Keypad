#!/bin/sh

now=$(date +"%m_%d_%Y_%T")
echo "********* update.sh **********" >> /var/log/keypadUpdater.log
echo $now >> /var/log/keypadUpdater.log
echo $USER >> /var/log/keypadUpdater.log

cd /usr/bin/oldphone/OldPhone-Keypad

git pull 

cd /usr/bin/oldphone/OldPhone-Keypad/installer
./install.sh
