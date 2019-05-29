# Created by Fletcher Easton

from Motors import *;
import time;
import serial;

try:
    motorSerial = serial.Serial('/dev/tty.wchusbserial1410', 57600, timeout=0.1);
    
    speed = 255;

    time.sleep(5);


    while(True):
        print("Forward");
        setDirectionSpeed(motorSerial, "FORWARD", speed);
        
        time.sleep(1);

        motorSerial.write(b"M");
        
        time.sleep(0.1);
        
        while(motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(motorSerial.readline().decode());

        time.sleep(10);

        print("Backward");
        setDirectionSpeed(motorSerial, "BACKWARD", speed);
        
        time.sleep(1);
        
        motorSerial.write(b"M");
                
        time.sleep(0.1);
        
        while(motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(motorSerial.readline().decode());
            
        time.sleep(10);
        
        print("Left");
        setDirectionSpeed(motorSerial, "LEFT", speed);
        
        time.sleep(1);
        
        motorSerial.write(b"M");
                
        time.sleep(0.1);
        
        while(motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(motorSerial.readline().decode());
            
        time.sleep(10);
        
        print("Right");
        setDirectionSpeed(motorSerial, "RIGHT", speed);
        
        time.sleep(1);
        
        motorSerial.write(b"M");
                
        time.sleep(0.1);
        
        while(motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(motorSerial.readline().decode());
            
        time.sleep(10);

except:
    pass;
