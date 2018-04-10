import cv2
import numpy as np
# import matplotlib.pyplot as plt
from DetectPlatform import DetectPlatform as DetP

class ColorSpecDet:

    def __init__(self):
        pass

    def ColorDet(self, rgb_image, key):

        colors = {'blue': (0, 0, 255), 'green': (0, 255, 0), 'red': (255, 0, 0)}
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        planes_ = cv2.split(rgb_image)
        planes_[0] = clahe.apply(rgb_image[:, :, 0])
        planes_[1] = clahe.apply(rgb_image[:, :, 1])
        planes_[2] = clahe.apply(rgb_image[:, :, 2])
        equalized_ = cv2.merge(planes_)

        blurred = cv2.GaussianBlur(equalized_, (5, 5), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
        edged = cv2.Canny(gray, 10, 250)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        ret, bw = cv2.threshold(closed, 50, 1, cv2.THRESH_BINARY_INV)
        # blurred = cv2.bitwise_and(blurred, blurred, edges_inv)
        edge_power = cv2.split(blurred)
        # Color space conversion
        edge_power[0] = bw * blurred[:,:,0]
        edge_power[1] = bw * blurred[:,:,1]
        edge_power[2] = bw * blurred[:,:,2]
        edge_power = cv2.merge(edge_power)

        hsv = cv2.cvtColor(edge_power, cv2.COLOR_RGB2HSV)
        lab = cv2.cvtColor(edge_power, cv2.COLOR_RGB2LAB)
        ycc = cv2.cvtColor(edge_power, cv2.COLOR_RGB2YCR_CB)
        hls = cv2.cvtColor(edge_power, cv2.COLOR_RGB2HLS_FULL)
        luv = cv2.cvtColor(edge_power, cv2.COLOR_RGB2LUV)
        frame = rgb_image

        objects_ = []
        size_cnt = []

        # Red thresholds
        if key == 'red':
            lower = np.array([0, 140, 100])
            upper = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv, lower, upper)

            lower = np.array([170])
            upper = np.array([210])
            mask_luv2 = cv2.inRange(luv[:,:,1], lower, upper)
            lower = np.array([230])
            upper = np.array([255])
            mask_hls1 = cv2.inRange(hls[:, :, 0], lower, upper)

            lower = np.array([190])
            upper = np.array([200])
            mask_lab2 = cv2.inRange(lab[:, :, 1], lower, upper)

            # lower = np.array([55, 175, 150])
            # upper = np.array([130, 210, 200])
            # mask3 = cv2.inRange(lab, lower, upper)

            lower = np.array([70, 200, 95])
            upper = np.array([110, 230, 113])
            mask4 = cv2.inRange(ycc, lower, upper)

            mask = mask_hls1 + mask4 + mask_lab2
            mask = mask & mask1 &  mask_luv2

        # Blue thresholds
        elif key == 'blue':
            lower = np.array([80])
            upper = np.array([140])
            mask1 = cv2.inRange(hsv[:,:,0], lower, upper)

            lower = np.array([70])
            upper = np.array([110])
            mask2 = cv2.inRange(lab[:, :, 2], lower, upper)

            lower = np.array([80])
            upper = np.array([125])
            mask3 = cv2.inRange(ycc[:, :, 1], lower, upper)

            lower = np.array([70])
            upper = np.array([100])
            mask4 = cv2.inRange(luv[:, :, 1], lower, upper)

            lower = np.array([90])
            upper = np.array([255])
            mask4 = cv2.inRange(hls[:, :, 0], lower, upper)
            lower = np.array([0])
            upper = np.array([60])
            mask5 = cv2.inRange(hls[:, :, 2], lower, upper)

            mask_sum = mask1 + mask2 + mask3 + mask4 + mask5
            mask = mask_sum
        # Green thresholds
        elif key == 'green':
            lower = np.array([25, 240, 80])
            upper = np.array([60, 255, 200])
            mask1 = cv2.inRange(hsv, lower, upper)


            lower = np.array([70])
            upper = np.array([110])
            mask2 = cv2.inRange(lab[:,:,1], lower, upper)


            lower = np.array([80])
            upper = np.array([120])
            mask3 = cv2.inRange(ycc[:,:,1], lower, upper)

            lower = np.array([60])
            upper = np.array([80])
            mask4 = cv2.inRange(luv[:, :, 1], lower, upper)

            lower = np.array([80, 90, 55])
            upper = np.array([130, 130, 90])
            mask5 = cv2.inRange(ycc, lower, upper)

            maskm = mask2 + mask3 + mask4 + mask5
            mask = mask1 & maskm
        if np.sum(mask) != 0:
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                x, y, w, h = cv2.boundingRect(c)
                # out = np.zeros(frame.shape, np.uint8)
                temp_image = rgb_image.copy()

                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if w>60 and h>45 and radius >0.6:
                    # draw the rectangle on the frame,
                    cv2.rectangle(temp_image, (x, y), (x + w, y + h), colors[key], 2)
                    # plt.imshow(temp_image)
                    rect = cv2.minAreaRect(c)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                    cv2.putText(frame, key + " ", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                colors[key], 2)
                    objects_ = np.append(objects_, c)
                    size_cnt = np.append(size_cnt, c.size)

                    fd_ob = 1
                    (platform_, plt_x, plt_y, plt_w, plt_h) = DetP.PlatformDet([], equalized_)
                    if platform_:
                        if x < plt_x and (y+int(h/2)) < plt_y:
                            ctr = np.array(c).reshape((-1, 1, 2)).astype(np.int32)
                            cv2.drawContours(temp_image, [ctr], -1, (255, 255, 255), 2)
                            # plt.imshow(temp_image)
                            return fd_ob, objects_, x, y, w, h

                        else:
                            return 0, 0, 0, 0, 0, 0
                    else:
                        if x<5 or y<5 or (x+w-640)<5 or (y+w -480)<5:
                            ctr = np.array(c).reshape((-1, 1, 2)).astype(np.int32)
                            cv2.drawContours(temp_image, [ctr], -1, (255, 255, 255), 2)
                            # plt.imshow(temp_image)
                            return fd_ob, objects_, x, y, w, h
                        else :
                            return 0, 0, 0, 0, 0, 0

                else :
                    return 0, 0, 0, 0, 0, 0
            else:
                return 0, 0, 0, 0, 0, 0

        else:
            return 0, 0, 0, 0, 0, 0
