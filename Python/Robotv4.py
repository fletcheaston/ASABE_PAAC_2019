# Created by Fletcher Easton

import os;
import time;
import serial;
from Position import *;
import Motors;


def bounded(num, lower, upper):
    if(num > upper):
        return(upper);
    if(num < lower):
        return(lower);
    return(num);


class Robot:
    def __init__(self):
        self.motorSerial = None;
        self.position = Position(0,0);
        self.side = "Left";
        self.dataFile = "SensorData.db";
        self.atomicDataFile = "AtomicSensorData.db";

        self.first = Position(30, 15);
        self.second = Position(225, 15);

        self.phase = "First";

        self.speed = 50;
        self.frSpeed = self.speed;
        self.brSpeed = self.speed;
        self.blSpeed = self.speed;
        self.flSpeed = self.speed;
        self.xDirection = 1;
        self.rotation = 0;

        self.setupMotorSerial();
        self.readSideAndPosition();


    def setupMotorSerial(self):
        self.motorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);

        time.sleep(5);

        while(self.motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(self.motorSerial.readline().decode());

        time.sleep(1);


    def readSideAndPosition(self):
        try:
            os.rename(self.dataFile, self.atomicDataFile);

            with open(self.atomicDataFile, "r") as f:
                self.side = f.readline().strip();
                readings = f.readline().strip().split(",");
                self.position = Position(float(readings[0]), float(readings[1]));
                self.rotation = float(f.readline().strip());
        except:
            pass;


    def moveToY(self, yPosition, exit, tolerance=3):
        if(abs(self.position.y - yPosition) > tolerance):
            if(self.position.y - yPosition > 0):
                Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - yPosition), self.speed);
            elif(self.position.y - yPosition < 0):
                Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - yPosition), self.speed);
        else:
            Motors.stopMotors(self.motorSerial);
            time.sleep(0.1);
            self.phase = exit;


    def moveToX(self, xPosition, exit, tolerance=2):
        if(abs(self.position.x - xPosition) > tolerance):
            if(self.position.x - xPosition > 0):
                self.xDirection = -1;
                Motors.setMotorSpeed(self.motorSerial, self.frSpeed, self.brSpeed, -1 * self.blSpeed, -1 * self.flSpeed);
            elif(self.position.y - xPosition < 0):
                self.xDirection = 1;
                Motors.setMotorSpeed(self.motorSerial, -1 * self.frSpeed, -1 * self.brSpeed, self.blSpeed, self.flSpeed);

        else:
            Motors.stopMotors(self.motorSerial);
            time.sleep(0.1);
            self.phase = exit;


    def reorient(self, exit):
        Motors.rotate(self.motorSerial, -1 * self.rotation, self.speed);
        time.sleep(0.1);
        self.phase = exit;


    def updateMovement(self):
        if(self.phase == "First"):
            if(abs(self.position.y - self.first.y) > 2):
                self.moveToY(self.first.y, "First", tolerance=2);
            elif(abs(self.position.x - self.first.x) > 5):
                self.moveToX(self.first.x, "Second", tolerance=5);
            else:
                self.phase = "Second";

        if(self.phase == "Second"):
            if(abs(self.position.y - self.second.y) > 2):
                self.moveToY(self.second.y, "Second", tolerance=2);
            elif(abs(self.position.x - self.second.x) > 5):
                self.moveToX(self.second.x, "First", tolerance=5);
            else:
                self.phase = "First";

        if(abs(self.rotation) > 3):
             Motors.rotate(self.motorSerial, -1 * self.rotation / 2, self.speed);


    def updateRotation(self):
        max_speed_adjustment = self.speed;
        max_angle = 90;
        proportional_adjustment = self.rotation / max_angle *  max_speed_adjustment * self.xDirection;
        distance_adjustment = (self.position.y - 15) * self.xDirection;

        self.frSpeed = self.speed + proportional_adjustment - distance_adjustment;
        self.brSpeed = self.speed + proportional_adjustment - distance_adjustment;
        self.flSpeed = self.speed - proportional_adjustment + distance_adjustment;
        self.blSpeed = self.speed - proportional_adjustment + distance_adjustment;



    def stop(self):
        Motors.stopMotors(self.motorSerial);


    def printSpeeds(self):
        print("FR: {!r}".format(self.frSpeed));
        print("FL: {!r}".format(self.flSpeed));
        print("BR: {!r}".format(self.brSpeed));
        print("BL: {!r}".format(self.blSpeed));


if __name__ == '__main__':
    robot = Robot();

    while(True):
        robot.readSideAndPosition();
        robot.updateMovement();
        robot.updateRotation();
#        robot.printSpeeds();
        print(robot.position.toString() + " : " + str(robot.rotation));
        print(robot.phase);
