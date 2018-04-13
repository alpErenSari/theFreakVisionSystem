# -*- coding: utf-8 -*-
import numpy as np
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from Bar2Wall2 import Bar2Wall
from Wall2Bar import Wall2Bar
from Bar2Tunnel import Bar2Tunnel
from Tunnel2Bar import Tunnel2Bar


# initializing the flags
StopFlag = 0
StartB2W = 1
StartW2B = 0
StartB2T = 0
StartT2B = 0


## Initializing the camera
camera = PiCamera()
camera.led = True
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

while (~StopFlag):
    ## Initializing the objects
    B2W = Bar2Wall()
    W2B = Wall2Bar()
    B2T = Bar2Tunnel()
    T2B = Tunnel2Bar()

    camera.capture(rawCapture, format="bgr", use_video_port=True)
    #image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Wall-30cm/0120.png')
    image = rawCapture.array
    rawCapture.truncate(0)
    
    cv2.namedWindow("Frame",1)
    cv2.imshow("Frame", image)
    if StartB2W:
        StopB2W1, resImg  = B2W.Bar2WallMain(StartB2W, image)
        StartW2B = StopB2W1
        StartB2W = ~StopB2W1
    elif StartW2B:
        StopW2B1, resImg = W2B.Wall2BarMain(StartW2B, image)
        StartB2T = StopW2B1
        StartW2B = ~StopW2B1
    elif StartB2T:
        StopB2T, resImg = B2T.Bar2TunnelMain(StartB2T, image)
        StartT2B = StopB2T
        StartB2T = ~StopB2T
    elif StartT2B:
        StopT2B = T2B.Tunnel2BarMain(StartT2B, image)
        StopFlag = StopT2B
        
    cv2.namedWindow("Frame",1)
    cv2.imshow("Frame", resImg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break        

cv2.destroyAllWindows()