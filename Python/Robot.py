# Created by Fletcher Easton

# Import Python libraries
import cv2;
import serial;
from time import sleep;

# Import custom libraries
from Dimension import *;
from Position import *;
from Gripper import *;

class Robot:
    def __init__(self, width, height):
        self.serial = serial.Serial('/dev/tty.usbmodem14401', 115200, timeout=0.1);

        self.dimension = Dimension(width, height);

        self.position = Position(0, 0);

        self.distance_weight = 0.5;

        self.grippers = [Gripper(0,0)];


    def drawRobot(self, image):
        self.updatePosition(1);

        print(self.position);

        height = image.shape[0];
        width = image.shape[1];

        cv2.rectangle(image, (int(self.position.x - self.dimension.width / 2), int(self.position.y - self.dimension.height / 2)), (int(self.position.x + self.dimension.width / 2), int(self.position.y + self.dimension.height / 2)), (255, 255, 0), 3);

        return(image);

    def updatePosition(self, count):
        if(count > 0):

            measurement = readSerial(self.serial);

            try:
                tof = int(measurement.split(":")[0]);
                lidar = int(measurement.split(":")[1]);
                rf = int(measurement.split(":")[2]);

                # If the reading is greater than 60 cm, the readings are less accurate. Use the readings from the other side then.
                if(tof < 60):
                    # Updates the robot's y position. Because readings are on the south side, we have to subtract the reading from 122 to get the correct position.
                    self.position.y = self.position.y * self.distance_weight + (122 - 4 - tof) * (1 - self.distance_weight);

                # Lidar readings are taken from the west side.
                self.position.x = self.position.x * self.distance_weight + (lidar + self.dimension.width / 2) * (1 - self.distance_weight);

                # If the reading is greater than 60 cm, the readings are less accurate. Use the readings from the other side then.
                if(rf < 60):
                    # Updates the robot's y position. Readings are taken on the north side.

                    #self.position.y = self.position.y * self.distance_weight + rf * (1 - self.distance_weight);
                    pass;

            except:
                pass;

            self.updatePosition(count - 1);

        else:
            self.serial.reset_input_buffer();


def readSerial(ser):
    message = ser.readline().decode().strip();

    return(message);
