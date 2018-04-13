import cv2
import numpy as np
import imutils
from ColorSpecDet import ColorSpecDet as cd
import matplotlib.pyplot as plt
from shape_detector import ShapeDetector

class RedTunnelDetected:
    def __init__(self):
        pass
    def RedTunnelDetected(self, w_color, h_color):
        if (w_color / h_color) <= 2.0:
            half_ = 1
        else:
            half_ = 0

        return half_

