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

        self.speed = 50;
        self.frSpeed = self.speed;
        self.brSpeed = self.speed;
        self.blSpeed = self.speed;
        self.flSpeed = self.speed;

        self.setupMotorSerial();
        self.updateNavigationData();

        self.phase = "MoveToPlant";

        self.plantLocations = [Position(35,15), Position(45, 15), Position(55, 15)];
        self.plantIndex = 0;


    def setupMotorSerial(self):
        self.motorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);

        time.sleep(5);

        while(self.motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(self.motorSerial.readline().decode());

        time.sleep(1);


    def update(self):
        self.updateNavigationData();
        self.updateSpeedsForRotation();
        self.checkPhase();
        self.move();


    def updateNavigationData(self):
        try:
            os.rename(self.dataFile, self.atomicDataFile);

            with open(self.atomicDataFile, "r") as f:
                self.side = f.readline().strip();
                readings = f.readline().strip().split(",");
                self.position = Position(float(readings[0]), float(readings[1]));
                self.rotation = float(f.readline().strip());

        except:
            pass;


    def updateSpeedsForRotation(self):
        max_speed_adjustment = 20;
        max_angle = 30;
        proportional_adjustment = self.rotation / max_angle *  max_speed_adjustment;

        self.frSpeed = self.speed + max_speed_adjustment * proportional_adjustment;
        self.brSpeed = self.speed + max_speed_adjustment * proportional_adjustment;
        self.flSpeed = self.speed - max_speed_adjustment * proportional_adjustment;
        self.blSpeed = self.speed - max_speed_adjustment * proportional_adjustment;


    def checkPhase(self):
        if(self.phase == "Wait"):
            pass;

        if(self.phase == "MoveToPlant"):
            self.moveToLocation(self.plantLocations[self.plantIndex], "MoveOverPlant");

        if(self.phase == "MoveOverPlant"):
            pass;

        if(self.phase == "PickupPlant"):
            pass;

        if(self.phase == "MoveToCenter"):
            pass;

        if(self.phase == "MoveAlongCenter"):
            pass;

        if(self.phase == "MoveToZone"):
            pass;

        if(self.phase == "DropPlant"):
            pass;


    def moveToLocation(self, location, exit, tolerance=2):
        if(abs(self.position.y - location.y) > tolerance):
            self.moveToY(location.y, exit, tolerance);
        elif(abs(self.position.x - location.x) > tolerance):
            self.moveToX(location.x, exit, tolerance);


    def moveToY(self, yPosition, exit, tolerance=2):
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
                Motors.setMotorSpeed(self.motorSerial, -1 * self.frSpeed, -1 * self.brSpeed, -1 * self.blSpeed, -1 * self.flSpeed);
            elif(self.position.y - xPosition < 0):
                Motors.setMotorSpeed(self.motorSerial, self.frSpeed, self.brSpeed, self.blSpeed, self.flSpeed);

        else:
            Motors.stopMotors(self.motorSerial);
            time.sleep(0.1);
            self.phase = exit;


    def stop(self):
        Motors.stopMotors(self.motorSerial);


if __name__ == '__main__':
    robot = Robot();
    try:
        while(True):
            robot.update();
    except:
        robot.stop();
