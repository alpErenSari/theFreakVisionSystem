import cv2
import numpy as np
import imutils
from ColorSpecDet import ColorSpecDet as cd
import matplotlib.pyplot as plt
from shape_detector import ShapeDetector

class RedTunnelDetected:
    def __init__(self):
        pass
    def RedTunnelDetected(self, x_color, x_color1):
        if (x_color < 10) or (abs(640 - x_color1) < 10):  # check the ratio
            half_ = 1
            print("x values are ", x_color, x_color1)
        else:
            half_ = 0

        return half_

