# -*- coding: utf-8 -*-
import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet as cd
import matplotlib.pyplot as plt
from shape_detector import ShapeDetector

class NothingFoundBar:

    def __init__(self):
        pass

    def BarNothingFound(self, img):
        fd_obj, objects_, x_color, y_color, w_color, h_color = cd.ColorDet([], img.copy(), "blue")
        if fd_obj:
            ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
            rgb_image = img
            cv2.drawContours(rgb_image.copy(), [ctr], -1, (0, 255, 0), 2)
            # plt.imshow(img)
            # ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
            sd = ShapeDetector()
            shape_, w, h = sd.detect(ctr)
            if shape_ == "rectangle":
                if (w / h < 0.7):  # tam olarak görmedigi yarım gördügü
                    nfd = 1 # obje bulduk

                else:
                    nfd = 0
            else:
                nfd = 0
        else:
            nfd = 0
        return nfd
