import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet
from shape_detector import ShapeDetector
from RedTunnelDetected import RedTunnelDetected
from CalculateDistance import calculateDist
from i2c import ard_i2c 
from hullOrder import hullOrderer

class Bar2Tunnel:
    def __init__(self):
        self.cd = ColorSpecDet()
        self.RTD = RedTunnelDetected()
        self.sd = ShapeDetector()
        self.pose = calculateDist()
        self.Navigation = ard_i2c()
        self.hord = hullOrderer()
        self.searchState = "left"
    def Bar2TunnelMain(self, start_flag, bgr_image):
        if start_flag:
            PrimaryStates = ["NothingFound", "TunnelDetected"]
            image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            fd_obj, objects_, resImg, imagePoints, w_color, h_color = self.cd.ColorDet(image.copy(), "red")
            # taking the upper left and right corners of the object
            stop_flag = 0
            if (len(imagePoints) == 4):
                imagePoints = self.hord.organizer(imagePoints)
                x_color, y_color = imagePoints[1][0], imagePoints[1][1]
                x_color1, y_color1 = imagePoints[2][0], imagePoints[2][1]
                if fd_obj:
                    ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                    shape_, w, h = self.sd.detect(ctr)
                    if shape_ == "rectangle" or shape_ == "tunnel":
                        if w_color / h_color < 5:
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

                if initial_state == PrimaryStates[0]:
                    if (self.searchState == "left"):
                        self.Navigation.writeArduino("s1*")
                        print("Searching..")
                    else:
                        self.Navigation.writeArduino("s0*")
                        print("Searching..")
                    return 0, resImg

                else:
                    half_ = self.RTD.RedTunnelDetected(x_color, x_color1)
                    if half_ == 1:
                        if (x_color < 10):
                            # right is not seen
                            i1 = "x"
                            i2 = "y"
                            self.searchState = "left"
                            print("Half of the tunnel is detected, Turning Right is needed")
                        else:
                            i1 = "y"
                            i2 = "x"
                            self.searchState = "right"
                            print("Half of the tunnel is detected, Turning Left is needed")
                        self.Navigation.writeArduino("t+9999" + i1 + i2 + "*")
                       
                        return 0, resImg

                    elif half_ == 0:
                        print("Tunnel is detected, "
                              "Navigation is Complete")
                        #print("The points are (%f,%f) and (%f,%f)"%(x_color, y_color, x_color1, y_color1))
                        dist_, angle = self.pose.distNAngle("tunnel", imagePoints)
                        print("The distance is %f and the angle is %f" % (dist_, angle))
    ##                    cv2.namedWindow("Result", 1)
    ##                    cv2.imshow("Result", resImg)
    ##                    cv2.waitKey(0)
    ##                    cv2.destroyAllWindows()
                        if angle < 0:
                            s = "-"
                        elif angle > 0:
                            s = "+"
                        else:
                            s = "+"
                        if abs(angle)<10:
                            ang_ = "0" + np.str(int(abs(angle)))
                        else:
                            ang_ = np.str(int(abs(angle)))
                        if abs(dist_)<10:
                            dist_str = "0" + np.str(abs(int(dist_)))
                        else:
                            dist_str = np.str(abs(int(dist_)))
                        self.Navigation.writeArduino("t" + s + ang_ + dist_str + "yy*")

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
                 if ((y_color < 36) and (y_color1 < 36) ):
                    self.Navigation.writeArduino("t+3005yy*")
                    print("Going Backwards, Freak can't see")
                 elif (x_color < 10):
                    # right is not seen
                    i1 = "x"
                    i2 = "y"
                    self.searchState = "right"
                    self.Navigation.writeArduino("t+9999" + i1 + i2 + "*")
                    print("Half of the tunnel is detected, Turning Right is needed")
                
                 elif (abs(x_color1-640)<10):
                    i1 = "y"
                    i2 = "x"
                    self.searchState = "left"
                    self.Navigation.writeArduino("t+9999" + i1 + i2 + "*")
                    print("Half of the tunnel is detected, Turning Left is needed")
                 
                 
                 else:
                     print("3 Points - IDLE")
                     self.Navigation.writeArduino("i*")
                 return 0, resImg
            else:
                print("Object is not find..")
                return 0, resImg
        else:
            return 1, bgr_image


##bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Tunnel-50cm/0009.png')
##image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
##rgb_image = image
##x = Bar2Tunnel()
##retval = x.Bar2TunnelMain(1, bgr_image)
##print(retval)
