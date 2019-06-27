# Created by Fletcher Easton

from Motors import *;
import time;
import serial;

motorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);

dirs = ["FORWARD", "LEFT", "BACKWARD", "RIGHT"];
counter = 0;
timeCounter = 0;
speed = 255;

time.sleep(5);

while(motorSerial.in_waiting > 0):
    time.sleep(0.1);
    print(motorSerial.readline().decode());

time.sleep(1);

while(True):
    timeCounter = time.time();

    setDirectionSpeed(motorSerial, dirs[counter % 4], 255);

    while(timeCounter < time.time() - 5):
        motorSerial.write(b"M");

        time.sleep(0.25);

        while(motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(motorSerial.readline().decode().strip());

    counter = counter + 1;
