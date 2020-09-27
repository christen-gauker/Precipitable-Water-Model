from numpy import *
import serial, time
from datetime import datetime, timedelta

tau      = 10 # Temporal resolution (1 measurement/tau seconds)
dt       = 2 # Time offset (records data every dt seconds)
n        = 0 # index
data1    = []

fname       = "../data/file.txt"
f           = open(fname, "a+", buffering=1)

ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600)

#ser = serial.Serial(port="/dev/serial/by-id/usb-Arduino_LLC_Arduino_Micro-if00", baudrate=9600)

def rw_Serial(data):
    line = ser.readline();
    line = line.decode("utf-8")
    try:
        data.append(float(line.strip("\n")))
    except ValueError:
        pass

while n < 10:
    now      = datetime.now()
    measure1 = datetime.strptime("17:37:30", "%H:%M:%S") + timedelta(seconds=(tau * n))
    end      = measure1 + timedelta(seconds=dt)
    send     = measure1 + timedelta(seconds=dt*2)

    if now.time().strftime("%H:%M:%S") == str(measure1.time()):
        rw_Serial(data1)
    elif now.time().strftime("%H:%M:%S") == str(end.time()):
        f.write(str(measure1.time()) + "," + str(round(mean(array(data1)), 2)) + "\n")
        n = n + 1
        data1 = []
        continue
    else:
        continue
