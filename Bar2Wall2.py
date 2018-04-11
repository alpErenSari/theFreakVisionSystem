import cv2
import numpy as np
import time
from ColorSpecDet import ColorSpecDet
# import matplotlib.pyplot as plt
import matplotlib.figure as figure
from shape_detector import ShapeDetector
from NothingFoundWall import NothingFoundWall as NDFWall
from GreenWallDetected import GreenWallDetected
from CalculateDistance import calculateDist
import os
from i2c import ard_i2c

class Bar2Wall:
    def __init__(self):
        self.cd = ColorSpecDet()
        self.GWD = GreenWallDetected()
        self.Navigation = ard_i2c()
        self.sd = ShapeDetector()
        self.pose = calculateDist()
    def Bar2WallMain(self, start_flag, bgr_image):


            if start_flag:
                PrimaryStates = ["NothingFound", "GreenWallDetected"]
                stop_flag = 0
                image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
                fd_obj, objects_, resImg, imagePoints, w_color, h_color = self.cd.ColorDet(image, "green")
                # taking the upper left and right corners of the object
                x_color, y_color = imagePoints[1][0], imagePoints[1][1]
                x_color1, y_color1 = imagePoints[2][0], imagePoints[2][1]
                if fd_obj:
                    ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                    rgb_image = image
                    cv2.drawContours(rgb_image, [ctr], -1, (0, 255, 0), 2)
                    shape_, w, h = self.sd.detect(ctr)
                    if shape_ == "rectangle":
                        if (w/h  < 2.2 ):
                            initial_state = PrimaryStates[1]
                        else:
                            initial_state = PrimaryStates[0]
                    else:
                        initial_state = PrimaryStates[0]
                else:
                    initial_state = PrimaryStates[0]

                # end of first if block, rectangle decision has been made

                if initial_state == PrimaryStates[0]:
                    #Navigation.writeArduino("s1*")
                    return 0
                else:
                    nfd = 1

                if nfd == 0:
                    # yield (stop_flag, "s1*")
                    print("Wall Not Found")
                    #Navigation.writeArduino("s1*")
                    return 0
                else:
                    half_ = self.GWD.GreenWallDetected(w_color, h_color)
                    if half_ == 1:
                        if np.absolute((x_color + w_color)-640)<=5:
                            # right is not seen
                            i1 = "y"
                            i2 = "x"
                        else :
                            i1 = "x"
                            i2 = "y"
                        #Navigation.writeArduino("w00000"+i1+i2)
                        print("Half of the wall is detected, "
                              "Turning Left is needed")
                        return 0

                    elif half_ == 0:
                        print("Wall is detected, "
                              "Navigation is Complete")
                        #print("The points are (%f,%f) and (%f,%f)"%(x_color, y_color, x_color1, y_color1))
                        # calculating the pose of the object
                        dist_, angle = self.pose.distNAngle("wall" , imagePoints)
                        print("The distance is %f and the angle is %f"%(dist_,angle))
                        cv2.namedWindow("Result", 1)
                        cv2.imshow("Result", resImg)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        if angle<0:
                            s = "-"
                        elif angle>0:
                            s = "+"
                        else :
                            s = "+"
                            if (x_color < 10) and (y_color < 10) and abs(x_color1 - 640) < 10 and abs(y_color1 - 0) < 10:
                                stop_flag = 1
                                return stop_flag
                        #Navigation.writeArduino("w" + s + np.str(angle) + np.str(dist_ / 10) + "yy*")
                        return 0

bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Wall-50cm/0009.png')
x = Bar2Wall()
retval = x.Bar2WallMain(1, bgr_image)
