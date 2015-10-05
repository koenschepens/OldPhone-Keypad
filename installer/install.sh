#!/bin/bash

serviceFolder="/home/osmc/.kodi/addons/service.keypad"

echo "installing..."

echo "copying new files"
if [ ! -d $serviceFolder ]
	then
		mkdir $serviceFolder
fi

cp ../program/* $serviceFolder/

if [ ! -f $serviceFolder/keypad.config ]
	then
		cp ./keypad.config $serviceFolder/keypad.config
fi

echo "Done"
