import numpy as np
import cv2

class hullOrderer:
    def __init__(self):
        self.ordered = np.zeros((4,2), dtype=np.int32)
        #self.temp = np.zeros((4,2), dtype=np.int32)

    def organizer(self, imagePoints):
        # this code makes sure that we are giving the corner output in a specific range
        # respahing to (4,2) from (4,1,2)
        imagePoints = np.reshape(imagePoints, (4,2))
        # taking the values of x and y
        x_point = imagePoints[imagePoints[:, 0].argsort()]
        y_point = imagePoints[imagePoints[:, 1].argsort()]
        print("x axis is ", x_point)
        print("y axis is ", y_point)

        if ((x_point[0] == y_point[0])[0] & (x_point[0] == y_point[0])[1]) or ((x_point[0] == y_point[1])[0] & (x_point[0] == y_point[1])[1]):
            self.ordered[0] = x_point[1] # point 0
            self.ordered[1] = x_point[0]
        else:
            self.ordered[0] = x_point[0]
            self.ordered[1] = x_point[1]

        if ((x_point[3] == y_point[3])[0] & (x_point[3] == y_point[3])[1]) or ((x_point[3] == y_point[2])[0] & (x_point[3] == y_point[2])[1]):
            self.ordered[3] = x_point[3] # point 3
            self.ordered[2] = x_point[2]
        else:
            self.ordered[3] = x_point[2]
            self.ordered[2] = x_point[3]



        return self.ordered
