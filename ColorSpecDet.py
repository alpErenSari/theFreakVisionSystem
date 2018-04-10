# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
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

        blurred = cv2.GaussianBlur(equalized_, (11, 11), 0)
        # gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
        # edged = cv2.Canny(gray, 10, 250)
        #
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        # ret, bw = cv2.threshold(closed, 50, 1, cv2.THRESH_BINARY_INV)
        # # blurred = cv2.bitwise_and(blurred, blurred, edges_inv)
        # edge_power = cv2.split(blurred)
        # # Color space conversion
        # edge_power[0] = bw * blurred[:,:,0]
        # edge_power[1] = bw * blurred[:,:,1]
        # edge_power[2] = bw * blurred[:,:,2]
        # edge_power = cv2.merge(edge_power)


        hsv = cv2.cvtColor(blurred, cv2.COLOR_RGB2HSV)
        yuv = cv2.cvtColor(blurred, cv2.COLOR_RGB2YUV)
        lab = cv2.cvtColor(blurred, cv2.COLOR_RGB2LAB)
        ycc = cv2.cvtColor(blurred, cv2.COLOR_RGB2YCR_CB)
        hls = cv2.cvtColor(blurred, cv2.COLOR_RGB2HLS_FULL)
        # luv = cv2.cvtColor(edge_power, cv2.COLOR_RGB2LUV)
        frame = rgb_image

        objects_ = []
        size_cnt = []

        # Red thresholds
        if key == 'red':


            # mean_r = np.mean(rgb_image[:, :, 0])
            # mask_r = cv2.inRange(rgb_image[:, :, 0], mean_r, 255)
            # searching for the tunnel's color in hsv and yuv

            mask_hsv = np.zeros(hsv[:,:,0].shape)
            mask_hsv[ (hsv[:,:,0]>167) | (hsv[:,:,0]<7) ] = 255

            mask_yuv = np.zeros(yuv[:,:,0].shape)
            mask_yuv[(yuv[:,:,1]>85) & (yuv[:,:,1]<128) &  (yuv[:,:,2]>150) & (yuv[:,:,2]<240)] = 255

            # mean_lab = np.mean(lab[:, :, 1])
            # mask_lab = cv2.inRange(lab[:, :, 1], mean_lab, 255)
            #
            # mean_hls1= np.mean(hls[:, :, 0])
            # mask_hls1 = cv2.inRange(hls[:, :, 0], mean_hls1, 255)
            #
            # mean_hls2= np.mean(hls[:, :, 2])
            # mask_hls2 = cv2.inRange(hls[:, :, 2], mean_hls2, 255)


            # mean_ycc = np.mean(ycc[:, :, 1])
            # mask_ycc = cv2.inRange(ycc[:, :, 1], mean_ycc, 255)


            # mask_merged = mask_hsv + mask_hls1 + mask_hls2 + mask_ycc
            # mask = mask_r &  mask_lab & mask_merged

            mask = np.zeros(hsv[:,:,0].shape)
            mask[(mask_hsv>128) & (mask_yuv>128)] = 255 # combining all the masks to create a reliable mask

        # Blue thresholds
        elif key == 'blue':

            # mean_b = np.mean(rgb_image[:, :, 2])
            # mask_b = cv2.inRange(rgb_image[:, :, 2], mean_b, 255)
            #
            # mean_lab = np.mean([lab[:, :, 2]])
            # mask_lab = cv2.inRange(lab[:, :, 2], 0, mean_lab)
            #
            # mean_ycc = np.mean([ycc[:, :, 2]])
            # mask_ycc = cv2.inRange(ycc[:, :, 2], mean_ycc, 255)
            #
            # mean_hsv1 = np.mean(hsv[:,:,0])
            # mask_hsv1 = cv2.inRange(hsv[:, :, 0], mean_hsv1, 255)
            #
            #
            # mean_hsv2 = np.mean(hsv[:,:,1])
            # mask_hsv2 = cv2.inRange(hsv[:, :, 1], mean_hsv2, 255)
            #
            # mask_hsv = mask_hsv1 + mask_hsv2
            # mask = mask_hsv & mask_lab & mask_ycc + mask_b

            # searching for the bar's color in hsv and yuv

            mask_hsv = np.zeros(hsv[:,:,0].shape)
            mask_hsv[(hsv[:,:,1]<255) & (hsv[:,:,1]>230) & (hsv[:,:,0]<130) & (hsv[:,:,0]>90) ] = 255

            mask_yuv = np.zeros(yuv[:,:,0].shape)
            mask_yuv[(yuv[:,:,1]>128) & (yuv[:,:,1]<210) &  (yuv[:,:,2]>40) & (yuv[:,:,2]<128)] = 255

            mask = np.zeros(yuv[:,:,0].shape)
            mask[(mask_hsv>128) & (mask_yuv>128)] = 255 # combining all the masks to create a reliable mask

        # Green thresholds
        elif key == 'green':
            # mean_g = np.mean(rgb_image[:, :, 1])
            # mask_g = cv2.inRange(rgb_image[:, :, 1], 0, mean_g)
            #
            # mean_lab = np.mean(lab[:, :, 1])
            # mask_lab = cv2.inRange(lab[:, :, 1], 0, mean_lab)
            #
            # mean_lab2 = np.mean(lab[:, :, 2])
            # mask_lab2 = cv2.inRange(lab[:, :, 2], mean_lab2, 255)
            #
            # mean_ycc0 = np.mean(ycc[:, :, 0])
            # mask_ycc0 = cv2.inRange(ycc[:, :, 0], 0, mean_ycc0)
            # mean_ycc1= np.mean(ycc[:, :, 1])
            # mask_ycc1 = cv2.inRange(ycc[:, :, 1], 0, mean_ycc1)
            #
            # mean_hls = np.mean(hls[:, :, 2])
            # mask_hls = cv2.inRange(hls[:, :, 2], mean_hls, 255)
            #
            # maskm = mask_ycc0 + mask_ycc1
            # mask = mask_g & mask_lab & mask_lab2 & maskm & mask_hls

            # searching for the wall's color in hsv and yuv

            mask_hsv = np.zeros(hsv[:,:,0].shape)
            mask_hsv[(hsv[:,:,1]>110) & (hsv[:,:,0]<80) & (hsv[:,:,0]>50) ] = 255

            mask_yuv = np.zeros(yuv[:,:,0].shape)
            mask_yuv[(yuv[:,:,1]>95) & (yuv[:,:,1]<128) &  (yuv[:,:,2]>50) & (yuv[:,:,2]<120)] = 255

            mask = np.zeros(yuv[:,:,0].shape)
            mask[(mask_hsv>128) & (mask_yuv>128)] = 255 # combining all the masks to create a reliable mask

        if np.sum(mask) != 0:
            kernel = np.ones((5,5), np.uint8)
            # changing into uint8 type for findContours function
            mask = np.uint8(mask)

            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            # By applying opening and closing we are enhancing the morphology

            # cv2.namedWindow("Mask", 1)
            # cv2.imshow("Mask", mask)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

            # only proceed if at least one contour was found
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea) # taking the largest contour
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                x, y, w, h = cv2.boundingRect(c)
                approxCurve = cv2.approxPolyDP(c, 10.0, True )
                temp_image = rgb_image.copy()
                temp_image = cv2.cvtColor(temp_image, cv2.COLOR_RGB2BGR)

                if w>60 and h>45:
                    #cv2.rectangle(temp_image, (x, y), (x + w, y + h), colors[key], 2)
                    # show_image = cv2.cvtColor(temp_image, cv2.COLOR_RGB2BGR)
                    # cv2.namedWindow("Binary")
                    # cv2.imshow("Binary", show_image)
                    # cv2.waitKey(0)
                    # cv2.destroyAllWindows()
                    rect = cv2.minAreaRect(c) # finds a rotated rectangle which covers the contour
                    box = cv2.boxPoints(rect) # taking the rotated rectangle's corners
                    box = np.int32(box) # converting corners into int32
                    print("The boxes are", box)

                    #cv2.rectangle(temp_image, box[1], box[3], colors[key], 2) # drawing the rectangle
                    #cv2.polylines(temp_image, c, True, (0,0,0), 3, cv2.FILLED)
                    cv2.drawContours(temp_image, [c], 0, colors[key], 3)

                    objects_ = np.append(objects_, c) # appending the largest contour into objects_
                    size_cnt = np.append(size_cnt, c.size) # appending the size of the largest contour
                    temp_points = box[1] # taking the upper left corners
                    x = temp_points[0] # taking upper left corner's x
                    y = temp_points[1] # taking upper left corner's y
                    temp_points1 = box[2] # taking the upper right corners
                    x1 = temp_points1[0] # taking upper right corner's x
                    y1 = temp_points1[1] # taking upper right corner's x
                    w = np.sqrt((x-x1)*(x-x1) + (y-y1)*(y-y1)) # calculating the width of the object
                    temp_points0 = box[0] # taking the bottom right corners
                    x0 = temp_points0[0] # taking bottom left corner's x
                    y0 = temp_points0[1] # taking bottom left corner's y
                    h = np.sqrt((x-x0)*(x-x0) + (y-y0)*(y-y0)) # calculating the height of the object
                    fd_ob = 1 # object is found flag
                    return fd_ob, objects_, temp_image,  x, y, w, h, x1, y1
                else :
                    return 0, 0, 0, 0, 0, 0, 0, 0, 0
            else:
                return 0, 0, 0, 0, 0, 0, 0, 0, 0

        else:
            return 0, 0, 0, 0, 0, 0, 0, 0

# bgr_image = cv2.imread('/home/eren/Documents/wheels_horizons/vo/FreakImage/freakData-04-04-2018/bar2Tunnel-50cm/0009.png')
# image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
# rgb_image = image
# x = ColorSpecDet()
# retval = x.ColorDet(image,'red')
# print(retval)

# bu kodda platform detectiou cıkarttık
