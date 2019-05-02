# Created by Fletcher Easton
import random;
import cv2;

from Position import *;
from Dimension import *;

class Plant:
    def __init__(self, x, y, color=None):
        self.position = Position(x, y);
        self.dimension = Dimension(6, 6);
        if(color == None):
            self.color = random.choice(["RED", "GREEN"])
        else:
            self.color = color;

    def __repr__(self):
        return("Plant(Position: {!r}, Color: {!r})".format(self.position, self.color));

    def drawPlant(self, image):
        height = image.shape[0];
        width = image.shape[1];
        color = None;

        if(self.color == "RED"):
            color = (0,0,255);
        if(self.color == "GREEN"):
            color = (0,255,0);
        if(self.color == "GOLD"):
            color = (0,215,255);

        cv2.rectangle(image, (int(self.position.x - self.dimension.width / 2), int(self.position.y - self.dimension.height / 2)), (int(self.position.x + self.dimension.width / 2), int(self.position.y + self.dimension.height / 2)), color, 3);


        return(image);
