import math

class calculateDist:

    def __init__(self):
        pass

    def distNAngle(self, object, u1, v1, u2, v2):

        # camera parameters in mm calibrated for Raspberry Pi camera
        # average reprojection error is 0.119
        fx = 656.51
        fy = 651.16
        # fx = 5.0*656.51/3.0
        # fy = 5.0*651.16/3.0
        cx = 292.18
        cy = 234.45
        # pixel coordinates
        # the coordinate calculations
        if (object is "tunnel"):
            y = -30.0 # tunnel
        elif (object is "wall"):
            y = -20.0 # wall
        elif (object is "bar"):
            y = -20.0 # bar
        else:
            y = -25.0

        #v2 = v2 + 29.0 # due to tilt of camera, correction
        z1 = (fy*y)/(v1-cy)
        x1 = ((u1-cx)*z1)/fx

        z2 = (fy*y)/(v2-cy)
        x2 = ((u2-cx)*z2)/fx

        x = (x1 + x2)/2.0
        z = (z1 + z2)/2.0


        print("The resulting coordinates are (%f,%f) and (%f,%f)"%(x1,z1,x2,z2))
        dist = math.sqrt(x**2.0 + z**2.0)
        diff_x = x2 - x1
        diff_z = z2 - z1
        #angle = 180*math.atan(diff_z/diff_x)/3.1415926
        angle = v2 - v1 + 29 # adjustment due to camera tilt
        # assumed that v2 and v1 difference is proportional to angle
        # positive angle means actual angle is positive
        print("The difference is %f"%diff_x)
        return dist/10.0, angle
