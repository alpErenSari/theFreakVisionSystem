import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet
from shape_detector import ShapeDetector
from GreenWallDetected import GreenWallDetected
from CalculateDistance import calculateDist
from i2c import ard_i2c
from hullOrder import hullOrderer

class Bar2Wall:
    def __init__(self):
        self.cd = ColorSpecDet()
        self.GWD = GreenWallDetected()
        self.Navigation = ard_i2c()
        self.sd = ShapeDetector()
        self.pose = calculateDist()
        self.hord = hullOrderer()
        self.searchState = "left"
    def Bar2WallMain(self, start_flag, bgr_image):
            if start_flag:
                PrimaryStates = ["NothingFound", "GreenWallDetected"]
                image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
                fd_obj, objects_, resImg, imagePoints, w_color, h_color = self.cd.ColorDet(image, "green")
                stop_flag = 0
                if (len(imagePoints) is 4):
                    imagePoints = self.hord.organizer(imagePoints)
                    x_color, y_color = imagePoints[1][0], imagePoints[1][1]
                    x_color1, y_color1 = imagePoints[2][0], imagePoints[2][1]
                    if fd_obj:
                        ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                        rgb_image = image
                        # cv2.drawContours(rgb_image, [ctr], -1, (0, 255, 0), 2)
                        shape_, w, h = self.sd.detect(ctr)
                        if shape_ == "rectangle":
                            if (w/h  < 5):
                                initial_state = PrimaryStates[1]
                                print("We found something..")
                            else:
                                initial_state = PrimaryStates[0]
                                print("We cannot find Tunnel..")
                        else:
                            initial_state = PrimaryStates[0]
                            print("We cannot find Tunnel..")
                    else:
                        initial_state = PrimaryStates[0]
                        print("We cannot find Tunnel..")

                    # end of first if block, rectangle decision has been made

                    if initial_state == PrimaryStates[0]:
                        if (self.searchState == "left"):
                            self.Navigation.writeArduino("s1*")
                            print("Searching..")
                        else:
                            self.Navigation.writeArduino("s0*")
                            print("Searching..")
                        return stop_flag, resImg

                    else:
                        half_ = self.GWD.GreenWallDetected(x_color, x_color1)
                        if half_ == 1:
                            if (x_color<10):
                                # right is not seen
                                i1 = "x"
                                i2 = "y"
                                self.searchState = "left"
                                print("Half of the wall is detected, Turning Right is needed")
                            else :
                                i1 = "y"
                                i2 = "x"
                                self.searchState = "right"
                                print("Half of the wall is detected, Turning Left is needed")
                            self.Navigation.writeArduino("w+9999"+i1+i2+"*")
                            return 0, resImg

                        elif half_ == 0:
                            print("Wall is detected, "
                                  "Navigation is Complete")
                            #print("The points are (%f,%f) and (%f,%f)"%(x_color, y_color, x_color1, y_color1))
                            # calculating the pose of the object
                            dist_, angle = self.pose.distNAngle("wall" , imagePoints)
                            print("The corners are", imagePoints)
                            print("The distance is %f and the angle is %f"%(dist_,angle))
##                          cv2.namedWindow("Result", 1)
##                          cv2.imshow("Result", resImg)
##                          cv2.waitKey(0)
##                          cv2.destroyAllWindows()
                            if angle < 0:
                                s = "-"
                            elif angle > 0:
                                s = "+"
                            else :
                                s = "+"

                            if abs(angle) < 10:
                                ang_ = "0" + np.str(int(abs(angle)))
                            else:
                                ang_ = np.str(int(abs(angle)))
                            if abs(dist_) < 10:
                                dist_str = "0" + np.str(abs(int(dist_)))
                            else:
                                dist_str = np.str(abs(int(dist_)))
                            
                            self.Navigation.writeArduino("w" +  s + ang_ + dist_str + "yy*")
                            if (abs(angle)<=8) and (abs(dist_) <= 10):
                                print("Tunnel will be passed, state is changed")
                                stop_flag = 1
                                print("State Change")
                                return 1, resImg
                            return 0, resImg
                elif (len(imagePoints) == 3):
                    imagePoints = self.hord.organizer(imagePoints)
                    x_color, y_color = imagePoints[0][0], imagePoints[0][1]
                    x_color1, y_color1 = imagePoints[1][0], imagePoints[1][1]
                    print("Three point half")

                    if (x_color < 10):
                        # right is not seen
                        i1 = "x"
                        i2 = "y"
                        self.searchState = "right"
                        self.Navigation.writeArduino("w+9999" + i1 + i2 + "*")
                        print("Half of the wall is detected, Turning Right is needed")

                    elif (abs(x_color1 - 640) < 10):
                        i1 = "y"
                        i2 = "x"
                        self.searchState = "left"
                        self.Navigation.writeArduino("w+9999" + i1 + i2 + "*")
                        print("Half of the wall is detected, Turning Left is needed")

                    return 0, resImg
                else:
                    return 0, resImg


            else:
                return 0,bgr_image

##bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Wall-50cm/0009.png')
##x = Bar2Wall()
##retval = x.Bar2WallMain(1, bgr_image)
