import serial
import time
from Motors import *
import sys

def speedSetCommand(args):
    global robotSpeed;
    
    try:
        robotSpeed = int(args[1]);
        print("Speed set to " + str(robotSpeed));
    except:
        print("Not a valid speed.");

def velocityCommand(robotSerial, args):
    validDirections = ["FORWARD", "BACKWARD", "LEFT", "RIGHT"];
    global robotSpeed;
    
    try:
        if(args[1] in validDirections):
            direction = args[1];
            
            setDirectionSpeed(robotSerial, direction, robotSpeed);
            
        else:
            print("Not a valid direction.");
    
    except:
        print("Not enough arguments. Direction and speed required.");

    
def positionCommand(robotSerial, args):
    validDirections = ["FORWARD", "BACKWARD", "LEFT", "RIGHT"];
    global robotSpeed;
    
    try:
        
        if(args[1] in validDirections):
            direction = args[1];
            
            try:
                distance = int(args[2]);
            
                setDirectionPosition(robotSerial, direction, distance, robotSpeed);
            
            except:
                print("Not a valid distance.");
            
        else:
            print("Not a valid direction.");
    
    except:
        print("Bad arguments. Direction, distance, and speed required.");
        
def rotateCommand(robotSerial, args):
    global robotSpeed;
    
    try:
        
        try:
            angle = int(args[1]);
            
            rotate(robotSerial, angle, robotSpeed);
            
        except:
            print("Not a valid angle.");
    
    except:
        print("Not enough arguments. Angle and speed required.");

def motorDataCommand(robotSerial):
    print(readMotorData(robotSerial));

def stopCommand(robotSerial):
    print("Stopping robot.");
    stopMotors(robotSerial);

def main():
    global robotSpeed = 100;
    global robotSerial = serial.Serial(port="/dev/ttyUSB0", baudrate=57600, timeout=0.1);

    time.sleep(5);

    while(robotSerial.in_waiting > 0):
        print(robotSerial.readline().decode().strip());

    while(True):
            
        command = input("Enter a command: ").upper().split(" ");
        
        if(command[0] == "STOP"):
            stopCommand(robotSerial);
        elif(command[0] == "SPEED"):
            speedSetCommand(command);
        elif(command[0] == "VELOCITY"):
            velocityCommand(robotSerial, command);
        elif(command[0] == "POSITION"):
            positionCommand(robotSerial, command);
        elif(command[0] == "ROTATE"):
            rotateCommand(robotSerial, command);
        elif(command[0] == "MOTOR"):
            motorDataCommand(robotSerial);
        elif(command[0] == "QUIT"):
            stopCommand(robotSerial);
            sys.exit(0);

        time.sleep(0.1);


if __name__== "__main__":
    main();