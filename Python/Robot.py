# Created by Fletcher Easton

import os;
import time;
import serial;
from Position import *;
from Dimension import *;
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

        self.neutralY = 55;
        self.nextPosition = Position(0, 0);
        self.phase = "Wait";
        self.xDirection = 1;

        self.speed = 50;
        self.frSpeed = self.speed;
        self.brSpeed = self.speed;
        self.blSpeed = self.speed;
        self.flSpeed = self.speed;
        self.rotation = 0;

        self.setupMotorSerial();
        self.readSideAndPosition();

        self.taskPositions = [Position(300, 80), Position(40, 15), Position(150, 30)];
        self.taskCount = 0;

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


    def moveToPosition(self, position):
        self.nextPosition = position;
        self.phase = "GoToNeutral";


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


    def moveToX(self, xPosition, exit, tolerance=3):
        if(abs(self.position.x - xPosition) > tolerance):
            if(self.position.x - xPosition > 0):
                self.xDirection = -1;
                Motors.setMotorSpeed(self.motorSerial, self.frSpeed, self.brSpeed, -1 * self.blSpeed, -1 * self.flSpeed);
            elif(self.position.y - xPosition < 0):
                self.yDirection = 1;
                Motors.setMotorSpeed(self.motorSerial, -1 * self.frSpeed, -1 * self.brSpeed, self.blSpeed, self.flSpeed);
        else:
            Motors.stopMotors(self.motorSerial);
            time.sleep(0.1);
            self.phase = exit;


    def updateMovement(self):
        if(self.phase == "Wait"):
            pass;

        elif(self.phase == "GoToNeutral"):
            self.moveToY(self.neutralY, "TraverseNeutral", tolerance=5);

        elif(self.phase == "TraverseNeutral"):
            self.moveToX(self.nextPosition.x, "WallMash", tolerance=2);

        elif(self.phase == "WallMash"):
            if(self.nextPosition.y < self.position.y):
                self.phase = "WallMashBottom";
            else:
                self.phase = "WallMashTop";
        elif(self.phase == "WallMashTop"):
            self.moveToY(96, "ExitNeutral", tolerance=3);
        elif(self.phase == "WallMashBottom"):
            self.moveToY(0, "ExitNeutral", tolerance=3);

        elif(self.phase == "ExitNeutral"):
            self.moveToY(self.nextPosition.y, "ReadjustX", tolerance=3);

        elif(self.phase == "ReadjustX"):
            self.moveToX(self.nextPosition.x, "Wait", tolerance=1);


    def updateRotation(self):
        max_speed_adjustment = 20;
        max_angle = 90;
        proportional_adjustment = self.rotation / max_angle *  max_speed_adjustment * self.xDirection;

        self.frSpeed = self.speed + proportional_adjustment;
        self.brSpeed = self.speed + proportional_adjustment;
        self.flSpeed = self.speed - proportional_adjustment;
        self.blSpeed = self.speed - proportional_adjustment;


    def stop(self):
        Motors.stopMotors(self.motorSerial);


if __name__ == '__main__':
    robot = Robot();

    while(True):
        robot.readSideAndPosition();
        robot.updateMovement();
        robot.updateRotation();
        print(robot.position.toString() + " : " + str(robot.rotation));
        print(str(robot.frSpeed) + " " + str(robot.brSpeed) + " " + str(robot.flSpeed) + " " + str(robot.blSpeed));
        if(robot.phase == "Wait"):
            if(robot.taskCount < len(robot.taskPositions)):
                robot.moveToPosition(robot.taskPositions[robot.taskCount]);
                robot.taskCount = robot.taskCount + 1;
