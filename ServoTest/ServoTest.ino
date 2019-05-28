/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object

  myservo.write(160);
  
  Serial.begin(57600);

}

void loop()
{
  
  if(Serial.available())
  {
    char a = Serial.read();

    switch(a)
    {
      case 'U':
      {
        myservo.write(130);
        Serial.println("Servo Angle: " + String(myservo.read()));
      }
      break;

      case 'D':
      {
        myservo.write(160);
        Serial.println("Servo Angle: " + String(myservo.read()));
      }
      break;

      default:
      {
        Serial.println("Servo Angle: " + String(myservo.read()));
      }
      break;
    }
  }
}

