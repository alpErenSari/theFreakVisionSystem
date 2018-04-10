# from picamera.array import PiRGBArray
# from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import ColorSpecDet

# initialize the camera and grab a reference to the raw camera capture
# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 50
# camera.hflip = True

# rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
# time.sleep(0.1)

# capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    # image = frame.array
lower = {'red': (90, 0, 20), 'green': (50, 122, 60), 'blue': (10, 50, 60)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255)}
# lower = {'red': (0, 100, 100), 'green': (66, 122, 129), 'blue': (97, 100, 117), 'yellow': (23, 59, 119),
#          'orange': (0, 50, 80)}  # assign new item lower['blue'] = (93, 10, 0)
# upper = {'red': (20, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255), 'yellow': (54, 255, 255),
#          'orange': (20, 255, 255)}
# define standard colors for circle around the object
colors = {'blue': (0, 0, 255), 'green': (0, 255, 0), 'red': (255, 0, 0)}

filename = '/home/bahart/PycharmProjects/FreakImage/Data/Tunnel/1.jpg'
bgr_image = cv2.imread(filename)
gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

lower = {'red': (0, 20, 80), 'green': (50, 122, 60), 'blue': (10, 50, 60)}  # assign new item lower['blue'] = (93, 10, 0)
upper = {'red': (186, 255, 255), 'green': (86, 255, 255), 'blue': (117, 255, 255)}

blurred = cv2.GaussianBlur(bgr_image, (11, 11), 0)
hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
ycr = cv2.cvtColor(blurred, cv2.COLOR_BGR2YCrCb)
all = hsv[:,:,0] + hsv[:,:,1] + lab[:,:,1] + lab[:,:,2] + ycr[:,:,1] +ycr[:,:,2]
frame =rgb_image
# for each color in dictionary check object in frame
for key, value in upper.items():
    # construct a mask for the color from dictionary`1, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.inRange(hsv, lower[key], upper[key])
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size. Correct this value for your obect's size
        if radius > 0.5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
            cv2.putText(frame, key + " object", (int(x - radius), int(y - radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        colors[key], 2)

# show the frame to our screen
# cv2.imshow("Frame", frame)
plt.imshow(frame)
plt.show()
# key = cv2.waitKey(1) & 0xFF
# if the 'q' key is pressed, stop the loop


