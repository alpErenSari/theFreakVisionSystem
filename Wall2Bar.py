# -*- coding: utf-8 -*-
import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet
from shape_detector import ShapeDetector
from CalculateDistance import calculateDist
from i2c import ard_i2c
class Wall2Bar:
    def __init__(self):
        self.cd = ColorSpecDet()
        self.Navigation = ard_i2c()
        self.sd = ShapeDetector()

    def Wall2BarMain(self, start_flag, bgr_image):

        if start_flag:
            PrimaryStates = ["NothingFound", "BarDetected"]
            image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            fd_obj, objects_, resImg, x_color, y_color, w_color, h_color, x_color1, y_color1 = self.cd.ColorDet(image, "blue")
            stop_flag = 0
            cv2.namedWindow("Result", 1)
            cv2.imshow("Result", resImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            if fd_obj:
                ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                rgb_image = image
                cv2.drawContours(rgb_image, [ctr], -1, (0, 255, 0), 2)
                shape_, w, h = self.sd.detect(ctr)
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
                # self.Navigation.writeArduino([], "s0*") # 0 for turning left
                return stop_flag
            else:
                bar_distL = x_color
                pose = calculateDist()
                dist_, angle = pose.distNAngle(x_color, y_color, x_color1, y_color1)
                print("The distance is %f and the angle is %f" % (dist_, angle))
                if (x_color < 10) and (y_color < 10) and abs(x_color1 - 640) < 10 and abs(y_color1 - 0) < 10:
                    stop_flag = 1
                    return stop_flag
                # self.Navigation.writeArduino([], "b"+ np.str(bar_distL) + np.str(dist_) + "*")
                return stop_flag
        else:
            return 1
# aa = Wall2Bar()
# aa.Wall2BarMain(1)
bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/Wall2Bar-30cm/0055.png')
x = Wall2Bar()
retval = x.Wall2BarMain(1, bgr_image)
