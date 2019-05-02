#include "Adafruit_VL53L0X.h"

#include <Wire.h>
#include <LIDARLite.h>

LIDARLite myLidarLite;

const int pingPin = 13; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 12; // Echo Pin of Ultrasonic Sensor
Adafruit_VL53L0X lox = Adafruit_VL53L0X();

void setup() {
 
  myLidarLite.begin(0, true); // Set configuration to default and I2C to 400 kHz
  myLidarLite.configure(0); // Change this number to try out alternate configurations
  
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (! Serial) {
    delay(1);
  }
  
  Serial.println("Adafruit VL53L0X test");
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  // power 
  Serial.println(F("VL53L0X API Simple Ranging example\n\n")); 
}


void loop() {
  int tof = readTOF();
  int lidar = readLIDAR();
  int rf = readRF();

  Serial.println(String(tof) + ":" + String(lidar) + ":" + String(rf));

  delay(50);
    
}

int readTOF()
{
  VL53L0X_RangingMeasurementData_t measure;
    
  lox.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if (measure.RangeStatus != 4) {  // phase failures have incorrect data
    return(int(measure.RangeMilliMeter / 10));
  } else {
    return(-1);
  }

}

int readLIDAR()
{
  // Take a measurement with receiver bias correction
  myLidarLite.distance();
  
  float average_distance = 0;

  for(int i = 0; i < 10; i++)
  {
    average_distance += float(myLidarLite.distance(false));
  }

  // Take a measurements without receiver bias correction and print to serial terminal
  return(int(average_distance / 10));
}


long readRF()
{
   long duration, cm;
   pinMode(pingPin, OUTPUT);
   digitalWrite(pingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   pinMode(echoPin, INPUT);
   duration = pulseIn(echoPin, HIGH);
   cm = microsecondsToCentimeters(duration);
   return(int(cm));
}

long microsecondsToCentimeters(long microseconds)
{
   return microseconds / 29 / 2;
}
