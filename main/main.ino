// Created by Fletcher Easton

const int northPingPin = 13; // Trigger Pin of Ultrasonic Sensor
const int northEchoPin = 12; // Echo Pin of Ultrasonic Sensor
const int westPingPin = 11; // Trigger Pin of Ultrasonic Sensor
const int westEchoPin = 10; // Echo Pin of Ultrasonic Sensor
const bool readSerial = false;

void setup()
{
   Serial.begin(9600);
}

void loop()
{
  if(readSerial)
  {
    char in;
    if (Serial.available())
    {
      in = Serial.read();
      switch(in)
      {
        case 'N': Serial.println(readNorthRangeFinder());
        case 'W': Serial.println(readWestRangeFinder());
      }
      Serial.flush();
    }
  }
  else
  {
    //Serial.println(readNorthRangeFinder());
    Serial.println(readWestRangeFinder());
  }

}

long readNorthRangeFinder()
{
   long duration, inches;
   pinMode(northPingPin, OUTPUT);
   digitalWrite(northPingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(northPingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(northPingPin, LOW);
   pinMode(northEchoPin, INPUT);
   duration = pulseIn(northEchoPin, HIGH);
   inches = microsecondsToInches(duration);
   return(inches);
}

long readWestRangeFinder()
{
   long duration, inches;
   pinMode(westPingPin, OUTPUT);
   digitalWrite(westPingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(westPingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(westPingPin, LOW);
   pinMode(westEchoPin, INPUT);
   duration = pulseIn(westEchoPin, HIGH);
   inches = microsecondsToInches(duration);
   return(inches);
}

double microsecondsToInches(long microseconds)
{
   return(microseconds / 74 / 2);
}
