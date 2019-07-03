#!/usr/bin/python3
# Created by Fletcher Easton

import math;
import time;
import serial;
import os;
from Position import *;

class Sensors:
    def __init__(self):
        self.sensorSerial = None;
        self.dataFile = "SensorData.db";

        self.setupSensorSerial();

        self.side = None;
        self.position = Position(0,0);
        self.rotation = 0;

        self.blt_readings = [];
        self.brt_readings = [];
        self.flt_readings = [];
        self.frt_readings = [];
        self.max_reading_count = 3;
        self.sensor_spacing = 12.86;

        self.left_rotations = [];
        self.right_rotations = [];
        self.left_weight = 0.5;
        self.right_weight = 0.5;

        self.blt_offset = 0;
        self.brt_offset = 0;
        self.flt_offset = 0;
        self.frt_offset = 0;

        self.determineOffset();

        if(self.side == "Left"):
            self.position = Position(0, 0);
        elif(self.side == "Right"):
            self.position = Position(483.87, 0);


    def setupSensorSerial(self):
        self.sensorSerial = serial.Serial('/dev/ttyUSB1', 57600, timeout=0.5);

        time.sleep(3);

        while(self.sensorSerial.in_waiting > 0):
            time.sleep(0.1);
            self.sensorSerial.readline().decode().strip();

        time.sleep(1);


    def determineOffset(self):
        for _ in range(0, self.max_reading_count):
            self.parseData(self.sensorSerial.readline().decode().strip());

        avg_blt = sum(self.blt_readings) / len(self.blt_readings);
        avg_flt = sum(self.flt_readings) / len(self.flt_readings);
        avg_brt = sum(self.brt_readings) / len(self.brt_readings);
        avg_frt = sum(self.frt_readings) / len(self.frt_readings);

        if(avg_blt < 10 and avg_flt < 10):
            self.side = "Right";
            self.blt_offset = avg_blt;
            self.flt_offset = avg_flt;
        if(avg_brt < 10 and avg_frt < 10):
            self.side = "Left";
            self.brt_offset = avg_brt;
            self.frt_offset = avg_frt;
        if(self.side is None):
            self.side = "Left";
            print("No offset.");

        print(self.side);
        print(self.frt_offset);
        print(self.brt_offset);
        print(self.flt_offset);
        print(self.blt_offset);


    def readData(self):
        while(self.sensorSerial.in_waiting > 0):
            self.parseData(self.sensorSerial.readline().decode().strip());


    def parseData(self, data):
        backLeftTof = None;
        backRightTof = None;
        frontLeftTof = None;
        frontRightTof = None;
        leftLidar = None;
        rightLidar = None;

        try:
            backLeftTof = max(float(data.split(",")[3]) / 10 - self.blt_offset, 0);
            backRightTof = max(float(data.split(",")[0]) / 10 - self.brt_offset, 0);
            frontLeftTof = max(float(data.split(",")[1]) / 10 - self.flt_offset, 0);
            frontRightTof = max(float(data.split(",")[2]) / 10 - self.frt_offset, 0);

            all_weights = backLeftTof + backRightTof + frontLeftTof + frontRightTof;
            self.left_weight = 1 - (backLeftTof + frontLeftTof) / all_weights;
            self.right_weight = 1 - (backRightTof + frontRightTof) / all_weights;

            self.blt_readings.insert(0, backLeftTof);
            self.brt_readings.insert(0, backRightTof);
            self.flt_readings.insert(0, frontLeftTof);
            self.frt_readings.insert(0, frontRightTof);
            if(len(self.blt_readings) > self.max_reading_count):
                del self.blt_readings[-1];
                del self.brt_readings[-1];
                del self.flt_readings[-1];
                del self.frt_readings[-1];

            if(backLeftTof == backRightTof == frontleftTof == frontRightTof):
                self.sensorSerial.write(b"R");

            leftLidar = int(data.split(",")[5]);
            rightLidar = int(data.split(",")[4]);

            print("Raw data: " + str(frontRightTof) + "," + str(backRightTof) + "," + str(frontLeftTof) + "," + str(backLeftTof) + "," + str(rightLidar) + "," + str(leftLidar));

            self.calculateRotation();

            x = self.position.x;
            y = self.position.y;

            if(self.side == "Left"):
                if(abs(leftLidar - rightLidar) > 5):
                    if(abs(leftLidar - x) <= 5 and abs(rightLidar - x) <= 5):
                        x = (leftLidar + rightLidar) / 2;
                    elif(abs(leftLidar - x) <= 5 and abs(rightLidar - x) > 5):
                        x = leftLidar;
                    elif(abs(leftLidar - x) > 5 and abs(rightLidar - x) <= 5):
                        x = rightLidar;
                    elif(abs(leftLidar - x) > 5 and abs(rightLidar - x) > 5):
                        #x = x;
                        x = (leftLidar + rightLidar) / 2;
                else:
                    x = (leftLidar + rightLidar) / 2;

            if(self.side == "Left"):
                y = (backRightTof + frontRightTof + (118.11 - (backLeftTof + 22.225)) + (118.11 - (frontLeftTof + 22.225))) / 4;


            self.position = Position(x,y);
        except:
            pass;


    def calculateRotation(self):
        cur_fl = self.flt_readings[0];
        cur_bl = self.blt_readings[0];
        cur_left_rotation = math.degrees(math.atan((cur_fl - cur_bl) / self.sensor_spacing));
        cur_fr = self.frt_readings[0];
        cur_br = self.brt_readings[0];
        cur_right_rotation = -1 * math.degrees(math.atan((cur_fr - cur_br) / self.sensor_spacing));

        self.left_rotations.insert(0, cur_left_rotation);
        self.right_rotations.insert(0, cur_right_rotation);
        if(len(self.left_rotations) > self.max_reading_count):
            del self.left_rotations[-1];
            del self.right_rotations[-1];

        self.rotation = (sum(self.left_rotations) / len(self.left_rotations)) * self.left_weight + (sum(self.right_rotations) / len(self.right_rotations)) * self.right_weight;

    def writeData(self):
        f = open(self.dataFile, 'w');
        f.write(self.side);
        f.write("\n");
        f.write(self.position.toString());
        f.write("\n");
        f.write(str(self.rotation));
        f.write("\n");
        f.flush();
        os.fsync(f.fileno());
        f.close();
#        print(self.position.toString());
#        print("Left rotations: " + str(self.left_rotations));
#        print("Right rotations: " + str(self.right_rotations));
#        print("Left weight: " + str(self.left_weight));
#        print("Right weight: " + str(self.right_weight));
        print("Avg rotation: " + str(self.rotation));
        time.sleep(0.2);
        print();


if __name__ == '__main__':
    sensor = Sensors();
    while(True):
        sensor.readData();
        sensor.writeData();

