#Created by Fletcher Easton

from Position import *;

def setDirectionSpeed(motorSerial, direction, speed):
    if(direction == "LEFT"):
        setMotorSpeed(motorSerial, speed, -1 * speed, -1 * speed, speed);
    if(direction == "FORWARD"):
        setMotorSpeed(motorSerial, speed, speed, -1 * speed, -1 * speed);
    if(direction == "BACKWARD"):
        setMotorSpeed(motorSerial, -1 * speed, -1 * speed, speed, speed);
    if(direction == "RIGHT"):
        setMotorSpeed(motorSerial, -1 * speed, speed, speed, -1 * speed);

def setMotorSpeed(motorSerial, frontRightSpeed, backRightSpeed, backLeftSpeed, frontLeftSpeed):
    motorSerial.write("S");
    motorSerial.write(String(frontRightSpeed) + " " + String(backRightSpeed) + " " + String(backLeftSpeed) + " " + String(frontLeftSpeed));

def moveVerticalPosition(motorSerial, currentPositionY, newPositionY):
    y_movement = newPositionY - currentPositionY;
    
    // Read current wheel positions from serial
    backLeftPos = 0;
    backRightPos = 0;
    frontLeftPos = 0;
    frontRightPos = 0;
    
    if(newPositionY > currentPositionY):
        y_movement = translateVerticalPosition(y_movement);
        motorSerial.write("P");
        motorSerial.write(String(
    



def translateVerticalPosition(pos):
    return(pos * 1);