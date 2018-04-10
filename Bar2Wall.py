import cv2
import numpy as np
import imutils
from ColorSpecDet import ColorSpecDet as cd
import matplotlib.pyplot as plt
from shape_detector import ShapeDetector
# state = bar2wall
FlagArd = 0 #[0 : Do Nothing] # [1 : SagSol] # [2 : Navigation]
TurnLeft = 0
TurnRight = 0
Navigate = 0
b2w = 1
distance_ = 22
class Bar2Wall:
    def __init__(self):
        pass
    while(b2w):
        filename = '/home/bahart/PycharmProjects/FreakImage/Data/Wall/' \
                   '200.jpg'
        PrimaryStates = ["NothingFound", "GreenWallDetected"]
        SecondaryStates = ["WallHalf"]
        ThirdStates = ["WallFarAway", "WallNearby"]
        MiddleState = ["SearchingAWall", "SearchingWholeWall"]
        # resim surekli okunucak
        bgr_image = cv2.imread(filename)
        image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        fd_obj, objects_, size_cnt, mask = cd.ColorDet([], image, "green")
        plt.imshow(mask)
        if FlagArd == 0:
            if fd_obj:
                ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                rgb_image = image
                cv2.drawContours(rgb_image, [ctr], -1, (0, 255, 0), 2)
                plt.imshow(image)
            # ctr = np.array(objects_).reshape((-1, 1, 2)).astype(np.int32)
                sd = ShapeDetector()
                shape_, w, h = sd.detect(ctr)
                if shape_=="rectangle":
                    if (w/h<2.5): # tam olarak görmedigi yarım gördügü
                        initial_state = PrimaryStates[1]
                    else:
                        initial_state = PrimaryStates[0]
                else:
                    initial_state = PrimaryStates[0]
            else:
                initial_state = PrimaryStates[0]

            if initial_state == PrimaryStates[1]: # GreenWallDetected
                if ((w/h)-1.42)<=0.9: # oranı kontrol et
                    if distance_ <= 25: # uzaklıga bak
                        second_state = ThirdStates[1] # yakında
                        FlagArd = 1
                        Navigate = 1 # burda distance hesaplıcaz
                    else :
                        second_state = ThirdStates[0] # uzakta
                        
                else:
                    second_state = SecondaryStates[0] # yarım goruyoruz

            if initial_state == PrimaryStates[0]: # Searching For a Wall
                FlagArd = 1
                TurnLeft = 1
                middlestate_ = MiddleState[0]






    M = cv2.moments(ctr)
    cX = int((M["m10"] / M["m00"]))
    cY = int((M["m01"] / M["m00"]))
    c = ctr.astype("float")
    c = ctr.astype("int")
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, shape_, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 2)
    plt.imshow(image)
