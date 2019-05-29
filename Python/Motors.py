#Created by Fletcher Easton

from Position import *;

def setDirectionSpeed(motorSerial, direction, speed):
    if(direction == "LEFT"):
        setMotorSpeed(motorSerial, speed, -1 * speed, -1 * speed, speed);
    if(direction == "FORWARD"):
        setMotorSpeed(motorSerial, -1 * speed, -1 * speed, speed, speed);
    if(direction == "BACKWARD"):
        setMotorSpeed(motorSerial, speed, speed, -1 * speed, -1 * speed);
    if(direction == "RIGHT"):
        setMotorSpeed(motorSerial, -1 * speed, speed, speed, -1 * speed);

def setMotorSpeed(motorSerial, frontRightSpeed, backRightSpeed, backLeftSpeed, frontLeftSpeed):
    writeSerialString(motorSerial, "S");
    writeSerialString(motorSerial, str(frontRightSpeed) + " " + str(backRightSpeed) + " " + str(backLeftSpeed) + " " + str(frontLeftSpeed));

def writeSerialString(motorSerial, string):
    bytes = string.encode();
    motorSerial.write(bytes);
