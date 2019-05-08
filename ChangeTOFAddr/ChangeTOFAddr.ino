#include "Adafruit_VL53L0X.h"
#include <Wire.h>

Adafruit_VL53L0X sensor6 = Adafruit_VL53L0X();
Adafruit_VL53L0X sensor7 = Adafruit_VL53L0X();

void setup() {
  Serial.begin(115200);

  while (! Serial)
  {
    delay(1);
  }

  Wire.begin();

  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);

  // Reset all sensors by setting SHUTDOWN to LOW, then setting to HIGH
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);

  delay(10);

  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);

  delay(100);

  // Shutdown sensor7, keep sensor6 awake for address change.
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);

  // Change it's address, and start it up.
  sensor6.begin(0x27);

  delay(50);

  digitalWrite(7, HIGH);

  sensor7.begin(0x31);


  delay(500);

  byte count = 0;

  for (byte i = 1; i < 120; i++)
  {

    Wire.beginTransmission (i);
    if (Wire.endTransmission () == 0)
    {
      Serial.print ("Found address: ");
      Serial.print (i, DEC);
      Serial.print (" (0x");
      Serial.print (i, HEX);
      Serial.println (")");
      count++;
      delay (1);  // maybe unneeded?
    } // end of good response
  } // end of for loop
  Serial.println ("Done.");
  Serial.print ("Found ");
  Serial.print (count, DEC);
  Serial.println (" device(s).");

}


void loop()
{
  String tof6 = readTOFSensor(sensor6);
  String tof7 = readTOFSensor(sensor7);

  Serial.println(tof6 + " " + tof7);
}

String readTOFSensor(Adafruit_VL53L0X sensor)
{
  VL53L0X_RangingMeasurementData_t measure;
    
  sensor.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

  if(measure.RangeStatus != 4)
  {
    return(String(int(measure.RangeMilliMeter / 10)));
  }
}

