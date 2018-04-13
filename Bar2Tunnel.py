import cv2
import numpy as np
from ColorSpecDet import ColorSpecDet
from shape_detector import ShapeDetector
from RedTunnelDetected import RedTunnelDetected
from CalculateDistance import calculateDist
from i2c import ard_i2c as Navigation

class Bar2Tunnel:
    def __init__(self):
        self.cd = ColorSpecDet()
        self.RTD = RedTunnelDetected()
        self.sd = ShapeDetector()
        self.pose = calculateDist()

    def Bar2TunnelMain(self, start_flag, bgr_image):
        if start_flag:
            PrimaryStates = ["NothingFound", "TunnelDetected"]
            image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            fd_obj, objects_, resImg, imagePoints, w_color, h_color = self.cd.ColorDet(image.copy(), "red")
            # taking the upper left and right corners of the object
            x_color, y_color = imagePoints[1][0], imagePoints[1][1]
            x_color1, y_color1 = imagePoints[2][0], imagePoints[2][1]
            stop_flag = 0
            if fd_obj:
                ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                shape_, w, h = self.sd.detect(ctr)
                if shape_ == "rectangle" or shape_ == "tunnel":
                    if w_color / h_color < 4.5:
                        initial_state = PrimaryStates[1]
                    else:
                        initial_state = PrimaryStates[0]
                else:
                    initial_state = PrimaryStates[0]
            else:
                initial_state = PrimaryStates[0]

            if initial_state == PrimaryStates[0]:
                # Navigation.writeArduino([], "s1*")
                return stop_flag, resImg

            else:
                nfd = 1
            if nfd == 0:
                # Navigation.writeArduino([], "s1*")
                print("Tunnel Not Found")
                return stop_flag, resImg

            else:
                #half_ = self.RTD.RedTunnelDetected(w_color, h_color)
                half_ = 0
                if half_ == 1:

                    if ((x_color < 20) or (x_color1 -640 > 20) ) :
                        # right is not seen
                        i1 = "y"
                        i2 = "x"
                    else:
                        i1 = "x"
                        i2 = "y"
                    # Navigation.writeArduino([], "t00000" + i1 + i2)
                    print("Half of the tunnel is detected, Turning Left is needed")
                    return stop_flag, resImg

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
                    if (x_color < 10) and (y_color < 10) and abs(x_color1 - 640) < 10 and abs(y_color1 - 0) < 10:
                        state_ = "Passing Tunnel"
                        stop_flag = 1
                        return stop_flag, resImg
                    # Navigation.writeArduino([], "t" + s + np.str(angle) + np.str(dist_ / 10) + "yy*")
                    return stop_flag, resImg
        else:
            return 1, resImg

##bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Tunnel-50cm/0009.png')
##image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
##rgb_image = image
##x = Bar2Tunnel()
##retval = x.Bar2TunnelMain(1, bgr_image)
##print(retval)
