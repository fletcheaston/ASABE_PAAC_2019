import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

directory = "E:\\PAAC\\Test_Images"

def display_contours(image):
    
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    edges = cv2.Canny(imgray,100,200)

    cv2.imshow('edges',edges)
    
    k = cv2.waitKey(0)
    if k==27:
        cv2.destroyAllWindows()
    else:
        print(k)

def find_red():
    cap = cv2.VideoCapture(0)

    while True:

    #Captures frames
        _, frame = cap.read()
        
        #Altering Videos
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blkwht_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        #Red Color
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        red = cv2.bitwise_and(frame, frame, mask=red_mask)

        #Original Frame
        cv2.imshow("Frame", frame)

        #Altered Frames
        cv2.imshow("Green", green)
        
        key = cv2.waitKey(1)
        if key == 27:
            exit()

def find_green():
    cap = cv2.VideoCapture(0)

    while True:

    #Captures frames
        _, frame = cap.read()
        
        #Altering Videos
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blkwht_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Green Color
        low_green = np.array([41, 54, 20])
        high_green = np.array([80, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)
        
        #Original Frame
        cv2.imshow("Frame", frame)

        #Altered Frames
        cv2.imshow("Red", red)

        key = cv2.waitKey(1)
        if key == 27:
            exit()
    
for file in os.listdir(directory):
    if file.endswith(".jpg") or file.endswith(".png"):
        image_file = directory + "\\" + file
        image = cv2.imread(image_file)
        display_contours(image)
        continue
    else:
        pass


