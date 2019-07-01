from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import numpy as np

class detection:
    def __init__(self, show_image=None):
        self.show_image = show_image
        self.check_red_count = []
        self.check_green_count = []
        self.camera = PiCamera()
        self.camera.framerate = 32
        self.camera.rotation = 180
        self.camera.resolution = (704, 544)
        self.hsv_red_low = [161, 170, 84]
        self.hsv_red_high = [179, 255, 255]
        self.hsv_green_low = [41, 54, 20]
        self.hsv_green_high = [80, 255, 255]
        
    def detect_color(self, low, high, image):
        hsv_frame = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        blkwht_frame = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        low_color = np.array(low)
        high_color = np.array(high)
        color_mask = cv.inRange(hsv_frame, low_color, high_color)
        color = cv.bitwise_and(hsv_frame, hsv_frame, mask=color_mask)
        color_blkwht_frame = cv.cvtColor(color, cv.COLOR_BGR2GRAY)
        retval, threshold = cv.threshold(color_blkwht_frame,2, 255, cv.THRESH_BINARY)

        return threshold
            
    def detect_red(self):
        rawCapture = PiRGBArray(self.camera, size=(704, 544))
        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            image = frame.array

            blurred_image = cv.GaussianBlur(image, (5,5), 0)
            
            new_image = self.detect_color(self.hsv_red_low, self.hsv_red_high, blurred_image)

            #Contour Setting
            contours, hierarchy = cv.findContours(new_image, 1, 2)
##            cv.drawContours(new_image, contours, -1, 255, 3)
            
            if len(contours) != 0:
                # draw in blue the contours that were found
                cv.drawContours(image, contours, -1, 255, 3)

                #find the biggest area
                c = max(contours, key = cv.contourArea)

                x,y,w,h = cv.boundingRect(c)
                
                # draw the book contour (in green)
                cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

##-----------------Checks if Area is Acceptable----------------------------
            try:
                area = w * h
                output = self.check_area(area)
                print(output)
            except:
                pass
            
##--------------------------Shows Image------------------------------------
            cv.imshow("Result", np.hstack([image]))

##-------------Sets quit key and truncates for smoothing-------------------
            key = cv.waitKey(1) & 0xFF

            rawCapture.truncate(0)

            if key == ord("q"):
                cv.destroyAllWindows()
                break

    def detect_green(self):
        rawCapture = PiRGBArray(self.camera, size=(704, 544))
        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            image = frame.array

            blurred_image = cv.GaussianBlur(image, (5,5), 0)
            
            new_image = self.detect_color(self.hsv_green_low, self.hsv_green_high, blurred_image)

            #Contour Setting
            contours, hierarchy = cv.findContours(new_image, 1, 2)
##            cv.drawContours(new_image, contours, -1, 255, 3)
            
            if len(contours) != 0:
                # draw in blue the contours that were found
                cv.drawContours(image, contours, -1, 255, 3)

                #find the biggest area
                c = max(contours, key = cv.contourArea)

                x,y,w,h = cv.boundingRect(c)
                
                # draw the book contour (in green)
                cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

##-----------------Checks if Area is Acceptable----------------------------
            try:
                area = w * h
                output = self.check_area(area)
                print(output)
            except:
                pass
            
##--------------------------Shows Image------------------------------------
            cv.imshow("Result", np.hstack([image]))

##-------------Sets quit key and truncates for smoothing-------------------
            key = cv.waitKey(1) & 0xFF

            rawCapture.truncate(0)

            if key == ord("q"):
                cv.destroyAllWindows()
                break
            
    def check_area(self, area):
        if area >= 10000:
            return 1
##        elif area >= 5000 and area < 10000:
##            return "maybe"
        else:
            return 0
        
    def __call__(self):
        rawCapture = PiRGBArray(self.camera, size=(704, 544))
        # Detect Red
        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            image = frame.array

            blurred_image = cv.GaussianBlur(image, (5,5), 0)
            new_image = self.detect_color(self.hsv_red_low, self.hsv_red_high, blurred_image)
            w_h = rectangle(self, new_image)
            area = w_h[0]*w_h[1]
            add = check_area(area)
            self.check__red_count += add
            rawCapture.truncate(0)

        # Detect If Green
        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            new_image = self.detect_color(self.hsv_green_low, self.hsv_green_high, blurred_image)
            w_h = rectangle(self, new_image)
            area = w_h[0]*w_h[1]
            add = check_area(area)
            self.check__green_count += add
            rawCapture.truncate(0)

        if self.check_red_count > self.check_green_count:
            return 'red'
        elif self.check_red_count < self.check_green_count:
            return 'green'
        else:
            return '''We're fucked!'''

    def draw_rectangle(self, new_image):
        contours, hierarchy = cv.findContours(new_image, 1, 2)
        ## cv.drawContours(new_image, contours, -1, 255, 3)
        
        if len(contours) != 0 and self.show_image:
            # draw in blue the contours that were found
            cv.drawContours(image, contours, -1, 255, 3)

            #find the biggest area
            c = max(contours, key = cv.contourArea)

            x,y,w,h = cv.boundingRect(c)
            
            # draw the book contour (in green)
            cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            return [w,h]
            
        else len(contours) != 0:

            #find the biggest area
            c = max(contours, key = cv.contourArea)

            x,y,w,h = cv.boundingRect(c)
            
            return [w,h]

                 

new_detection = detection()
if __name__ == '__main__':
##    while True:
##        indicator = str(input('Which color would you like(g/r): '))
##        show_image = str(input('Show image or run competition(s/r): '))
##        if indicator == 'r' and show_image == 's':
##            new_detection.detect_red(True)
##        elif indicator == 'r' and show_image == 'r':
##            new_detection.detect_red(False)
##        elif indicator == 'g' and show_image == 's':
##            new_detection.detect_green(True)
##        elif indicator == 'g' and show_image == 'r':
##            new_detection.detect_green(False)
##        else:
##            print('Invalid choice')

    while True:
        indicator = str(input('Which color would you like(g/r): '))
        show_image = str(input('Show image or run competition(s/r): '))
        if show_image == 's':
            new_detection(True)
        elif show_image == 'r':
            new_detection(False)
        else:
            print('Invalid choice')


