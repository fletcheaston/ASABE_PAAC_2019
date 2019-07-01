import cv2
import numpy as np
import os

hsv_green_low = [41, 54, 20]
hsv_green_high = [80, 255, 255]

image_folder = "E:\\PAAC\\Test_Images"

def red_images(image_folder):
    for file in os.listdir(image_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            image_file = image_folder + "\\" + file
            image = cv2.imread(image_file)
            display_red(image)
            continue
        else:
            pass

def display_red(image):  
    hsv_red_low = [161, 170, 84]
    hsv_red_high = [179, 255, 255]
    
    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    blkwht_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Red Color
    low_red = np.array(hsv_red_low)
    high_red = np.array(hsv_red_high)
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(hsv_frame, hsv_frame, mask=red_mask)
    red_blkwht_frame = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    retval, threshold = cv2.threshold(red_blkwht_frame,2, 255, cv2.THRESH_BINARY)

    cv2.imshow("Threshold", threshold)
    cv2.imshow("Red_BLK_White",red_blkwht_frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        exit()



red_images(image_folder)

##def realtime(hsv_red_low, hsv_red_high, hsv_green_low, hsv_green_high):
##    cap = cv2.VideoCapture(0)
##
##    while True:
##
##        #Captures frames
##        _, frame = cap.read()
##
##        #Altering Videos
##        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
##        blkwht_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##
##
##        #Red Color
##        low_red = np.array(hsv_red_low)
##        high_red = np.array(hsv_red_high)
##        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
##        red = cv2.bitwise_and(frame, frame, mask=red_mask)
##        red_blkwht_frame = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
##        retval, threshold = cv2.threshold(red_blkwht_frame,2, 255, cv2.THRESH_BINARY)
##
##        #Green Color
##        low_green = np.array(hsv_green_low)
##        high_green = np.array(hsv_green_high)
##        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
##        green = cv2.bitwise_and(frame, frame, mask=green_mask)
##        blkwht_frame = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
##        
##        #Original Frame
##        #cv2.imshow("Frame", frame)
##
##        #Altered Frames
##        cv2.imshow("Threshold", threshold)
##        cv2.imshow("Red_BLK_White",red_blkwht_frame)
##        ##cv2.imshow("Green BLK_White",green_blkwht_frame)
##        ##cv2.imshow("Red", red)
##        ##cv2.imshow("Green", green)
##        
##        key = cv2.waitKey(1)
##        if key == 27:
##            exit()
