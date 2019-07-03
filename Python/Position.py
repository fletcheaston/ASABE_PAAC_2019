# Created by Fletcher Easton

class Position:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
 
    def toString(self):
        return("{!r},{!r}".format(self.x, self.y));
