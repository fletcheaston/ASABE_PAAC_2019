# Created by Fletcher Easton

import serial;
from Position import *;
from Dimension import *;
import Motors;

class Robot:
    def __init__(self):
        self.sensorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);
        self.motorSerial = serial.Serial('/dev/ttyUSB1', 57600, timeout=0.1);
        self.speed = 100;

        self.position = None;
        self.side = "Left";
        self.neutralPosition = None;
        # TODO: All this stuff.. so alot..
        # Read sensors and determine what the position is
        # Then, determine which side of the board we're on and rotate accordingly
        # Side is either left or right
        # Push back into corner to align along axes
        # neutralPosition is the position in the board where our robot can traverse safely in the X-direction. Allows for simplified pathfinding

        self.nextPlantIndex = None;
        # nextPlantIndex is the index of the closest plant in the plantlist Either 0 or 20


    def updateLocation(self):
        pass;
        # Read position from the shared file or database or whatever


    def moveToNeutralPosition(self):
        # Move close enough to the Y-position of the neutralPosition
        # Stops if we get within 3cm of the neutralPosition, and gives a 1cm buffer on either side to travel to. Allows for some margin of error
        while(abs(self.position.y - self.neutralPosition.y) > 3):

            if(self.side == "Left"):

                if(self.position.y - self.neutralPosition.y > 3):
                    # If the robot is above the neutralPosition on the left side, move right
                    Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - self.neutralPosition.y - 1), self.speed); #!!! May need to fix abs if problem?

                elif(self.position.y - self.neutralPosition.y < -3):
                    # If the robot is below the neutralPosition on the left side, move left
                    Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - self.neutralPosition.y - 1), self.speed);

            elif(self.side == "Right"):

                if(self.position.y - self.neutralPosition.y > 3):
                    # If the robot is above the neutralPosition on the right side, move right
                    Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - self.neutralPosition.y - 1), self.speed);

                elif(self.position.y - self.neutralPosition.y < -3):
                    # If the robot is below the neutralPosition on the left side, move left
                    Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - self.neutralPosition.y - 1), self.speed);

            # Delay for position to change as motors move the robot
            time.sleep(0.1);
            self.updateLocation();


    def moveXPosition(self, location):
        # Move close enough to the X-position of the location
        # Stops if we get within 1cm of the location.x, and gives a 1cm buffer on either side to travel to. Allows for some margin of error
        while(abs(self.position.x - location.x) > 1):

            if(self.side == "Left"):

                if(self.position.x - location.x > 1);
                    # If the robot is right of the location.x on the left side of the board, we move backward
                    Motors.setDirectionPosition(self.motorSerial, "BACKWARD", self.position.y - self.neutralPosition.y - 1, self.speed);

                elif(self.position.x - location.x < -1);
                    # If the robot is left of the location.x on the left side of the board, we move forward
                    Motors.setDirectionPosition(self.motorSerial, "FORWARD", self.position.y - self.neutralPosition.y - 1, self.speed);

            if(self.side == "Right"):

                if(self.position.x - location.x > 1);
                    # If the robot is right of the location.x on the right side of the board, we move forward
                    Motors.setDirectionPosition(self.motorSerial, "FORWARD", self.position.y - self.neutralPosition.y - 1, self.speed);

                elif(self.position.x - location.x < -1);
                    # If the robot is left of the location.x on the right side of the board, we move backward
                    Motors.setDirectionPosition(self.motorSerial, "BACKWARD", self.position.y - self.neutralPosition.y - 1, self.speed);

            # Delay for position to change as motors move the robot
            time.sleep(0.1);
            self.updateLocation();


    def moveYPosition(self, location):
        # Move close enough to the Y-position of the location
        # Stops if we get within 1cm of the location.y, and gives a 1cm buffer on either side to travel to. Allows for some margin of error
        while(abs(self.position.y - location.y) > 1):

            if(self.side == "Left"):

                if(self.position.y - location.y > 1):
                    # If the robot is above the location.y on the left side, move right
                    Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - location.y - 1), self.speed); # TODO: !!! May need to fix abs if problem?

                elif(self.position.y - location.y < -1):
                    # If the robot is below the location.y on the left side, move left
                    Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - location.y - 1), self.speed);

            elif(self.side == "Right"):

                if(self.position.y - location.y > 1):
                    # If the robot is above the location.y on the right side, move right
                    Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - location.y - 1), self.speed);

                elif(self.position.y - location.y < -1):
                    # If the robot is below the location.y on the left side, move left
                    Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - location.y - 1), self.speed);

            # Delay for position to change as motors move the robot
            time.sleep(0.1);
            self.updateLocation();


    def moveAgainstWall(self, location):
        # Moves against the closest wall, to realign with the axes
        if(self.side == "Left"):

            if(self.position.y - location.y > 1):
                # If the robot is above the location.y on the left side, move right into the lower wall
                Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - location.y + 5), self.speed);

            elif(self.position.y - location.y < -1):
                # If the robot is below the location.y on the left side, move left into the upper wall
                Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - location.y + 5), self.speed);

        elif(self.side == "Right"):

            if(self.position.y - location.y > 1):
                # If the robot is above the location.y on the right side, move right into the lower wall
                Motors.setDirectionPosition(self.motorSerial, "LEFT", abs(self.position.y - location.y + 5), self.speed);

            elif(self.position.y - location.y < -1):
                # If the robot is below the location.y on the left side, move left into the upper wall
                Motors.setDirectionPosition(self.motorSerial, "RIGHT", abs(self.position.y - location.y + 5), self.speed);

        # Delay for position to change as motors move the robot
        time.sleep(5); # TODO: Adjust sleep time for however large the distance is * some constant (must calculate/figure out)

        # TODO: Update our Y-position based on what wall we're pushing into


    def pauseMovement(self):
        Motors.stopMotors(self.motorSerial);
        # May need to adjust the delay. Minimize time waiting, but we don't want to rotate
        time.sleep(0.1);


    def moveToLocation(self, location):
        # We first move to the neutralPosition
        self.moveToNeutralPosition();

        # We stop the motors for a split second so we don't accidentally rotate when changing directions
        self.pauseMovement();

        # We then move to the correct X-position
        self.moveXPosition(location);

        # We stop the motors for a split second so we don't accidentally rotate when changing directions
        self.pauseMovement();

        # We then move against the correct wall, to fix any slight rotation problems
        self.moveAgainstWall(location);

        # We then move to the correct Y-position
        self.moveYPosition(location);

        # Now, we should be in the desired location with minimum misalignment from axes


    def moveToNextPlant(self, plantlist):
        nextPlant = plantlist[self.nextPlantIndex];

        # TODO: Adjust position to travel to, we don't want to run over our plant
        moveToLocation(nextPlant.position);
