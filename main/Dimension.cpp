// Created by Fletcher Easton

#include "Dimension.h"

using namespace std;

Dimension::Dimension(double width, double height)
{
   myWidth = width;
   myHeight = height;
}

double Dimension::getWidth()
{
   return(myWidth);
}

double Dimension::getHeight()
{
   return(myHeight);
}
