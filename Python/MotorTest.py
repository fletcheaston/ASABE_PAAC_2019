# Created by Fletcher Easton

from Motors import *;
import time;
import serial;

motorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);

speed = 255;

time.sleep(5);

while(motorSerial.in_waiting > 0):
    time.sleep(0.1);
    print(motorSerial.readline().decode());

time.sleep(1);

print("Forward");
setDirectionPosition(motorSerial, "FORWARD", 500, 255);

time.sleep(1);

motorSerial.write(b"M");

time.sleep(0.1);

while(motorSerial.in_waiting > 0):
    time.sleep(0.1);
    print(motorSerial.readline().decode());
