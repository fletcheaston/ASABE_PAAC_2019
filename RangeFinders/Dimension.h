// Created by Fletcher Easton
#ifndef _DIMENSIONCLASS_H
#define _DIMENSIONCLASS_H

class Dimension
{
   public:
      Dimension(double width, double height);
      double getWidth();
      double getHeight();

   private:
      double myWidth;
      double myHeight;
};

#endif
