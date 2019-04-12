// Created by Fletcher Easton
#ifndef _POSITIONCLASS_H
#define _POSITIONCLASS_H

#include <WString.h>

class Position
{
   public:
      Position(double x, double y);
      double getX();
      double getY();
      String toString();

   private:
      double xPos;
      double yPos;
};

#endif
