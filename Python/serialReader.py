import serial;
import time;

ser = serial.Serial("/dev/ttyUSB1", 57600, timeout=0.1);

time.sleep(1);

while(True):

    time.sleep(0.1);
    while(ser.in_waiting > 0):
        print(ser.readline().decode());

