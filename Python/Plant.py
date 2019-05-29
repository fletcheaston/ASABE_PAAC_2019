# Created by Fletcher Easton

from Position import *;
from Dimension import *;

class Plant:
    def __init__(self, position, dimension, color):
        self.position = position;
        self.dimension = dimension;
        self.color = color;
        self.inPosition = False;