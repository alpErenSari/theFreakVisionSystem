import cv2
import numpy as np
import imutils
from ColorSpecDet import ColorSpecDet as cd
import matplotlib.pyplot as plt
class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        w = 0
        h = 0
        # Wall ==> w/h = 26/12
        # Bar ==> w/h = 0.589
        # Tunnel ==> w/h = 21/11

        if len(approx) >= 4 and len(approx)<=5:
            (x, y, w, h) = cv2.boundingRect(approx)
            # ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "rectangle"# if ar >= 0.95 and ar <= 1.05 else "rectangle"

        elif len(approx) >=6 and len(approx)<=30:
            shape = "tunnel"

            w = 0
            h = 0
        else:
            shape = "nothing"
            w = 0
            h = 0
        # return the name of the shape
        return shape, w, h




#
#
#
# cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
#                         cv2.CHAIN_APPROX_SIMPLE)
#
#
#
#
#
#
#
#
#
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
#
#
#
#
#
#
#
#
# for c in cnts:
#     # compute the center of the contour, then detect the name of the
#     # shape using only the contour
#     M = cv2.moments(c)
#     cX = int((M["m10"] / M["m00"]))
#     cY = int((M["m01"] / M["m00"]))
#     shape, w, h = sd.detect(c)
#
#     # multiply the contour (x, y)-coordinates by the resize ratio,
#     # then draw the contours and the name of the shape on the image
#     c = c.astype("float")
#     c = c.astype("int")
#     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
#     cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5, (255, 255, 255), 2)
#
#     # show the output image
#     cv2.imshow("Image", image)
#     cv2.waitKey(0)