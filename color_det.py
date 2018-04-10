# # from picamera.array import PiRGBArray
# # from picamera import PiCamera
# import time
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# filename = '/home/bahart/PycharmProjects/FreakImage/Data/Tunnel/13.jpg'
# bgr_image = cv2.imread(filename)
# gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
# rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
# plt.imshow(rgb_image)
# def DetectColor(rgb_image):
#     lower = {'red': (90, 0, 20), 'green': (50, 122, 60), 'blue': (10, 50, 60)}  # assign new item lower['blue'] = (93, 10, 0)
#     upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255)}
#     # lower = {'red': (0, 100, 100), 'green': (66, 122, 129), 'blue': (97, 100, 117), 'yellow': (23, 59, 119),
#     #          'orange': (0, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
#     # upper = {'red': (20, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255), 'yellow': (54, 255, 255),
#     #          'orange': (20, 255, 255)}
#     # define standard colors for circle around the object
#     colors = {'blue': (0, 0, 255), 'green': (0, 255, 0), 'red': (255, 0, 0)}
#     bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
#     blurred = cv2.GaussianBlur(bgr_image, (11, 11), 0)
#     hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
#     frame =rgb_image
#     objects_ = []
#     count = 1
#     size_cnt = []
#     # for each color in dictionary check object in frame
#     for key, value in upper.items():
#
#         # construct a mask for the color from dictionary`1, then perform
#         # a series of dilations and erosions to remove any small
#         # blobs left in the mask
#         kernel = np.ones((10,10), np.uint8)
#         mask = cv2.inRange(hsv, lower[key], upper[key])
#         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#         mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
#
#         # find contours in the mask and initialize the current
#         # (x, y) center of the ball
#         cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
#                                 cv2.CHAIN_APPROX_SIMPLE)[-2]
#         center = None
#
#         # only proceed if at least one contour was found
#         if len(cnts) > 0:
#             # find the largest contour in the mask, then use
#             # it to compute the minimum enclosing circle and
#             # centroid
#             c = max(cnts, key=cv2.contourArea)
#             ((x, y), radius) = cv2.minEnclosingCircle(c)
#             M = cv2.moments(c)
#             center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#
#             # only proceed if the radius meets a minimum size. Correct this value for your obect's size
#             if radius > 0.5:
#                 # draw the circle and centroid on the frame,
#                 # then update the list of tracked points
#                 cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
#                 cv2.putText(frame, key + " object", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
#                             colors[key], 2)
#                 objects_ = np.append(objects_, cnts)
#                 size_cnt = np.append(size_cnt,cnts.__sizeof__())
#     plt.imshow(frame)
#     plt.show()
#     return objects_, size_cnt
#
#
#     # show the frame to our screen
#     # cv2.imshow("Frame", frame)
#
# aa, bb = DetectColor(rgb_image)
# # key = cv2.waitKey(1) & 0xFF
# # if the 'q' key is pressed, stop the loop
#
#
