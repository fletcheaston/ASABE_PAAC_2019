import serial
import pygame
import time
import sys
from Motors import *

# 0 is A
# 1 is B
# 3 is X
# 4 is Y
# 6 is left bumper
# 7 is right bumper
# 11 is left of start button
# 13 is start button

def get_buttons(xbox_pad):
    buttons = [];
    pygame.event.get();
    for i in range(xbox_pad.get_numbuttons()):
        if(xbox_pad.get_button(i) == 1):
            buttons.append(i);
    return(buttons);

# Initialize PyGame for joystick functionality
pygame.init();
pygame.joystick.init();
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())];
xbox_pad = joysticks[0];
xbox_pad.init();

print("Controller: {!r}".format(xbox_pad.get_name()));

try:
    robotSerial = serial.Serial(port="/dev/ttyUSB1", baudrate=9600, timeout=0.1);
except:
    print("No device found.");
    sys.exit();

time.sleep(1);

buttons = [];

speed = 100;

print("Ready to run.");

while(True):
    buttons = get_buttons(xbox_pad);

    # Move forward
    if(0 in buttons):
        setDirectionSpeed(robotSerial, "FORWARD", speed);
        
    # Move backward
    if(4 in buttons):
        setDirectionSpeed(robotSerial, "BACKWARD", speed);
        
    # Stop
    if(1 in buttons):
        setDirectionSpeed(robotSerial, "FORWARD", 0);
        
    # Spin left
    if(6 in buttons):
        setMotorSpeed(robotSerial, speed, speed, -1 * speed, -1 * speed);
        
    # Spin right
    if(7 in buttons):
        setMotorSpeed(robotSerial, -1 * speed, -1 * speed, speed, speed);
        
    # Decrease speed
    if(11 in buttons):
        speed = speed - 5;
        if(speed < 0):
            speed = 0;
    
    # Increase speed
    if(13 in buttons):
        speed = speed + 5;
        if(speed > 255):
            speed = 255;
        
    message = "";
    while(robotSerial.in_waiting > 0):
        message += robotSerial.readline().decode().strip();
    if(message != ""):
        print(message);

    time.sleep(0.1);
