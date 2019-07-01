from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
import time
import cv2 as cv
import numpy as np
from threading import Thread

class detection:
    def __init__(self):
        self.check_red_count = 0
        self.check_green_count = 0
        self.show_image = None
        self.camera = PiCamera()
        self.camera.framerate = 32
        self.camera.rotation = 180
        self.camera.resolution = (704, 544)
        self.hsv_red_low = [161, 170, 84]
        self.hsv_red_high = [179, 255, 255]
        self.hsv_green_low = [41, 54, 20]
        self.hsv_green_high = [80, 255, 255]
            
    def __call__(self, show_image = None):
        self.show_image = show_image
        self.detect()

        if self.check_red_count > self.check_green_count:
            return 'red'
        elif self.check_red_count < self.check_green_count:
            return 'green'
        else:
            return '''We're fucked!'''

    def detect(self):
        rawCapture = PiRGBArray(self.camera, size=(704, 544))

        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):

            image = frame.array

            blurred_image = cv.GaussianBlur(image, (5,5), 0)
            
            green_image = self.detect_color(self.hsv_green_low, self.hsv_green_high, blurred_image)
            red_image = self.detect_color(self.hsv_red_low, self.hsv_red_high, blurred_image)
            
            
            green_w_h = self.rectangle(green_image, image)
            red_w_h = self.rectangle(red_image, image)

            green_area = green_w_h[0] * green_w_h[1]
            red_area = red_w_h[0]*red_w_h[1]
            
            green_add = self.check_area(green_area)
            red_add = self.check_area(red_area)
            
            self.check_green_count += green_add
            self.check_red_count += red_add 
            
            if self.show_image:
                ## Shows Image-------------------------------------------------
                cv.imshow("Result", np.hstack([image]))

                ## Sets quit key and truncates for smoothing-------------------
                key = cv.waitKey(1) & 0xFF
                
                rawCapture.truncate(0)

                if key == ord("q"):
                    cv.destroyAllWindows()
                    break    
  
            else:
                rawCapture.truncate(0)
            print(self.check_green_count)

##    def run_red(self):
##        rawCapture = PiRGBArray(self.camera, size=(704, 544))
##        # Runs Red
##        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
##            end_time = time.time()
##            print(end_time)
##            if end_time - start_time >= 5.0:
##                cv.destroyAllWindows()
##                break
##            
##            image = frame.array
##
##            blurred_image = cv.GaussianBlur(image, (5,5), 0)
##            
##            new_image = self.detect_color(self.hsv_red_low, self.hsv_red_high, blurred_image)
##            
##            w_h = self.rectangle(new_image, image)
##
##            area = w_h[0]*w_h[1]
##
##            add = self.check_area(area)
##
##            self.check_red_count += add
##            
##            if self.show_image:
##                ## Shows Image-------------------------------------------------
##                cv.imshow("Result", np.hstack([image]))
##
##                ## Sets quit key and truncates for smoothing-------------------
##                key = cv.waitKey(1) & 0xFF
##
##                rawCapture.truncate(0)
##                
##            else:
##                rawCapture.truncate(0)
##            
##    def run_green(self):
##        rawCapture = PiRGBArray(self.camera, size=(704, 544))
##        # Runs Green
##        start_time = time()
##        for frame in self.camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
##            
##            if time() - start_time >= 5.0:
##                cv.destroyAllWindows()
##                break
##            
##            image = frame.array
##
##            blurred_image = cv.GaussianBlur(image, (5,5), 0)
##            
##            new_image = self.detect_color(self.hsv_green_low, self.hsv_green_high, blurred_image)
##
##            w_h = self.rectangle(self, new_image, image)
##
##            area = w_h[0]*w_h[1]
##
##            add = self.check_area(area)
##
##            self.check_green_count += add
##            
##            if self.show_image:
##                ## Shows Image-------------------------------------------------
##                cv.imshow("Result", np.hstack([image]))
##
##                ## Sets quit key and truncates for smoothing-------------------
##                key = cv.waitKey(1) & 0xFF
##
##                rawCapture.truncate(0)
##            else:
##                rawCapture.truncate(0)
##            print(self.check_green_count)
        
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

    def check_area(self, area):
        if area >= 10000:
            return 1
        else:
            return 0

    def rectangle(self, new_image, image):
        contours, hierarchy = cv.findContours(new_image, 1, 2)
        if len(contours) != 0 and self.show_image:
            # draw in blue the contours that were found
            cv.drawContours(image, contours, -1, 255, 3)

            #find the biggest area
            c = max(contours, key = cv.contourArea)

            x,y,w,h = cv.boundingRect(c)
            
            # draw the book contour (in green)
            cv.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
            return [w,h]
            
        elif len(contours) != 0:
            #find the biggest area
            c = max(contours, key = cv.contourArea)

            x,y,w,h = cv.boundingRect(c)
            
            return [w,h]
        else:
            return [0,0]

new_detection = detection()
if __name__ == '__main__':
    while True:
        show_image = str(input('Show image or run competition(s/r): '))
        time = str(input('Input Time to run each detection(A number): '))
        try:
##            time = float(time)
            if show_image == 's' or show_image == 'r':
                if show_image == 's':
                    print("good! a")
                    new_detection(True)
                elif show_image == 'r':
                    print("good! b")
                    new_detection(False)
            else:
                print('Invalid image_choice')
        except Exception as error:
            print(error)
            print('Invalid Time choice')

