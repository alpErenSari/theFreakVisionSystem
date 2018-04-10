# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
#
# filename = '/home/bahart/PycharmProjects/FreakImage/Data/Tunnel/12.jpg'
# bgr_image = cv2.imread(filename)
# gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
# rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
# plt.imshow(rgb_image)

class ColorSpecDet:

    def __init__(self):
        pass

    def ColorDet(self, rgb_image, SpecColor):

        lower = {'red': (90, 0, 20), 'green': (50, 122, 60),
                 'blue': (10, 50, 60)}  # assign new item lower['blue'] = (93, 10, 0)
        upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255)}

        colors = {'blue': (0, 0, 255), 'green': (0, 255, 0), 'red': (255, 0, 0)}
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        blurred = cv2.GaussianBlur(bgr_image, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        frame = rgb_image
        objects_ = []
        count = 1
        size_cnt = []
        # for each color in dictionary check object in frame
        # for key, value in upper.items():
        key = SpecColor
        value = upper.get(SpecColor)
            # construct a mask for the color from dictionary`1, then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
        kernel = np.ones((10, 10), np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        if np.sum(mask) != 0:
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                x, y, w, h = cv2.boundingRect(c)

                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if w>125 and h > 125:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.rectangle(frame, (x, y), (x + w, y + h), colors[key], 2)
                    cv2.putText(frame, key + " ", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                colors[key], 2)
                    objects_ = np.append(objects_, c)
                    size_cnt = np.append(size_cnt, c.size)

            plt.imshow(frame)
            plt.show()
            fd_ob = 1
            return fd_ob, objects_, size_cnt, mask
        else:
            fd_ob = 0
            objects_ = 0
            size_cnt = 0
            mask = 0
            return fd_ob, objects_, size_cnt, mask
        # show the frame to our screen
        #  cv2.imshow("Frame", frame)
#
# colordet = ColorSpecDet()
# fd_obj, objects_, size_cnt, mask = colordet.ColorDet(rgb_image, "red")