import serial
import time
from Motors import *
import sys

def speedCommand(robotSerial, args):
    validDirections = ["FORWARD", "BACKWARD", "LEFT", "RIGHT"];

    try:
        if(args[1] in validDirections):
            direction = args[1];
            try:
                speed = int(args[2]);
                setDirectionSpeed(robotSerial, direction, speed);

            except:
                print("Not a valid speed.");
            
        else:
            print("Not a valid direction.");
    
    except:
        print("Not enough arguments. Direction and speed required.");

    
def positionCommand(robotSerial, args):
    try:
        
        try:
            position = int(args[1]);
            
            try:
                speed = int(args[2]);
                setMotorPositionDelta(robotSerial, position, position, position, position, speed);

            except:
                print("Not a valid speed.");
            
        except:
            print("Not a valid position.");
    
    except:
        print("Not enough arguments. Position and speed required.");
        
def rotateCommand(robotSerial, args):
    try:
        
        try:
            angle = int(args[1]);
            
            try:
                speed = int(args[2]);
                rotate(robotSerial, angle, speed);

            except:
                print("Not a valid speed.");
            
        except:
            print("Not a valid angle.");
    
    except:
        print("Not enough arguments. Angle and speed required.");


def stopCommand(robotSerial):
    print("Stopping robot.");
    stopMotors(robotSerial);

robotSerial = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0.1);

time.sleep(5);

while(robotSerial.in_waiting > 0):
    print(robotSerial.readline().decode().strip());

while(True):
        
    command = input("Enter a command: ").upper().split(" ");
    
    if(command[0] == "STOP"):
        stopCommand(robotSerial);
    elif(command[0] == "SPEED"):
        speedCommand(robotSerial, command);
    elif(command[0] == "POSITION"):
        positionCommand(robotSerial, command);
    elif(command[0] == "ROTATE"):
        rotateCommand(robotSerial, command);
    elif(command[0] == "QUIT"):
        stopCommand(robotSerial);
        sys.exit(0);
        
    
    time.sleep(0.1);
