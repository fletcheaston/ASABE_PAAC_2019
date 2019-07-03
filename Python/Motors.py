#Created by Fletcher Easton

from Position import *;
import time;


# The angle-constant for rotating the robot.
def angleConstant():
    return(1);


# The forward/backward-constant for moving the robot.
def longitudinalConstant():
    return(20.3491866233);


# The side-to-side-constant for moving the robot.
def lateralConstant():
    return(22.8258388496);


# Passes the speed of 0 to all motors.
def stopMotors(motorSerial):
    setMotorSpeed(motorSerial, 0, 0, 0, 0);


# Moves the robot in one of four predefined ways. Direction is local to the robot.
def setDirectionSpeed(motorSerial, direction, speed):
    if(direction == "RIGHT"):
        setMotorSpeed(motorSerial, speed,  -1 * speed, -1 * speed, speed);

    elif(direction == "FORWARD"):
        setMotorSpeed(motorSerial, -1 * speed, -1 * speed, speed, speed);

    elif(direction == "BACKWARD"):
        setMotorSpeed(motorSerial, speed, speed, -1 * speed, -1 * speed);

    elif(direction == "LEFT"):
        setMotorSpeed(motorSerial,  -1 * speed, speed, speed, -1 * speed);

    else:
        print("Invalid direction: {!r}".format(direction));
        setMotorSpeed(motorSerial, 0, 0, 0, 0);


# Moves the robot in one of four predefined ways. Direction is local to the robot. Distance is in centimeters.
def setDirectionPosition(motorSerial, direction, distance, speed):
    if(direction == "RIGHT"):
        adjustedDistance = int(lateralConstant() * distance);
        setMotorPositionDelta(motorSerial, adjustedDistance, -1 * adjustedDistance, -1 * adjustedDistance, adjustedDistance, speed);

    elif(direction == "FORWARD"):
        adjustedDistance = int(longitudinalConstant() * distance);
        setMotorPositionDelta(motorSerial, -1 * adjustedDistance, -1 * adjustedDistance, adjustedDistance, adjustedDistance, speed);

    elif(direction == "BACKWARD"):
        adjustedDistance = int(longitudinalConstant() * distance);
        setMotorPositionDelta(motorSerial, adjustedDistance, adjustedDistance, -1 * adjustedDistance, -1 * adjustedDistance, speed);

    elif(direction == "LEFT"):
        adjustedDistance = int(lateralConstant() * distance);
        setMotorPositionDelta(motorSerial, -1 * adjustedDistance, adjustedDistance, adjustedDistance, -1 * adjustedDistance, speed);

    else:
        print("Invalid direction: {!r}".format(direction));
        setMotorSpeed(motorSerial, 0, 0, 0, 0);

# Moves the robot in one of four predefined ways. Direction is local to the robot. Distance is in centimeters.
def setDirectionPositionAndSpeed(motorSerial, direction, distance, frSpeed, brSpeed, blSpeed, flSpeed):
    if(direction == "RIGHT"):
        adjustedDistance = int(lateralConstant() * distance);
        setMotorPositionDeltaAndSpeed(motorSerial, adjustedDistance, -1 * adjustedDistance, -1 * adjustedDistance, adjustedDistance, frSpeed, brSpeed, blSpeed, flSpeed);

    elif(direction == "FORWARD"):
        adjustedDistance = int(longitudinalConstant() * distance);
        setMotorPositionDeltaAndSpeed(motorSerial, -1 * adjustedDistance, -1 * adjustedDistance, adjustedDistance, adjustedDistance, frSpeed, brSpeed, blSpeed, flSpeed);

    elif(direction == "BACKWARD"):
        adjustedDistance = int(longitudinalConstant() * distance);
        setMotorPositionDeltaAndSpeed(motorSerial, adjustedDistance, adjustedDistance, -1 * adjustedDistance, -1 * adjustedDistance, frSpeed, brSpeed, blSpeed, flSpeed);

    elif(direction == "LEFT"):
        adjustedDistance = int(lateralConstant() * distance);
        setMotorPositionDeltaAndSpeed(motorSerial, -1 * adjustedDistance, adjustedDistance, adjustedDistance, -1 * adjustedDistance, frSpeed, brSpeed, blSpeed, flSpeed);

    else:
        print("Invalid direction: {!r}".format(direction));
        setMotorSpeed(motorSerial, 0, 0, 0, 0);

# Sets all motors to their respective passed-in speeds.
def setMotorSpeed(motorSerial, frontRightSpeed, backRightSpeed, backLeftSpeed, frontLeftSpeed):
    string = "S " + str(frontRightSpeed) + " " + str(backRightSpeed) + " " + str(backLeftSpeed) + " " + str(frontLeftSpeed) + " ";
    writeSerialString(motorSerial, string);


# Moves all motors to their respective passed-in positions, at their respective passed-in speeds.
def setMotorPosition(motorSerial, frPos, frSpeed, brPos, brSpeed, blPos, blSpeed, flPos, flSpeed):
    string = "P " + str(frPos) + " " + str(frSpeed) + " " + str(brPos) + " " + str(brSpeed) + " " + str(blPos) + " " + str(blSpeed) + " " + str(flPos) + " " + str(flSpeed) + " ";
    writeSerialString(motorSerial, string);


# Reads motor speed and position from the MegaPi and returns everything in a string.
def readMotorData(motorSerial):

    motorSerial.write(b"M");

    time.sleep(0.1);

    motorSpeeds = motorSerial.readline().decode().strip();
    motorPositions = motorSerial.readline().decode().strip();

    return("Speed: " + str(motorSpeeds) + "\nPosition: " + str(motorPositions));


# Reads the motor positons (and speeds) from the MegaPi and returns an array of positions.
def getMotorPosition(motorSerial):

    motorSerial.write(b"M");

    time.sleep(0.1);

    motorSpeeds = motorSerial.readline().decode().strip().split(',');
    motorPositions = motorSerial.readline().decode().strip().split(',');
    motorPositions[0] = int(motorPositions[0]);
    motorPositions[1] = int(motorPositions[1]);
    motorPositions[2] = int(motorPositions[2]);
    motorPositions[3] = int(motorPositions[3]);

    return(motorPositions);


# Adjusts relative motor positions.
def setMotorPositionDelta(motorSerial, frPos, brPos, blPos, flPos, allSpeed):
    currentPos = getMotorPosition(motorSerial);
    newfrPos = frPos + currentPos[0];
    newbrPos = brPos + currentPos[1];
    newblPos = blPos + currentPos[2];
    newflPos = flPos + currentPos[3];

    setMotorPosition(motorSerial, newfrPos, allSpeed, newbrPos, allSpeed, newblPos, allSpeed, newflPos, allSpeed);


def setMotorPositionDeltaAndSpeed(motorSerial, frPos, brPos, blPos, flPos, frSpeed, brSpeed, blSpeed, flSpeed):
    currentPos = getMotorPosition(motorSerial);
    newfrPos = frPos + currentPos[0];
    newbrPos = brPos + currentPos[1];
    newblPos = blPos + currentPos[2];
    newflPos = flPos + currentPos[3];

    setMotorPosition(motorSerial, newfrPos, frSpeed, newbrPos, brSpeed, newblPos, blSpeed, newflPos, flSpeed);


# Rotates the robot by a specified angle and speed.
def rotate(motorSerial, angle, speed):
    realAngle = int(angleConstant() * angle);
    setMotorPositionDelta(motorSerial, realAngle, realAngle, realAngle, realAngle, speed);


# Utility method to write data to the robot.
def writeSerialString(motorSerial, string):
    bytes = string.encode();
    motorSerial.write(bytes);

