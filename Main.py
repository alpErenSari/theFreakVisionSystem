# -*- coding: utf-8 -*-
import numpy as np
from Bar2Wall2 import Bar2Wall
from Wall2Bar import Wall2Bar
from Bar2Tunnel import Bar2Tunnel
from Tunnel2Bar import Tunnel2Bar
import cv2
StopFlag = 0

StartB2W = 1
StartW2B = 0
StartB2T = 0
StartT2B = 0
##
B2W = Bar2Wall()
W2B = Wall2Bar()
B2T = Bar2Tunnel()
T2B = Tunnel2Bar()

while (~StopFlag):
    image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Wall-30cm/0120.png')
    if StartB2W:
        StopB2W1  = B2W.Bar2WallMain(StartB2W, image)
        StartW2B = StopB2W1
        StartB2W = ~StopB2W1
    elif StartW2B:
        StopW2B1 = W2B.Wall2BarMain(StartW2B, image)
        StartB2T = StopW2B1
        StartW2B = ~StopW2B1
    elif StartB2T:
        StopB2T = B2T.Bar2TunnelMain(StartB2T, image)
        StartT2B = StopB2T
        StartB2T = ~StopB2T
    elif StartT2B:
        StopT2B = T2B.Tunnel2BarMain(StartT2B, image)
        StopFlag = StopT2B
