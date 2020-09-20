#! bin/bash/
while getopts "i" opt; do
	case "${opt}" in
    i)
				sudo apt-get install libopenobex1-dev bluez libbluetooth-dev
				sudo pip3 install bluez
				cd ./lightblue-0.4/
				python3 setup.py install
				cd ../

        cd ./iniarduino/
        chmod 0755 install.sh
        sudo ./install.sh
        iniarduino
        cd ../
        ;;
