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
from i2c import ard_i2c 

# FARKLI STATELERDEN BASLAMAK ICIN, BASLAMAK ISTEDIGIMIZI 1 YAPIYORUZ
# EGER HEPSINI ARKA ARKAYA DENEYECEKSEK STARTB2W U 1 YAPMAK YETERLI
# initializing the flags
StopFlag = 0
StartB2W = 0
StartW2B = 0
StartB2T = 1
StartT2B = 0

Navigation = ard_i2c()

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

B2W = Bar2Wall()
W2B = Wall2Bar()
B2T = Bar2Tunnel()
T2B = Tunnel2Bar()

while (~StopFlag):
    ## Initializing the objects
    current_time = time.time()

    camera.capture(rawCapture, format="bgr", use_video_port=True)
    #image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Wall-30cm/0120.png')
    image = rawCapture.array
    rawCapture.truncate(0)
    
    cv2.namedWindow("Frame",1)
    cv2.imshow("Frame", image)
    if StartB2W:
        print("Bar to Wall State")
        StopB2W1, resImg  = B2W.Bar2WallMain(StartB2W, image)
        StartW2B = StopB2W1
        StartB2W = int(not(StopB2W1!=0))
    elif StartW2B:
        print("Wall to Bar State")
        StopW2B1, resImg = W2B.Wall2BarMain(StartW2B, image)
        StartB2T = StopW2B1
        StartW2B = int(not(StopW2B1!=0))
    elif StartB2T:
        print("Bar to Tunnel State")
        StopB2T, resImg = B2T.Bar2TunnelMain(StartB2T, image)
        StartT2B = StopB2T
        StartB2T = int(not(StopB2T!=0))
        print("Start bar to Tunnel Flag :%d"%StartB2T)
        print("Start tunnel to bar Flag :%d"%StartT2B)
        print("Stop bar to Tunnel Flag :%d"%StopB2T)
    elif StartT2B:
        print("Tunnel to Bar State")
        StopT2B, resImg = T2B.Tunnel2BarMain(StartT2B, image)
        StopFlag = StopT2B
        
        
    cv2.namedWindow("Frame",1)
    cv2.imshow("Frame", resImg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    time_el = time.time()-current_time
    print("Time elapsed:%f" %time_el)

Navigation.writeArduino("i*")
cv2.destroyAllWindows()
