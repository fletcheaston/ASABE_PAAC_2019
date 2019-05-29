// Created by Fletcher Easton
// Designed for the MegaPi
// Drives four DC motors with encoders (using the MegaPi slots)
// Drives two servos (using the analog pins)

#define DEBUG

#ifdef DEBUG
  #define DEBUG_PRINT(x) Serial.println(x);
#else
  #define DEBUG_PRINT(x)
#endif

#include <Arduino.h>
#include <MeMegaPi.h>
#include <Wire.h>

int c = 0;

MeEncoderOnBoard FrontRightMotor(SLOT2);
MeEncoderOnBoard BackRightMotor(SLOT1);
MeEncoderOnBoard BackLeftMotor(SLOT4);
MeEncoderOnBoard FrontLeftMotor(SLOT3);

void isr_process_encoder1()
{
    if(digitalRead(FrontRightMotor.getPortB()) == 0)
    {
        FrontRightMotor.pulsePosMinus();
    }
    else
    {
        FrontRightMotor.pulsePosPlus();
    }
}

void isr_process_encoder2()
{
    if(digitalRead(BackRightMotor.getPortB()) == 0)
    {
        BackRightMotor.pulsePosMinus();
    }
    else
    {
        BackRightMotor.pulsePosPlus();
    }
}

void isr_process_encoder3()
{
    if(digitalRead(BackLeftMotor.getPortB()) == 0)
    {
        BackLeftMotor.pulsePosMinus();
    }
    else
    {
        BackLeftMotor.pulsePosPlus();
    }
}

void isr_process_encoder4()
{
    if(digitalRead(FrontLeftMotor.getPortB()) == 0)
    {
        FrontLeftMotor.pulsePosMinus();
    }
    else
    {
        FrontLeftMotor.pulsePosPlus();
    }
}

void setupMotors()
{
    attachInterrupt(FrontRightMotor.getIntNum(), isr_process_encoder1, RISING);
    attachInterrupt(BackRightMotor.getIntNum(), isr_process_encoder2, RISING);
    attachInterrupt(BackLeftMotor.getIntNum(), isr_process_encoder3, RISING);
    attachInterrupt(FrontLeftMotor.getIntNum(), isr_process_encoder4, RISING);

    //Set PWM 8KHz
    // No idea what this does, but it was in the example code so...?
    TCCR1A = _BV(WGM10);
    TCCR1B = _BV(CS11) | _BV(WGM12);
  
    TCCR2A = _BV(WGM21) | _BV(WGM20);
    TCCR2B = _BV(CS21);

    FrontRightMotor.setPulse(11);
    BackRightMotor.setPulse(11);
    BackLeftMotor.setPulse(11);
    FrontLeftMotor.setPulse(11);

    FrontRightMotor.setRatio(34.02);
    BackRightMotor.setRatio(34.02);
    BackLeftMotor.setRatio(34.02);
    FrontLeftMotor.setRatio(34.02);

    FrontRightMotor.setPosPid(1.8, 0, 1.2);
    BackRightMotor.setPosPid(1.8, 0, 1.2);
    BackLeftMotor.setPosPid(1.8, 0, 1.2);
    FrontLeftMotor.setPosPid(1.8, 0, 1.2);

    FrontRightMotor.setSpeedPid(0.18, 0.01, 0);
    BackRightMotor.setSpeedPid(0.18, 0.01, 0);
    BackLeftMotor.setSpeedPid(0.18, 0.01, 0);
    FrontLeftMotor.setSpeedPid(0.18, 0.01, 0);
}

void setup()
{
    Serial.begin(57600);
    
    Wire.begin();
    
    setupMotors();

    Serial.println("Finished setup.");
}

void loop()
{
    c++;

    if(c % 100 == 0)
    {
        printMotorData();
    }

    if(c % 1000 == 0)
    {
        FrontRightMotor.runSpeed(20);
        BackRightMotor.runSpeed(20);
        BackLeftMotor.runSpeed(20);
        FrontLeftMotor.runSpeed(20);
        Serial.println("Running all motors at speed 20");
    }
    else if(c % 500 == 0)
    {
        FrontRightMotor.runSpeed(-20);
        BackRightMotor.runSpeed(-20);
        BackLeftMotor.runSpeed(-20);
        FrontLeftMotor.runSpeed(-20);
        Serial.println("Running all motors at speed -20");
    }

    FrontRightMotor.loop();
    BackRightMotor.loop();
    BackLeftMotor.loop();
    FrontLeftMotor.loop();

    delay(10);
}

void printMotorData()
{
    Serial.println(String(FrontRightMotor.getCurrentSpeed()) + "," + String(BackRightMotor.getCurrentSpeed()) + "," + String(BackLeftMotor.getCurrentSpeed()) + "," + String(FrontLeftMotor.getCurrentSpeed()));
    Serial.println(String(FrontRightMotor.getCurPos()) + "," + String(BackRightMotor.getCurPos()) + "," + String(BackLeftMotor.getCurPos()) + "," + String(FrontLeftMotor.getCurPos()));
}

