import cv2;
import numpy as np;
from time import sleep;

from Robot import *;
from Plant import *;

def drawAndDisplay(robot, plants):
    board_image = img = cv2.imread('Board.png',cv2.IMREAD_COLOR)

    for p in plants:
        board_image = p.drawPlant(board_image);

    board_image = robot.drawRobot(board_image);

    height, width, _ = board_image.shape;

    board_image = cv2.resize(board_image, (width * 2, height * 2));

    cv2.imshow("Board", board_image);
    cv2.waitKey(1);

def main():
    robot = Robot(20, 15);

    plants_x = [64, 82, 100, 118, 136, 154, 172, 190, 208, 226, 244, 262, 280, 298, 316, 334, 352, 370, 388, 406, 424];
    plants_y = 95;
    plants = [];

    for x in plants:
    	if(x == 244):
    		all_plants.append(Plant(x, plants_y, "GOLD"));
    	else:
    		all_plants.append(Plant(x, plants_y));

    while(True):

        drawAndDisplay(robot, plants);
        sleep(0.05);

if __name__ == '__main__':
    main()
