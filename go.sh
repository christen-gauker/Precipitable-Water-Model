#! bin/bash/
while getopts ":major:minor" opt; do
	case "${opt}" in
    major)
				sudo sed -i 's/raspberrypi/ursa-major/g' /etc/hostname
				sudo sed -i 's/raspberrypi/ursa-major/g' /etc/hosts

				sudo cp ./major/bluetooth-auto-power@.service /etc/systemd/system/
				sudo sed -i 's/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd/ExecStart=\/usr\/lib\/bluetooth\/bluetoothd -C"/g' /etc/systemd/system/dbus-org.bluez.service

				sudo cp ./major/10-local.rules /etc/udev/rules.d/
				sudo cp ./major/obexpush.service /etc/systemd/system/
				# sudo apt-get update && sudo apt-get upgrade
				# sudo apt-get install bluez bluez-tools libbluetooth-dev gnome-bluetooth
				# bt-adapter --set Discoverable 1
				# bt-agent pair 5C:F3:70:9C:A5:0D
				# bt-obex -p 5C:F3:70:9C:A5:0D
				#bluetooth-sendto --device 5C:F3:70:9C:A5:0D ./data/file.txt

				sudo service bluetooth stop
				sudo bluetooth --compat

				systemctl --user start obex
				sudo systemctl --global enable obex
				sudo systemctl enable obexpush

				sudo apt-get install python3-pip python3-dev libatlas-base-dev
				sudo pip3 install numpy pyserial

        cd ./iniarduino/
        chmod 0755 install.sh
        sudo ./install.sh
        iniarduino
        cd ../

				sudo reboot
        ;;
		minor)
				sudo sed -i 's/raspberrypi/ursa-minor/g' /etc/hostname
				sudo sed -i 's/raspberrypi/ursa-minor/g' /etc/hosts

				{
					sleep 10s
					sudo killall obexpushd
				} & sudo obexpushd -B23 -o /bluetooth -n
			esac
		done
