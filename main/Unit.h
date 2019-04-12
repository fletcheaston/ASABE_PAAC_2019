// Created by Fletcher Easton

#ifndef UNITCLASS_H
#define UNITCLASS_H

#include "Position.h"
#include "Dimension.h"
#include <Arduino.h>


class Unit
{
   public:
      Unit(double width, double height);
      Position getPosition();
      double getWidth();
      double getHeight();
      void setDirectionFinder(int pingPin, int echoPin, String direction);

   private:
      Dimension dimension;

      int pingPins[4];
      int echoPins[4];

};

#endif
