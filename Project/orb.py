import numpy as np
import cv2 as cv
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

import socket

client_socket = scoket.socket()
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # and occupied/unoccupied text
    image = frame.array
    img = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

    # Initiate ORB detector
    orb = cv.ORB(nfeatures=100)

    # find the keypoints with ORB
    kp = orb.detect(img,None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    # draw only keypoints location,not size and orientation
    img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)
    cv.imshow("ORB features", img2)
    key = cv.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
