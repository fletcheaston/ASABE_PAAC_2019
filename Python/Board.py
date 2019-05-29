# Created by Fletcher Easton

from Position import *;
from Dimension import *;
from Plant import *;
from Zone import *;

import random;

class Board:
    def __init__(self, dimension):
        self.dimension = dimension;
        self.plantList = [];
        
        for i in range(21):
            tempPos = Position(i * 10, 100);
            tempDim = Dimension(5, 5);
            tempColor = random.choice(["RED", "GREEN"]);
            if(i == 11):
                tempColor = "GOLD";
            self.plantList.append(Plant(tempPos, tempDim, tempColor));
        
        tempPos = Position(0, 0);
        tempDim = Dimension(100, 100);
        self.redZone = Zone(tempPos, tempDim, "RED");
        self.greenZone = Zone(tempPos, tempDim, "GREEN");