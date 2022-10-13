import serial
import time

device = serial.Serial("COM10", 115200, rtscts=False)

while True:

    print(device.readline(), device.read())

    time.sleep(0.5)
