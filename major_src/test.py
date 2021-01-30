from numpy import *
import serial, time
from datetime import datetime, timedelta
import subprocess

tau      = 10 # Temporal resolution (1 measurement/tau seconds)
dt       = 2 # Time offset (records data every dt seconds)
n        = 0 # ind

fname       = "/home/pi/Precipitable-Water-Model/data/file.txt"
f           = open(fname, "a+", buffering=1)

def rw_Serial(data, ser):
    line = ser.readline();
    line = line.decode("utf-8")

    print(line)
    reading = float(line.strip("\n"))
    data.append(reading)

measure1 = datetime.now() + timedelta(seconds=10) 
#measure1 = datetime.strptime('14:13:00', '%H:%M:%S')
def time_trigger():
	while True:
	    ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600)
	    data1    = []
	    now1      = datetime.now()
	    #measure1 = datetime.strptime("10:16:30", "%H:%M:%S") + timedelta(seconds=(tau * n))
	    if now1.time().strftime("%H:%M:%S") == str(measure1.time().strftime("%H:%M:%S")):
	      ser.write(bytes('Y', 'utf-8'))
	      rw_Serial(data1, ser)
	      f.write(str(measure1.time().strftime('%H:%M:%S')) + "," + str(round(mean(array(data1)), 2)) + "\n")
	      measure1 = (measure1 + timedelta(seconds=(tau)))
	      subprocess.call('scp /home/pi/Precipitable-Water-Model/data/file.txt ursa_major@129.138.36.123:/home/projects/Precipitable-Water-Model/auto', shell=True)
	      continue
	    else:
	        continue

def user_trigger():
	while True:
		io = input("Activate?\n>> ")
		if io == "y":
			ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600)
			data1 = []
			ser.write(bytes('Y', 'utf-8'))
			rw_Serial(data1, ser)
			print(round(mean(array(data1)), 2))
		else:
			print("URSA Major not active")
			break

user_trigger()
