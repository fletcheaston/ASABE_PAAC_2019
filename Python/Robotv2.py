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

        self.speed = 100;
        self.frSpeed = -1 * self.speed;
        self.brSpeed = -1 * self.speed;
        self.blSpeed = 1 * self.speed;
        self.flSpeed = 1 * self.speed;
        self.rotation = 0;

        self.setupMotorSerial();
        self.updateNavigationData();


    def setupMotorSerial(self):
        self.motorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);

        time.sleep(5);

        while(self.motorSerial.in_waiting > 0):
            time.sleep(0.1);
            print(self.motorSerial.readline().decode());

        time.sleep(1);


    def updateNavigationData(self):
        try:
            os.rename(self.dataFile, self.atomicDataFile);

            with open(self.atomicDataFile, "r") as f:
                self.side = f.readline().strip();
                print(self.side);
                readings = f.readline().strip().split(",");
                print(readings);
                self.position = Position(float(readings[0]), float(readings[1]));
                self.rotation = float(f.readline().strip());
                print(self.rotation);
        except:
            pass;


    def updateSpeedsForRotation(self):
        max_speed_adjustment = abs(self.speed);
        max_angle = 90;
        proportional_adjustment = self.rotation / max_angle *  max_speed_adjustment;

        self.frSpeed = int(-1 * (self.speed + proportional_adjustment));
        self.brSpeed = int(-1 * (self.speed + proportional_adjustment));
        self.flSpeed = int(1 * (self.speed - proportional_adjustment));
        self.blSpeed = int(1 * (self.speed - proportional_adjustment));


    def move(self):
        Motors.setMotorSpeed(self.motorSerial, self.frSpeed, self.brSpeed, self.blSpeed, self.flSpeed);


    def printSpeeds(self):
        print("FR: {!r}".format(self.frSpeed));
        print("FL: {!r}".format(self.flSpeed));
        print("BR: {!r}".format(self.brSpeed));
        print("BL: {!r}".format(self.blSpeed));
        print(self.rotation);


    def stop(self):
        Motors.stopMotors(self.motorSerial);


if __name__ == '__main__':
    robot = Robot();

    try:
        while(True):
            robot.updateNavigationData();
            robot.updateSpeedsForRotation();
            robot.move();
            robot.printSpeeds();
    except:
        robot.stop();
