// Created by Fletcher Easton
// Designed for Arduino Nano
// Reads data from four TOF sensors (using I2C)
// Reads data from two LIDAR sensors (using I2C)

#define DEBUG

#ifdef DEBUG
  #define DEBUG_PRINT(x) Serial.println(x);
#else
  #define DEBUG_PRINT(x)
#endif

#include <Arduino.h>
#include <Wire.h>
#include "Adafruit_VL53L0X.h"
#include <LIDARLite.h>

#define tofBackLeftShutDown 24
#define tofBackRightShutDown 26
#define tofFrontLeftShutDown 30
#define tofFrontRightShutDown 28

Adafruit_VL53L0X tofBackLeft = Adafruit_VL53L0X();
Adafruit_VL53L0X tofBackRight = Adafruit_VL53L0X();
Adafruit_VL53L0X tofFrontLeft = Adafruit_VL53L0X();
Adafruit_VL53L0X tofFrontRight = Adafruit_VL53L0X();

#define lidarLeftShutdown 23
#define lidarRightShutdown 22

LIDARLite lidarLeft;
LIDARLite lidarRight;

void setupTof()
{
    pinMode(tofFrontLeftShutDown, OUTPUT);
    pinMode(tofFrontRightShutDown, OUTPUT);
    pinMode(tofBackLeftShutDown, OUTPUT);
    pinMode(tofBackRightShutDown, OUTPUT);

    delay(10);

    digitalWrite(tofFrontLeftShutDown, LOW);
    digitalWrite(tofFrontRightShutDown, LOW);
    digitalWrite(tofBackLeftShutDown, LOW);
    digitalWrite(tofBackRightShutDown, LOW);

    delay(10);

    digitalWrite(tofFrontLeftShutDown, HIGH);
    digitalWrite(tofFrontRightShutDown, HIGH);
    digitalWrite(tofBackLeftShutDown, HIGH);
    digitalWrite(tofBackRightShutDown, HIGH);

    delay(10);

    digitalWrite(tofFrontLeftShutDown, HIGH);
    digitalWrite(tofFrontRightShutDown, LOW);
    digitalWrite(tofBackLeftShutDown, LOW);
    digitalWrite(tofBackRightShutDown, LOW);

    tofFrontLeft.begin(0x35);

    delay(50);

    digitalWrite(tofFrontRightShutDown, HIGH);

    tofFrontRight.begin(0x39);

    delay(50);

    digitalWrite(tofBackLeftShutDown, HIGH);

    tofBackLeft.begin(0x43);

    delay(50);

    digitalWrite(tofBackRightShutDown, HIGH);

    tofBackRight.begin(0x47);

    delay(100);
    
}

void setupLidar()
{
    pinMode(lidarLeftShutdown, OUTPUT);
    pinMode(lidarRightShutdown, OUTPUT);
  
    delay(10);
  
    digitalWrite(lidarLeftShutdown, LOW);
    digitalWrite(lidarRightShutdown, LOW);
  
    delay(10);
  
    digitalWrite(lidarLeftShutdown, HIGH);
  
    lidarLeft.begin(4, true);
  
    lidarLeft.setI2Caddr(0x66, 1, 0x62);
  
    delay(50);
  
    digitalWrite(lidarRightShutdown, HIGH);
  
    lidarRight.begin(4, true);
  
    lidarRight.setI2Caddr(0x64, 1, 0x62);
  
    delay(50);
}

void printI2Cdevices()
{
    // Print available devices over i2c.
    byte count = 0;

    for (byte i = 1; i < 120; i++)
    {

        Wire.beginTransmission(i);
        if (Wire.endTransmission() == 0)
        {
            Serial.print("Found address: ");
            Serial.print(i, DEC);
            Serial.print(" (0x");
            Serial.print(i, HEX);
            Serial.println(")");
            count++;
            delay (1);
        }
    }
    
    Serial.println ("Done.");
    Serial.print ("Found ");
    Serial.print (count, DEC);
    Serial.println (" device(s).");
}

void setup()
{
    Serial.begin(57600);
    
    Wire.begin();
    
    setupTof();

    setupLidar();

    printI2Cdevices();
}

void loop()
{
    Serial.println(getTofData() + getLidarData());
}

String getLidarData()
{
    String lidarData = "";
  
    lidarData = lidarData + String(lidarLeft.distance(true, 0x66));

    delay(10);
    
    lidarData = lidarData + ",";
    
    lidarData = lidarData + String(lidarRight.distance(true, 0x64));

    delay(10);
  
    return(lidarData);
}

String getTofData()
{
    String tofData = "";
    VL53L0X_RangingMeasurementData_t measure;
        
    tofBackLeft.rangingTest(&measure);

    delay(10);
    
    if (measure.RangeStatus != 4 && measure.RangeMilliMeter != 0 && measure.RangeMilliMeter != 8191)
    {
        tofData = tofData + String(measure.RangeMilliMeter);
    }
    else
    {
        tofData = tofData + "???";
    }
    
    tofData = tofData + ",";
    
    tofBackRight.rangingTest(&measure);

    delay(10);
    
    if (measure.RangeStatus != 4 && measure.RangeMilliMeter != 0 && measure.RangeMilliMeter != 8191)
    {
      tofData = tofData + String(measure.RangeMilliMeter);
    }
    else
    {
        tofData = tofData + "???";
    }
    
    tofData = tofData + ",";
    
    tofFrontLeft.rangingTest(&measure);

    delay(10);
    
    if (measure.RangeStatus != 4 && measure.RangeMilliMeter != 0 && measure.RangeMilliMeter != 8191)
    {
        tofData = tofData + String(measure.RangeMilliMeter);
    }
    else
    {
        tofData = tofData + "???";
    }
    
    tofData = tofData + ",";
    
    tofFrontRight.rangingTest(&measure);

    delay(10);
    
    if (measure.RangeStatus != 4 && measure.RangeMilliMeter != 0 && measure.RangeMilliMeter != 8191)
    {
        tofData = tofData + String(measure.RangeMilliMeter);
    }
    else
    {
        tofData = tofData + "???";
    }

    tofData = tofData + ",";
    
    return(tofData);
}
