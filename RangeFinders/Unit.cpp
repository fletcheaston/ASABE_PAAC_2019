// Created by Fletcher EASTon

#include "Unit.h"

#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

using namespace std;

long microsecondsToInches(long microseconds)
{
   return(microseconds / 74 / 2);
}

Unit::Unit(double width, double height)
{
   dimension = Dimension(width, height);
}

Position Unit::getPosition()
{
   pinMode(pingPins[NORTH], OUTPUT);
   digitalWrite(pingPins[NORTH], LOW);
   delayMicroseconds(2);
   digitalWrite(pingPins[NORTH], HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPins[NORTH], LOW);
   pinMode(echoPins[NORTH], INPUT);
   long northDuration = pulseIn(echoPins[NORTH], HIGH);
   long northInches = microsecondsToInches(northDuration);

   pinMode(pingPins[WEST], OUTPUT);
   digitalWrite(pingPins[WEST], LOW);
   delayMicroseconds(2);
   digitalWrite(pingPins[WEST], HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPins[WEST], LOW);
   pinMode(echoPins[WEST], INPUT);
   long westDuration = pulseIn(echoPins[WEST], HIGH);
   long westInches = microsecondsToInches(westDuration);

   Position tempPosition = Position(northInches + getHeight() / 2, westInches + getWidth() / 2);

   return(tempPosition);
}

double Unit::getWidth()
{
   return(dimension.getWidth());
}

double Unit::getHeight()
{
   return(dimension.getHeight());
}

void Unit::setDirectionFinder(int pingPin, int echoPin, String direction)
{
   if(direction == "NORTH")
   {
      pingPins[NORTH] = pingPin;
      echoPins[NORTH] = echoPin;
   }
   if(direction == "EAST")
   {
      pingPins[EAST] = pingPin;
      echoPins[EAST] = echoPin;
   }
   if(direction == "SOUTH")
   {
      pingPins[SOUTH] = pingPin;
      echoPins[SOUTH] = echoPin;
   }
   if(direction == "WEST")
   {
      pingPins[WEST] = pingPin;
      echoPins[WEST] = echoPin;
   }
}
