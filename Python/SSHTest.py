import serial
import time
from Motors import *

robotSerial = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0.1);
validDirections = ["FORWARD", "BACKWARD", "LEFT", "RIGHT"];

while(True):
    
    direction = None;
    while(True):
        direction = input("Enter a direction: ").upper();
        if(direction == "STOP"):
            stopMotors(robotSerial);
        elif(direction in validDirections):
            break;
        else:
            print("Not a valid direction. Try again.");
    
    speed = None;
    while(speed is None):
        try:
            speed = int(input("Enter a speed: "));
        except:
            print("Not an integer. Try again.");
            speed = None;

    setDirectionSpeed(robotSerial, direction, speed);
    
    time.sleep(0.1);
