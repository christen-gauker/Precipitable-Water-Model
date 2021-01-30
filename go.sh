#! bin/bash/
while getopts "ac" opt; do
	case "${opt}" in
    a)
				sudo sed -i 's/raspberrypi/ursa-major/g' /etc/hostname
				sudo sed -i 's/raspberrypi/ursa-major/g' /etc/hosts
                sudo mv ./major_src/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf 
				sudo apt-get install python3-pip python3-dev libatlas-base-dev
				sudo pip3 install numpy pyserial

				sudo reboot
        ;;
	c) 
		vpnstart
		vpnstop
		;;
	esac
done
