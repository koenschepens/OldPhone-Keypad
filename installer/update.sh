#!/bin/sh

cd /usr/bin/oldphone/OldPhone-Keypad

git update-server-info >> /var/log/keypadUpdater.log
git pull >> /var/log/keypadUpdater.log

cd /usr/bin/oldphone/OldPhone-Keypad/installer
./install.sh
