# -*- coding: utf-8 -*-
import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet as cd
# import matplotlib.pyplot as plt
from shape_detector import ShapeDetector
from NothingFoundBar import NothingFoundBar as NDFBar
from CalculateDistance import calculateDist
from i2c import ard_i2c as Navigation
class Tunnel2Bar:
    def __init__(self):
        pass

    def Tunnel2BarMain(self, start_flag, bgr_image):
        if start_flag:
            PrimaryStates = ["NothingFound", "BarDetected"]

            image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            fd_obj, objects_, x_color, y_color, w_color, h_color, x_color1, y_color1 = cd.ColorDet([], image, "blue")
            if fd_obj:
                ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                rgb_image = image
                cv2.drawContours(rgb_image, [ctr], -1, (0, 255, 0), 2)
                sd = ShapeDetector()
                shape_, w, h = sd.detect(ctr)
                if shape_ == "rectangle":
                    if (w / h < 1):  # tam olarak görmedigi yarım gördügü
                        initial_state = PrimaryStates[1]
                    else:
                        initial_state = PrimaryStates[0]
                else:
                    initial_state = PrimaryStates[0]
            else:
                initial_state = PrimaryStates[0]

            if initial_state == PrimaryStates[0]:
                nfd = 0
            else:
                nfd = 1
            if nfd == 0:
                print("Bar Not Found")

                Navigation.writeArduino([], "s0*")
                return 0
            else:
                bar_distL = x_color

                ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                shape_, w, h = sd.detect(ctr)
                pose = calculateDist()
                dist_, angle = pose.distNAngle(x_color, y_color, x_color1, y_color1)
                print("The distance is %f and the angle is %f" % (dist_, angle))

                if (x_color<10) and (y_color<10) and abs(x_color1-640)<10 and abs(y_color1-0)<10:
                    state_ = "Passing Bar"
                    stop_flag = 1
                    return stop_flag

                # yield (stop_flag, "b"+ np.str(bar_distL) + np.str(dist_) + "*")
                Navigation.writeArduino([], "b"+ np.str(bar_distL) + np.str(dist_) + "*")
                return 0
        else:
            return 1
