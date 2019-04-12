// Created by Fletcher Easton

#include "Position.h"

using namespace std;

Position::Position(double x, double y)
{
   xPos = x;
   yPos = y;
}

double Position::getX()
{
   return(xPos);
}

double Position::getY()
{
   return(yPos);
}

String Position::toString()
{
   return("X: " + String(xPos) + " Y: " + String(yPos));
}
