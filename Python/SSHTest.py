import serial
import time
from Motors import *

robotSerial = serial.Serial(port="/dev/ttyUSB1", baudrate=57600, timeout=0.1);
validDirections = ["FORWARD", "BACKWARD", "LEFT", "RIGHT"];

while(True):
    
    direction = None;
    while(True):
        direction = input("Enter a direction: ").upper();
        if(direction in validDirections):
            break;
        print("Not a valid ")
    
    speed = None;
    while(speed is None):
        try:
            speed = int(input("Enter a speed: "));
        except:
            print("Not an integer. Try again.");
            speed = None;

    setDirectionSpeed(robotSerial, direction, speed);
    
    time.sleep(0.1);
