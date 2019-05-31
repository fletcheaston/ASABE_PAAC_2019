#Created by Fletcher Easton

from Position import *;

def stopMotors(motorSerial):
    setMotorSpeed(motorSerial, 0, 0, 0, 0);

def setDirectionSpeed(motorSerial, direction, speed):
    if(direction == "RIGHT"):
        setMotorSpeed(motorSerial, speed, -1 * speed, -1 * speed, speed);
    elif(direction == "FORWARD"):
        setMotorSpeed(motorSerial, -1 * speed, -1 * speed, speed, speed);
    elif(direction == "BACKWARD"):
        setMotorSpeed(motorSerial, speed, speed, -1 * speed, -1 * speed);
    elif(direction == "LEFT"):
        setMotorSpeed(motorSerial, -1 * speed, speed, speed, -1 * speed);
    else:
        print("Invalid direction: {!r}".format(direction));
        setMotorSpeed(motorSerial, 0, 0, 0, 0);

def setMotorSpeed(motorSerial, frontRightSpeed, backRightSpeed, backLeftSpeed, frontLeftSpeed):
    string = "S " + str(frontRightSpeed) + " " + str(backRightSpeed) + " " + str(backLeftSpeed) + " " + str(frontLeftSpeed) + " ";
    writeSerialString(motorSerial, string);

def writeSerialString(motorSerial, string):
    bytes = string.encode();
    motorSerial.write(bytes);
