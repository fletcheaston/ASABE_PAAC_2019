import serial
import time
from Motors import *

def speedCommand(robotSerial):
    direction = None;
    while(True):
        direction = input("Enter a direction: ").upper();
        if(direction in validDirections):
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
    
def positionCommand(robotSerial):
    position = None;
    while(position is None):
        try:
            position = int(input("Enter a position: "));
        except:
            print("Not an integer. Try again.");
            speed = None;
    
    speed = None;
    while(speed is None):
        try:
            speed = int(input("Enter a speed: "));
        except:
            print("Not an integer. Try again.");
            speed = None;

    setMotorPositionDelta(robotSerial, position, speed);

def stopCommand(robotSerial):
    print("Stopping robot.");
    stopMotors(robotSerial);

robotSerial = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0.1);
validDirections = ["FORWARD", "BACKWARD", "LEFT", "RIGHT"];

while(True):
    
    command = input("Enter a command: ").upper();
    
    if(command == "SPEED"):
        speedCommand(robotSerial);
    elif(command == "STOP"):
        stopCommand(robotSerial);
    elif(command == "POSITION"):
        positionCommand(robotSerial);
        
    
    time.sleep(0.1);
