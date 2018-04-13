# -*- coding: utf-8 -*-
import cv2
import numpy as np
import imutils
from ColorSpecDet import ColorSpecDet as cd
import matplotlib.pyplot as plt
from shape_detector import ShapeDetector

class GreenWallDetected:
    def __init__(self):
        pass
    def GreenWallDetected(self, x_color, x_color1):

        if (x_color < 10 or (640 - x_color1) < 10):  # check the ratio
            half_ = 1
        else:
            half_ = 0

        return half_
