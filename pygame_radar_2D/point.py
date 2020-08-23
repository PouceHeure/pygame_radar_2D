import math 

class PointPolar: 

    def __init__(self,theta,r,theta_in_deg=True):
        if(theta_in_deg):
            self.theta = math.radians(theta)
        else: 
            self.theta = theta
        self.r = r 

    def convert_to_point(self): 
        x = math.cos(self.theta) * self.r
        y = math.sin(self.theta) * self.r
        return Point(x,y)


class Point: 

    def __init__(self,x,y):
        self.x = x 
        self.y = y 

    def to_pos(self):
        return (int(self.x),int(self.y))

    def __repr__(self): 
        return f"(x:{self.x}, y:{self.y})"
