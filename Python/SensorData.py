# Created by Fletcher Easton

import serial;

def main():
    while(True):
        
        try:
            sensorSerial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.1);
            
            while(True):
                
                while(sensorSerial.in_waiting):
                    data = readSerial(sensorSerial);
                    
                    parseData(data);
        
        except:
            pass;

def parseData(data):
    backLeftTof = None;
    backRightTof = None;
    frontLeftTof = None;
    frontRightTof = None;
    leftLidar = None;
    rightLidar = None;
    
    try:
        backLeftTof = data.split(",")[0];
        backRightTof = data.split(",")[1];
        frontLeftTof = data.split(",")[2];
        frontRightTof = data.split(",")[3];
        leftLidar = data.split(",")[4];
        rightLidar = data.split(",")[5];
        
    except:
        pass;
        
    print(backLeftTof, backRightTof, frontLeftTof, frontRightTof, leftLidar, rightLidar);

def readSerial(ser):
    message = ser.readline().decode().strip();
    return(message);
    
if __name__== "__main__":
    main();
