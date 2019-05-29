# Created by Fletcher Easton

from Motors import *;
import time;
import serial;

try:
    motorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);

    time.sleep(5);


    while(True):
        print("Forward");
        setDirectionSpeed(motorSerial, "FORWARD", 50);
        time.sleep(10);

        motorSerial.write(b"M");
        while(motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(motorSerial.readline().decode());


        print("Backward");
        setDirectionSpeed(motorSerial, "BACKWARD", 50);
        time.sleep(10);

except:
    pass;
