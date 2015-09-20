#!/bin/bash

clear

echo "installing..."

echo "disabling oldkeypad services"
/etc/init.d/oldkeypad stop

echo "deleting existing oldkeypad files"
rm /etc/init.d/oldkeypad

echo "copying new files"
mkdir /usr/share/oldkeypad
cp ./kbdout.config /usr/share/oldkeypad/kbdout.config

cp ./keypadd.sh /etc/init.d/keypadd
chmod 777 /etc/init.d/keypadd

echo "enabling oldkeypad service"
/etc/init.d/oldkeypad start