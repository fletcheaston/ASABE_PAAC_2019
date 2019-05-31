#Created by Fletcher Easton

from Position import *;

# Passes the speed of 0 to all motors.
def stopMotors(motorSerial):
    setMotorSpeed(motorSerial, 0, 0, 0, 0);

# Moves the robot in one of four predefined ways. Direction is local to the robot.
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

# Sets all motors to their respective passed-in speeds.
def setMotorSpeed(motorSerial, frontRightSpeed, backRightSpeed, backLeftSpeed, frontLeftSpeed):
    string = "S " + str(frontRightSpeed) + " " + str(backRightSpeed) + " " + str(backLeftSpeed) + " " + str(frontLeftSpeed) + " ";
    writeSerialString(motorSerial, string);
    
# Sets all motors to one passed-in speed.
def setMotorSpeed(motorSerial, allSpeed):
    string = "S " + str(allSpeed) + " " + str(allSpeed) + " " + str(allSpeed) + " " + str(allSpeed) + " ";
    writeSerialString(motorSerial, string);

# Moves all motors to their respective passed-in positions, at their respective passed-in speeds.
def setMotorPosition(motorSerial, frPos, frSpeed, brPos, brSpeed, blPos, blSpeed, flPos, flSpeed):
    string = "P " + str(frPos) + " " + str(frSpeed) + " " + str(brPos) + " " + str(brSpeed) + " " + str(blPos) + " " + str(blSpeed) + " " + str(flPos) + " " + str(flSpeed) + " ";
    writeSerialString(motorSerial, string);

# Moves all motors to their respective passed-in positions, at the same speed.
def setMotorPosition(motorSerial, frPos, brPos, blPos, flPos, allSpeed):
    string = "P " + str(frPos) + " " + str(allSpeed) + " " + str(brPos) + " " + str(allSpeed) + " " + str(blPos) + " " + str(allSpeed) + " " + str(flPos) + " " + str(allSpeed) + " ";
    writeSerialString(motorSerial, string);

# Moves all motors to the same position, at the same speed.
def setMotorPosition(motorSerial, allPos, allSpeed):
    string = "P " + str(allPos) + " " + str(allSpeed) + " " + str(allPos) + " " + str(allSpeed) + " " + str(allPos) + " " + str(allSpeed) + " " + str(allPos) + " " + str(allSpeed) + " ";
    writeSerialString(motorSerial, string);

# Reads the motor positons (and speeds) from the MegaPi and returns
def getMotorPosition(motorSerial):
    
    motorSerial.write(b"M");
    
    time.sleep(0.1);
    
    motorSpeeds = motorSerial.readline().decode().strip().split(' ');
    motorPositions = motorSerial.readline().decode().strip().split(' ');
    motorPositions[0] = int(motorPositions[0]);
    motorPositions[1] = int(motorPositions[1]);
    motorPositions[2] = int(motorPositions[2]);
    motorPositions[3] = int(motorPositions[3]);

    return(motorPositions);
    
def setMotorPositionDelta(motorSerial, frPos, brPos, blPos, flPos, allSpeed):
    currentPos = getMotorPosition(motorSerial);
    newfrPos = frPos + currentPos[0];
    newbrPos = brPos + currentPos[1];
    newblPos = blPos + currentPos[2];
    newflPos = flPos + currentPos[3];
    
    setMotorPosition(motorSerial, newfrPos, newbrPos, newblPos, newflPos, allSpeed);
    
def setMotorPositionDelta(motorSerial, allPos, allSpeed):
    currentPos = getMotorPosition(motorSerial);
    newfrPos = allPos + currentPos[0];
    newbrPos = allPos + currentPos[1];
    newblPos = allPos + currentPos[2];
    newflPos = allPos + currentPos[3];
    
    setMotorPosition(motorSerial, newfrPos, newbrPos, newblPos, newflPos, allSpeed);
    
def writeSerialString(motorSerial, string):
    bytes = string.encode();
    motorSerial.write(bytes);
