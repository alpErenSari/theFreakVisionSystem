import numpy as np
import cv2

class hullOrderer:
    def __init__(self):
        self.ordered = np.zeros((4,2), dtype=np.int32)
        #self.temp = np.zeros((4,2), dtype=np.int32)

    def organizer(self, imagePoints):
        # this code makes sure that we are giving the corner output in a specific order
        # respahing to (4,2) from (4,1,2)
        imagePoints = np.reshape(imagePoints, (4,2))
        # taking the values of x and y
        x_point = imagePoints[imagePoints[:, 0].argsort()] # sorting wth x values
        y_point = imagePoints[imagePoints[:, 1].argsort()] # sorting wth y values
        print("x axis is ", x_point)
        print("y axis is ", y_point)

        if ((x_point[0] == y_point[0])[0] & (x_point[0] == y_point[0])[1]) or ((x_point[0] == y_point[1])[0] & (x_point[0] == y_point[1])[1]):
            self.ordered[0] = x_point[1] # bottom left point
            self.ordered[1] = x_point[0] # upper left point
        else:
            self.ordered[0] = x_point[0] # bottom left point
            self.ordered[1] = x_point[1] # upper left point

        if ((x_point[3] == y_point[3])[0] & (x_point[3] == y_point[3])[1]) or ((x_point[3] == y_point[2])[0] & (x_point[3] == y_point[2])[1]):
            self.ordered[3] = x_point[3] # bottom right point
            self.ordered[2] = x_point[2] # upper right point
        else:
            self.ordered[3] = x_point[2] # bottom right point
            self.ordered[2] = x_point[3] # upper right point



        return self.ordered
