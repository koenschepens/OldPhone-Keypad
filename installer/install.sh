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
if [ ! -f /usr/share/oldkeypad ]
	then
		mkdir /usr/share/oldkeypad
fi
if [ ! -f /usr/share/oldkeypad/kbdout.config ]
	then
		cp ./kbdout.config /usr/share/oldkeypad/kbdout.config
fi

cp ./keypadd.sh /etc/init.d/keypadd
chmod 777 /etc/init.d/keypadd

echo "enabling oldkeypad service"
/etc/init.d/oldkeypad start