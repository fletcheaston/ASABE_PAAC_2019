// Created by Fletcher Easton

#include "Unit.h"

Unit robot(12, 12);

void setup()
{
   robot.setDirectionFinder(12, 13, "NORTH");
   robot.setDirectionFinder(10, 11, "WEST");
   Serial.begin(9600);
}

void loop()
{
   Serial.println(robot.getPosition().toString());
}
