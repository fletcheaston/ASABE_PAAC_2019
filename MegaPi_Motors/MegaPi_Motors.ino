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
#include <Servo.h>

MeEncoderOnBoard FrontRightMotor(SLOT3);
MeEncoderOnBoard BackRightMotor(SLOT4);
MeEncoderOnBoard BackLeftMotor(SLOT1);
MeEncoderOnBoard FrontLeftMotor(SLOT2);

#define gripperLeftPin A8
#define gripperRightPin A7

Servo gripperLeft;
Servo gripperRight;

int gripperPos = 0;

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

void setupServos()
{
    gripperLeft.attach(gripperLeftPin);
    gripperRight.attach(gripperRightPin);
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
    if(Serial.available())
    {
        char a = Serial.read();
        switch(a)
        {
            case 'M':
            {
                // Prints motor speeds and positions
                printMotorData();
            }
            break;
            
            case 'S':
            {
                // Read successive characters to set motor speeds
                readAndRunMotorSpeed();
            }
            break;
            
            case 'P':
            {
                // Read successive characters to set motor positions
                readAndRunMotorPosition();
            }
            break;
            
            case 'U':
            // Move servos/grippers to the up position
            break;

            case 'D':
            // Move servos/grippers to the down position
            break;

            case 'G':
            // Print gripper position
            break;

            case 'R':
            {
                // Reset all components
                DEBUG_PRINT("Resetting the program...");
                setup();
            }
            break;

            case 'Q':
            {
                // Quit the program.
                DEBUG_PRINT("Quitting the program...");
                quit();
            }

            default:
            break;
        }
    }

    FrontRightMotor.loop();
    BackRightMotor.loop();
    BackLeftMotor.loop();
    FrontLeftMotor.loop();
}

void printMotorData()
{
    Serial.println(String(FrontRightMotor.getCurrentSpeed()) + "," + String(BackRightMotor.getCurrentSpeed()) + "," + String(BackLeftMotor.getCurrentSpeed()) + "," + String(FrontLeftMotor.getCurrentSpeed()));
    Serial.println(String(FrontRightMotor.getCurPos()) + "," + String(BackRightMotor.getCurPos()) + "," + String(BackLeftMotor.getCurPos()) + "," + String(FrontLeftMotor.getCurPos()));
}

void quit()
{
    FrontRightMotor.runSpeed(0);
    BackRightMotor.runSpeed(0);
    BackLeftMotor.runSpeed(0);
    FrontLeftMotor.runSpeed(0);

}

void readAndRunMotorSpeed()
{
    DEBUG_PRINT("Setting motor speed...");

    int motor1Speed = 0;
    motor1Speed = Serial.parseInt();
    DEBUG_PRINT("FrontRightMotor speed set to " + String(motor1Speed));
  
    int motor2Speed = 0;
    motor2Speed = Serial.parseInt();
    DEBUG_PRINT("BackRightMotor speed set to " + String(motor2Speed));
  
    int motor3Speed = 0;
    motor3Speed = Serial.parseInt();
    DEBUG_PRINT("BackLeftMotor speed set to " + String(motor3Speed));

    int motor4Speed = 0;
    motor4Speed = Serial.parseInt();
    DEBUG_PRINT("FrontLeftMotor speed set to " + String(motor4Speed));
  
    FrontRightMotor.runSpeed(motor1Speed);
    BackRightMotor.runSpeed(motor2Speed);
    BackLeftMotor.runSpeed(motor3Speed);
    FrontLeftMotor.runSpeed(motor4Speed);
}

void readAndRunMotorPosition()
{
    // Reads and parses the position (int) from Serial
    // Has to parse the int because we don't know how big the number will be
    // The number will likely be larger than 255, or what can be held in a single byte
    // Therefore, it must be parsed.
    // Parsing is slower than simply reading bytes and chars, but we work with what we got
    // The byte is used for speed because we expect a value between 0 and 255 
    
    int motor1Position = 0;
    motor1Position = Serial.parseInt();
    byte motor1Speed = 0;
    motor1Speed = Serial.parseInt();
    
    int motor2Position = 0;
    motor2Position = Serial.parseInt();
    int motor2Speed = 0;
    motor2Speed = Serial.parseInt();

    int motor3Position = 0;
    motor3Position = Serial.parseInt();
    int motor3Speed = 0;
    motor3Speed = Serial.parseInt();

    int motor4Position = 0;
    motor4Position = Serial.parseInt();
    int motor4Speed = 0;
    motor4Speed = Serial.parseInt();

    FrontRightMotor.moveTo(motor1Position, motor1Speed);
    BackRightMotor.moveTo(motor2Position, motor2Speed);
    BackLeftMotor.moveTo(motor3Position, motor3Speed);
    FrontLeftMotor.moveTo(motor4Position, motor4Speed);
}

