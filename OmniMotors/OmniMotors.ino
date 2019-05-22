// Created by Fletcher Easton

#include "Adafruit_VL53L0X.h"
#include <Wire.h>

Adafruit_VL53L0X FrontLeftTof = Adafruit_VL53L0X();
Adafruit_VL53L0X FrontRightTof = Adafruit_VL53L0X();
Adafruit_VL53L0X BackLeftTof = Adafruit_VL53L0X();
Adafruit_VL53L0X BackRightTof = Adafruit_VL53L0X();

int frontLeftShutdown = 22;
int frontRightShutdown = 24;
int backLeftShutdown = 26;
int backRightShutdown = 28;


// Front Encoder Pins
int frontLeftEncoderA = 2;
int frontLeftEncoderB = 4;
int frontRightEncoderA = 3;
int frontRightEncoderB = 5;

// Back Encoder Pins
int backLeftEncoderA = 18;
int backLeftEncoderB = 16;
int backRightEncoderA = 19;
int backRightEncoderB = 17;

volatile long frontLeftEncoderPos = 0;
volatile long frontRightEncoderPos = 0;
volatile long backLeftEncoderPos = 0;
volatile long backRightEncoderPos = 0;

// Front Motor Pins
int ENA_Front = 13;      //Enable pin for first motor
int IN1 = 47;       //control pin for first motor
int IN2 = 49;       //control pin for first motor
int IN3 = 51;        //control pin for second motor
int IN4 = 53;        //control pin for second motor
int ENB_Front = 12;      //Enable pin for second motor

// Back Motor Pins
int ENA_Back = 11;      //Enable pin for first motor
int IN5 = 46;       //control pin for first motor
int IN6 = 48;       //control pin for first motor
int IN7 = 50;        //control pin for second motor
int IN8 = 52;        //control pin for second motor*/
int ENB_Back = 10;      //Enable pin for second motor


void setup ( )
{  
    Serial.begin (9600); //Starting the serial communication at 9600 baud rate

    setupTOF();

    setupMotors();
    
    Serial.println("Starting up...");

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENA_Front, 255);;

    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    analogWrite(ENB_Front, 100);

    digitalWrite(IN5, LOW);
    digitalWrite(IN6, LOW);
    analogWrite(ENA_Back, 100);

    digitalWrite(IN7, LOW);
    digitalWrite(IN8, LOW);
    analogWrite(ENB_Back, 100);

    
}

void setupTOF()
{
    Wire.begin();

    pinMode(frontLeftShutdown, OUTPUT);
    pinMode(frontRightShutdown, OUTPUT);
    pinMode(backLeftShutdown, OUTPUT);
    pinMode(backRightShutdown, OUTPUT);

    delay(10);

    digitalWrite(frontLeftShutdown, LOW);
    digitalWrite(frontRightShutdown, LOW);
    digitalWrite(backLeftShutdown, LOW);
    digitalWrite(backRightShutdown, LOW);

    delay(10);

    digitalWrite(frontLeftShutdown, HIGH);
    digitalWrite(frontRightShutdown, HIGH);
    digitalWrite(backLeftShutdown, HIGH);
    digitalWrite(backRightShutdown, HIGH);

    delay(10);

    digitalWrite(frontLeftShutdown, HIGH);
    digitalWrite(frontRightShutdown, LOW);
    digitalWrite(backLeftShutdown, LOW);
    digitalWrite(backRightShutdown, LOW);

    FrontLeftTof.begin(0x31);

    delay(50);

    digitalWrite(frontRightShutdown, HIGH);

    FrontRightTof.begin(0x33);

    delay(50);

    digitalWrite(backLeftShutdown, HIGH);

    BackLeftTof.begin(0x35);

    delay(50);

    digitalWrite(backRightShutdown, HIGH);

    BackRightTof.begin(0x37);

    delay(100);

    // Print available devices over i2c.
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

void setupMotors()
{
    //Initializing the motor pins as output
    pinMode(ENA_Front, OUTPUT);
    pinMode(IN1, OUTPUT);  
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);  
    pinMode(IN4, OUTPUT);
    pinMode(ENB_Front, OUTPUT);

    pinMode(ENA_Back, OUTPUT);
    pinMode(IN5, OUTPUT);  
    pinMode(IN6, OUTPUT);
    pinMode(IN7, OUTPUT);  
    pinMode(IN8, OUTPUT);
    pinMode(ENB_Back, OUTPUT);

    pinMode(frontLeftEncoderA, INPUT);
    digitalWrite(frontLeftEncoderA, HIGH);       // turn on pullup resistor
    pinMode(frontLeftEncoderB, INPUT);
    digitalWrite(frontLeftEncoderB, HIGH);       // turn on pullup resistor
    attachInterrupt(digitalPinToInterrupt(2), doEncoderFrontLeft, RISING);

    pinMode(frontRightEncoderA, INPUT);
    digitalWrite(frontRightEncoderA, HIGH);       // turn on pullup resistor
    pinMode(frontRightEncoderB, INPUT);
    digitalWrite(frontRightEncoderB, HIGH);       // turn on pullup resistor
    attachInterrupt(digitalPinToInterrupt(3), doEncoderFrontRight, RISING);

    pinMode(backLeftEncoderA, INPUT);
    digitalWrite(backLeftEncoderA, HIGH);       // turn on pullup resistor
    pinMode(backLeftEncoderB, INPUT);
    digitalWrite(backLeftEncoderB, HIGH);       // turn on pullup resistor
    attachInterrupt(digitalPinToInterrupt(18), doEncoderBackLeft, RISING);

    pinMode(backRightEncoderA, INPUT);
    digitalWrite(backRightEncoderA, HIGH);       // turn on pullup resistor
    pinMode(backRightEncoderB, INPUT);
    digitalWrite(backRightEncoderB, HIGH);       // turn on pullup resistor
    attachInterrupt(digitalPinToInterrupt(19), doEncoderBackRight, RISING);
}

void loop()
{
    Serial.print("Front Left Encoder Pos: ");
    Serial.println(frontLeftEncoderPos);

    Serial.print("Front Right Encoder Pos: ");
    Serial.println(frontRightEncoderPos);

    Serial.print("Back Left Encoder Pos: ");
    Serial.println(backLeftEncoderPos);

    Serial.print("Back Right Encoder Pos: ");
    Serial.println(backRightEncoderPos);

}

void doEncoderFrontLeft()
{
    if (digitalRead(frontLeftEncoderA) == digitalRead(frontLeftEncoderB))
    {
        frontLeftEncoderPos++;
    }
    else
    {
        frontLeftEncoderPos--;
    }
}

void doEncoderFrontRight()
{
    if (digitalRead(frontRightEncoderA) == digitalRead(frontRightEncoderB))
    {
        frontRightEncoderPos++;
    }
    else
    {
        frontRightEncoderPos--;
    }
}

void doEncoderBackLeft()
{
    if (digitalRead(backLeftEncoderA) == digitalRead(backLeftEncoderB))
    {
        backLeftEncoderPos++;
    }
    else
    {
        backLeftEncoderPos--;
    }
}

void doEncoderBackRight()
{
    if (digitalRead(backRightEncoderA) == digitalRead(backRightEncoderB))
    {
        backRightEncoderPos++;
    }
    else
    {
        backRightEncoderPos--;
    }
}
