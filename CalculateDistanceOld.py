import numpy as np
import cv2
import math 

class calculateDist:

    def __init__(self):
        # camera parameters in mm calibrated for Raspberry Pi camera
        # average reprojection error is 0.119
        # defining the camera matrix and distortion coefficients
        self.cameraMatrix = np.array([[628.60, 0, 325.24],
            [0, 623.32, 237.67], [0, 0, 1.0]]) # defining the camera matrix in mm
        self.distCoeffs = np.array([0.11909, -0.55747, 0.0, 0.0, 0.4596])

    def distNAngle(self, object, imagePoints):

        imagePoints = np.float32(imagePoints)

        if (object is "tunnel"):
            objectPoints = np.array([[-122.5 ,0 ,0],
            [-122.5 ,-150 ,0],[122.5 ,-150 ,0],[122.5 ,0 ,0]],
            dtype = np.float32) # define 3D object points for tunnel
        elif (object is "wall"):
            objectPoints = np.array([[-120 ,0 ,0],
            [-120 ,-110 ,0],[120 ,-110 ,0],[120 ,0 ,0]],
            dtype = np.float32) # define 3D object points for wall
        else:
            objectPoints = np.array([[-22.5 ,0 ,0],
            [-22.5 ,-121 ,0],[22.5 ,-121 ,0],[22.5 ,0 ,0]],
            dtype = np.float32) # define 3D object points for bar

        _, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, self.cameraMatrix, self.distCoeffs)
        Rt,_ = cv2.Rodrigues(rvec)
        R = Rt.transpose()
        pos = -R * tvec
        
        sy = math.sqrt(Rt[2,1]*Rt[2,1] + Rt[2,2]*Rt[2,2])
        singular = sy < 1e-6
        
        roll = math.atan2(-R[2][1], R[2][2])
        pitch = math.asin(R[2][0])
        yaw = math.atan2(-R[1][0], R[0][0])

        dist = np.linalg.norm(tvec)
        rollDegree = 180*pitch/3.1415926 # coverting the roll into degree from radian

        #print("The resulting distance and angle are (%f,%f)"%(dist, roll))

        return dist/10.0, rollDegree
