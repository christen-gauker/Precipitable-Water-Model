#! bin/bash/
while getopts "i" opt; do
	case "${opt}" in
    i)
        cd ./iniarduino/
        chmod 0755 install.sh
        sudo ./install.sh
        iniarduino
        cd ../
        ;;
        
