# -*- coding: utf-8 -*-
import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet
from shape_detector import ShapeDetector
from CalculateDistance import calculateDist
from i2c import ard_i2c
from hullOrder import hullOrderer

class Wall2Bar:
    def __init__(self):
        self.cd = ColorSpecDet()
        self.Navigation = ard_i2c()
        self.sd = ShapeDetector()
        self.pose = calculateDist()
        self.hord = hullOrderer()
        self.searchState = "left"
    def Wall2BarMain(self, start_flag, bgr_image):

        if start_flag:
            PrimaryStates = ["NothingFound", "BarDetected"]
            image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            fd_obj, objects_, resImg, imagePoints, w_color, h_color = self.cd.ColorDet(image, "blue")
            # taking the upper left and right corners of the object
            stop_flag = 0
            if (len(imagePoints) is 4):
                imagePoints = self.hord.organizer(imagePoints)
                x_color, y_color = imagePoints[1][0], imagePoints[1][1]
                x_color1, y_color1 = imagePoints[2][0], imagePoints[2][1]

    ##            cv2.namedWindow("Result", 1)
    ##            cv2.imshow("Result", resImg)
    ##            cv2.waitKey(0)
    ##            cv2.destroyAllWindows()
                if fd_obj:
                    ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                    rgb_image = image
                    cv2.drawContours(rgb_image, [ctr], -1, (0, 255, 0), 2)
                    shape_, w, h = self.sd.detect(ctr)
                    if shape_ == "rectangle":
                        if (w / h < 5):  # tam olarak görmedigi yarım gördügü
                            initial_state = PrimaryStates[1]
                            print("We found something..")
                        else:
                            initial_state = PrimaryStates[0]
                            print("We cannot find Bar..")
                    else:
                        initial_state = PrimaryStates[0]
                        print("We cannot find Bar..")
                else:
                    initial_state = PrimaryStates[0]
                    print("We cannot find Bar..")

                if initial_state == PrimaryStates[0]:
                    if (self.searchState == "left"):
                        self.Navigation.writeArduino("s1*")
                        print("Searching..")
                    else:
                        self.Navigation.writeArduino("s0*")
                        print("Searching..")
                    return stop_flag, resImg
                else:
                    bar_distL = x_color
                    dist_, angle = self.pose.distNAngle("bar" ,imagePoints)
                    print("The distance is %f and the angle is %f" % (dist_, angle))
                    if (x_color < 10) and (y_color < 10) and (abs(x_color1 - 640) < 10) and (abs(y_color1 - 0) < 10):
                        print("Bar will be passed, state is changed")
                        stop_flag = 1
                        return stop_flag, resImg

                    self.Navigation.writeArduino("b"+ np.str(int(bar_distL)) + np.str(int(dist_)) + "*")
                    return stop_flag, resImg
            else:
                return 1, resImg
        else:
            return 1,bgr_image

# aa = Wall2Bar()
# aa.Wall2BarMain(1)
##bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/Wall2Bar-30cm/0055.png')
##x = Wall2Bar()
##retval = x.Wall2BarMain(1, bgr_image)
