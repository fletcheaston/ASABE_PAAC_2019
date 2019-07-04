# Created by Fletcher Easton

import os;
import time;
import serial;
from Position import *;
import Motors;
from Robot import *;


if __name__ == '__main__':
    robot = Robot();

    while(True):
        time.sleep(0.1);
        robot.readSideAndPosition();
        robot.updateMovement();
        robot.updateRotation();

        print(robot.position.toString() + " : " + str(robot.rotation));
        print("Next Position: " + robot.taskPositions[robot.taskCount - 1].toString());
        print(robot.phase);

#        if(abs(robot.rotation) > 5):
 #           Motors.rotate(robot.motorSerial, -1 * robot.rotation / 2, robot.speed);
  #          time.sleep(0.25);

        if(robot.phase == "Wait"):
            if(robot.taskCount < len(robot.taskPositions)):
                robot.moveToPosition(robot.taskPositions[robot.taskCount]);
                robot.taskCount = robot.taskCount + 1;
