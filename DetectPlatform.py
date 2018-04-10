import cv2
import numpy as np
# import matplotlib.pyplot as plt



class DetectPlatform:

    def __init__(self):
        pass

    def PlatformDet(self, equalized_):
        rgb_image = equalized_
        # clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        # bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        # planes_ = cv2.split(rgb_image)
        # planes_[0] = clahe.apply(rgb_image[:, :, 0])
        # planes_[1] = clahe.apply(rgb_image[:, :, 1])
        # planes_[2] = clahe.apply(rgb_image[:, :, 2])
        # equalized_ = cv2.merge(planes_)

        blurred = cv2.GaussianBlur(equalized_, (5, 5), 0)
        blurred = cv2.GaussianBlur(equalized_, (15, 15), 0)
        blurred = cv2.GaussianBlur(equalized_, (15, 15), 0)
        blurred = cv2.GaussianBlur(equalized_, (15, 15), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
        # edges = cv2.filter2D(gray, cv2.CV_32F, kernel)
        edged = cv2.Canny(gray, 10, 250)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow("Closed", closed)
        # plt.imshow(closed)
        ret, bw = cv2.threshold(closed, 50, 1, cv2.THRESH_BINARY_INV)
        # ret, edges_inv = cv2.threshold(edges, 55, 255, cv2.THRESH_BINARY_INV)
        # blurred = cv2.bitwise_and(blurred, blurred, edges_inv)
        edge_power = cv2.split(blurred)
        # Color space conversion
        edge_power[0] = bw * blurred[:, :, 0]
        edge_power[1] = bw * blurred[:, :, 1]
        edge_power[2] = bw * blurred[:, :, 2]
        edge_power = cv2.merge(edge_power)

        lower = np.array([0])
        upper = np.array([100])
        image_gray0 = cv2.inRange(edge_power[:,:,0], lower, upper)
        image_gray1 = cv2.inRange(edge_power[:,:,1], lower, upper)
        image_gray2 = cv2.inRange(edge_power[:,:,2], lower, upper)
        image_gray = image_gray0 & image_gray1 & image_gray2

        mask = image_gray
        kernel = np.ones((3, 3), np.uint8)
        # Openning and closing morphologies
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        cnts_ = np.flip(sorted(cnts, key=cv2.contourArea),0)
        if len(cnts)>0:
            for i in range(2):
                c = cnts_[i]
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                ctr = np.array(c).reshape((-1, 1, 2)).astype(np.int32)
                temp_image = rgb_image.copy()
                cv2.drawContours(temp_image, [ctr], -1, (255, 255, 255), 2)
                x, y, w, h = cv2.boundingRect(c)
                # plt.imshow(temp_image)
                if (np.abs((x + w)-640) < 5 or x<5) and (np.abs((y + h)-480) < 5 or y<5) and w>100:
                    temp_image = rgb_image.copy()
                    ctr = np.array(c).reshape((-1, 1, 2)).astype(np.int32)
                    cv2.drawContours(temp_image, [ctr], -1, (255, 255, 255), 2)
                    # plt.imshow(temp_image)
                    cv2.rectangle(temp_image, (x, y), (x + w, y + h), [0,0,0],2)
                    # plt.imshow(temp_image)
                    rect = cv2.minAreaRect(c)
                    ground_find = 1
                    return (ground_find, x, y, w, h)
                else:
                    if i == 1:
                        return (0, 0, 0, 0, 0)
                    else:
                        continue

        else:
            return (0, 0, 0, 0, 0)

