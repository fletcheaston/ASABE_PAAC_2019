import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import os

file_path = 'D:\\PAAC\\Test_Images'

## Show all contoured images in folder
##    show_all_contours()
## Show contour for single image
##    show_contours(image_name)
## Prints number of .png and .jpg images in folder
##    c.number_of_files

class Contour:
    def __init__(self, image_folder_path):
        self.image_folder_path = image_folder_path
        self.image_list = []
        self.number_of_files = 0

    def __call__(self):
        for file in os.listdir(self.image_folder_path):
            if file.endswith(".jpg") or file.endswith(".png"):
                self.image_list.append(file)
                self.number_of_files += 1

    def show_all_contours(self):
        for file in self.image_list:
            image_file = self.image_folder_path + "\\" + file
            image = cv.imread(image_file)
            self.show_contours(image)

    def nothing(self):
        pass
				
    def binary_version(self):
        for file in self.image_list:
            
            image_file = self.image_folder_path + "\\" + file
            image = cv.imread(image_file)
            imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            
            while True:
                cv.createTrackbar('low_value','thresholding', 0, 255, self.nothing())
                cv.createTrackbar('high_value', 'thresholding', 0, 255, self.nothing())
                
                ret,thresh1 = cv.threshold(imgray,50,100,cv.THRESH_BINARY)
                
                cv.imshow('Threshold',thresh1)
                cv.imshow('Original',image)

                k = cv.waitKey(0)
                if k==0:
                    cv.destroyAllWindows()
	
    def show_contours(self, image):
        imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
        edges = cv.Canny(imgray,100,200)
        
        cv.imshow('original',image)
        cv.imshow('edges',edges)
        
        k = cv.waitKey(0)
        if k==27:
            cv.destroyAllWindows()
            
c = Contour(file_path)
c()
##c.show_all_contours()
c.binary_version()



print(c.number_of_files)

