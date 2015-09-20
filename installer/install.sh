#!/bin/bash

clear

echo "installing..."

echo "disabling oldkeypad services"

echo "deleting existing oldkeypad files"
if [ -f /etc/init.d/oldkeypad ]
  then
	/etc/init.d/oldkeypad stop
    rm /etc/init.d/oldkeypad
fi
if [ -f /etc/init.d/keypadd ]
  then
	/etc/init.d/keypadd stop
    rm /etc/init.d/keypadd
fi

echo "copying new files"
if [ ! -d /usr/share/keypad ]
	then
		mkdir /usr/share/keypad
fi

if [ ! -f /usr/share/keypad/keypad.config ]
	then
		cp ./keypad.config /usr/share/keypad/keypad.config
fi

cp ./keypadd.sh /etc/init.d/keypadd
chmod 777 /etc/init.d/keypadd

echo "enabling keypadd service"
/etc/init.d/keypadd start