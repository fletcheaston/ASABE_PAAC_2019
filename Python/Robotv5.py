# Created by Fletcher Easton

import os;
import time;
import serial;
from Position import *;
import Motors;


class Robot:
    def __init__(self):
        self.motorSerial = None;
        self.position = Position(0,0);
        self.side = "Left";
        self.dataFile = "SensorData.db";
        self.atomicDataFile = "AtomicSensorData.db";

        self.plantPositions = [Position(55, 12), Position(75, 12), Position(85, 12), Position(102, 12), Position(120, 12), Position(140, 12), Position(160, 12), Position(175, 12), Position(195, 12), Position(210, 12)];
        self.plantIndex = 0;

        self.zonePositions = [Position(10, 90), Position(20, 90), Position(30, 90), Position(40, 90), Position(50, 90), Position(60, 90), Position(70, 90), Position(80, 90), Position(90, 90), Position(100, 90)];
        self.zoneIndex = 0;

        self.phase = "MoveToPlant";

        self.speed = 25;
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
        if(self.phase == "Wait"):
            pass;

        if(self.phase == "MoveToPlant"):
            plant = self.plantPositions[self.plantIndex];
            if(abs(self.position.y - plant.y) > 2):
                self.moveToY(plant.y, "MoveToPlant", tolerance=2);
            elif(abs(self.position.x - plant.x) > 2):
                self.moveToX(plant.x, "PickupPlant", tolerance=2);
            else:
                self.phase = "PickupPlant";

        if(self.phase == "PickupPlant"):
            Motors.stopMotors(self.motorSerial);
            Motors.writeSerialString(self.motorSerial, "U");
            time.sleep(1);
            self.plantIndex = self.plantIndex + 1;
            if(self.plantIndex > len(self.plantPositions)):
                self.phase = "Wait";
            else:
                self.phase = "MoveToZone";

        if(self.phase == "MoveToZone"):
            zone = self.zonePositions[self.zoneIndex];
            if(abs(self.position.y - zone.y) > 2):
                self.moveToY(zone.y, "MoveToZone", tolerance=2);
            elif(abs(self.position.x - zone.x) > 2):
                self.moveToX(zone.x, "DropoffPlant", tolerance=2);
            else:
                self.phase = "DropoffPlant";

        if(self.phase == "DropoffPlant"):
            Motors.stopMotors(self.motorSerial);
            Motors.writeSerialString(self.motorSerial, "D");
            time.sleep(1);
            self.zoneIndex = self.zoneIndex + 1;
            if(self.zoneIndex > len(self.zonePositions)):
                self.phase = "Wait";
            else:
                self.phase = "MoveToPlant";

        if(abs(self.rotation) > 3):
            Motors.rotate(self.motorSerial, -1 * self.rotation / 2, self.speed);


    def updateRotation(self):
        max_speed_adjustment = self.speed;
        max_angle = 30;
        proportional_adjustment = self.rotation / max_angle *  max_speed_adjustment * self.xDirection;

        self.frSpeed = self.speed + proportional_adjustment;
        self.brSpeed = self.speed + proportional_adjustment;
        self.flSpeed = self.speed - proportional_adjustment;
        self.blSpeed = self.speed - proportional_adjustment;


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
        robot.printSpeeds();
        print(robot.position.toString() + " : " + str(robot.rotation));
        print(robot.phase);
        print(robot.plantPositions[robot.plantIndex].toString());
        time.sleep(0.1);
