# Created by Fletcher Easton

class Position:
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

    def __repr__(self):
        return("Position(X:{!r}, Y:{!r})".format(self.x, self.y));
