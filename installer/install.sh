#!/bin/bash

serviceFolder="/home/osmc/.kodi/addons/service.keypad"

echo "installing..."

echo "copying new files"
if [ ! -d $serviceFolder ]
	then
		echo "creating $serviceFolder"
		mkdir $serviceFolder
fi

echo "copying program files"
cp ../program/* $serviceFolder/

if [ ! -f $serviceFolder/keypad.config ] || [ "$1" == "f" ]
	then
		echo "copying config"
		cp ./keypad.config $serviceFolder/keypad.config
fi

echo "Done"