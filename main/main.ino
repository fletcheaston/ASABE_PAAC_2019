// Created by Fletcher Easton

#include "Adafruit_VL53L0X.h"
#include <Wire.h>

Adafruit_VL53L0X tof_backward = Adafruit_VL53L0X();
Adafruit_VL53L0X tof_forward = Adafruit_VL53L0X();
float average_distance;
unsigned long pulseWidth;

String input;

int TOF_BACKWARD_PIN = 44;
int TOF_FORWARD_PIN = 42;

int LIDAR_LEFT_TRIGGER = 2;
int LIDAR_LEFT_MONITOR = 3;
int LIDAR_RIGHT_TRIGGER = 4;
int LIDAR_RIGHT_MONITOR = 5;

int EN_A_FORWARD = 13;
int IN1_FORWARD = 11;
int IN2_FORWARD = 10;
int IN3_FORWARD = 9;
int IN4_FORWARD = 8;
int EN_B_FORWARD = 12;

/*
int EN_A_BACKWARD = ;
int IN1_BACKWARD = ;
int IN2_BACKWARD = ;
int IN3_BACKWARD = ;
int IN4_BACKWARD = ;
int EN_B_BACKWARD = ;
*/

void setup()
{
  Serial.begin(115200); // Start serial communications

  while (! Serial)
  {
    delay(1);
  }

  Serial.println("Setting up LIDAR sensors...");

  setupLIDAR();

  Serial.println("Setting up TOF sensors...");

  setupTOF();

  Serial.println("Setting up motors...");

  setupForwardMotors();
  //setupBackwardMotors();

}

void setupLIDAR()
{
  pinMode(LIDAR_LEFT_TRIGGER, OUTPUT); // Set pin 2 as trigger pin
  digitalWrite(LIDAR_LEFT_TRIGGER, LOW); // Set trigger LOW for continuous read
  pinMode(LIDAR_LEFT_MONITOR, INPUT); // Set pin 3 as monitor pin

  pinMode(LIDAR_RIGHT_TRIGGER, OUTPUT); // Set pin 4 as trigger pin
  digitalWrite(LIDAR_RIGHT_TRIGGER, LOW); // Set trigger LOW for continuous read
  pinMode(LIDAR_RIGHT_MONITOR, INPUT); // Set pin 5 as monitor pin
}

void setupTOF()
{
  pinMode(TOF_BACKWARD_PIN, OUTPUT);
  pinMode(TOF_FORWARD_PIN, OUTPUT);

  // Reset all sensors by setting SHUTDOWN to LOW, then setting to HIGH
  digitalWrite(TOF_BACKWARD_PIN, LOW);
  digitalWrite(TOF_FORWARD_PIN, LOW);

  delay(10);

  digitalWrite(TOF_BACKWARD_PIN, HIGH);
  digitalWrite(TOF_FORWARD_PIN, HIGH);

  delay(10);

  // Shutdown sensor7, keep sensor6 awake for address change.
  digitalWrite(TOF_BACKWARD_PIN, HIGH);
  digitalWrite(TOF_FORWARD_PIN, LOW);

  // Change it's address, and start it up.
  tof_backward.begin(0x27);

  delay(10);

  digitalWrite(TOF_FORWARD_PIN, HIGH);

  tof_forward.begin(0x31);
}

void setupForwardMotors()
{
    pinMode(EN_A_FORWARD, OUTPUT);
    pinMode(IN1_FORWARD, OUTPUT);
    pinMode(IN2_FORWARD, OUTPUT);
    pinMode(IN3_FORWARD, OUTPUT);
    pinMode(IN4_FORWARD, OUTPUT);
    pinMode(EN_B_FORWARD, OUTPUT);
}

/*
void setupBackwardMotors()
{
    pinMode(EN_A_BACKWARD, OUTPUT);
    pinMode(IN1_BACKWARD, OUTPUT);
    pinMode(IN2_BACKWARD, OUTPUT);
    pinMode(IN3_BACKWARD, OUTPUT);
    pinMode(IN4_BACKWARD, OUTPUT);
    pinMode(EN_B_BACKWARD, OUTPUT);
}
*/

void loop()
{
    /*if(Serial.available())
    {
        input = Serial.readString();
        if(input == "Position")
        {
            printPosition();
        }
        else if(input == "Move")
        {
            readMove();
        }
    }*/
    printPosition();
}

void readMove()
{
    int motorLeftForward = 128 - Serial.read();
    if(motorLeftForward >= 0)
    {
        moveForwardLeft(1, motorLeftForward);
    }
    else
    {
        moveForwardLeft(-1, motorLeftForward);
    }

    int motorRightForward = 128 - Serial.read();
    if(motorRightForward >= 0)
    {
        moveForwardRight(1, motorRightForward);
    }
    else
    {
        moveForwardRight(-1, motorRightForward);
    }

    /*
    int motorLeftBackward = 128 - Serial.read();
    if(motorLeftForward >= 0)
    {
        moveForwardLeft(1, motorLeftBackward);
    }
    else
    {
        moveForwardLeft(-1, motorLeftBackward);
    }

    int motorRightBackward = 128 - Serial.read();
    if(motorLeftForward >= 0)
    {
        moveForwardLeft(1, motorRightBackward);
    }
    else
    {
        moveForwardLeft(-1, motorRightBackward);
    }
    */


}

void moveForwardLeft(int dir, int speed)
{
    if(dir == 1)
    {
        digitalWrite(IN1_FORWARD, HIGH);
        digitalWrite(IN2_FORWARD, LOW);
    }
    else
    {
        digitalWrite(IN1_FORWARD, LOW);
        digitalWrite(IN2_FORWARD, HIGH);
    }
    analogWrite(EN_A_FORWARD, speed);
}

void moveForwardRight(int dir, int speed)
{
    if(dir == 1)
    {
        digitalWrite(IN3_FORWARD, HIGH);
        digitalWrite(IN4_FORWARD, LOW);
    }
    else
    {
        digitalWrite(IN3_FORWARD, LOW);
        digitalWrite(IN4_FORWARD, HIGH);
    }
    analogWrite(EN_B_FORWARD, speed);
}

void printPosition()
{
    String lidar3 = getLidar(LIDAR_LEFT_MONITOR);
    String lidar5 = getLidar(LIDAR_RIGHT_MONITOR);
    String tof6 = readTOFSensor(tof_backward);
    String tof7 = readTOFSensor(tof_forward);

    Serial.println(lidar3 + " " + lidar5 + " " + tof6 + " " + tof7);
}

String getLidar(int monitor_pin)
{
  average_distance = 0;

  for(int i = 0;i < 3;i++)
  {
    pulseWidth = pulseIn(monitor_pin, HIGH); // Count how long the pulse is high in microseconds
    average_distance += pulseWidth / 10; // 10usec = 1 cm of distance
    delay(5);

  }

  return(String(int(average_distance / 3)));
}


String readTOFSensor(Adafruit_VL53L0X sensor)
{
  VL53L0X_RangingMeasurementData_t measure;
  average_distance = 0;

  for(int i = 0;i < 2;i++)
  {
    sensor.rangingTest(&measure, false); // pass in 'true' to get debug data printout!

    if(measure.RangeStatus != 4)
    {
      average_distance += measure.RangeMilliMeter / 10;
    }
    else
    {
      average_distance += 100;
    }
  }

  return(String(int(average_distance / 2)));
}
