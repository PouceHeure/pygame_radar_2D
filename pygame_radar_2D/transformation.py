import math 
from .point import Point, PointPolar

class VectorTranslation: 

    def __init__(self,x,y):
        self.x = x 
        self.y = y 

    def __repr__(self):
        return f"(x:{self.x}, y:{self.y})"

class VectorOrientation: 

    def __init__(self,w,is_deg=True):
        if(is_deg): 
            self.w = math.radians(w)
        else: 
            self.w = w

    def __repr__(self):
        return f"(w:{self.w})"        

class Transformation: 

    def __init__(self, frame_name_from, frame_name_to, translation, orientation):
        self._translation = translation
        self._orientation = orientation
        self._frame_name_from = frame_name_from
        self._frame_name_to = frame_name_to
        HANDLER_FRAMES.register_transformation(frame_name_from,frame_name_to,self)

    def transform(self, point):
        w = self._orientation.w
        x = math.cos(w)*point.x - math.sin(w)*point.y
        y = math.sin(w)*point.x + math.cos(w)*point.y 
        x = x + self._translation.x 
        y = y + self._translation.y 
        new_point = Point(x,y)
        return new_point

    def __repr__(self):
        return f"translation: {self._translation}, orientation: {self._orientation}"

class HandlerFrames: 

    def __init__(self):
        self._frames = {}

        self._transformations_relation = {}
        self._transformations = {}

    def register_frame(self,frame): 
        name = frame.get_name()
        if(not name in self._frames.keys()):
            self._frames[name] = frame
            return True

        print(f"can't register frame {name}, other frame have already this name")
        return False 

    def _check_frame_exist(self,name):
        return name in self._frames.keys()

    def _hash_relation(self,frame_name_from,frame_name_to):
        return frame_name_from+":"+frame_name_to

    def register_transformation(self,frame_name_from,frame_name_to,transformation):
        if(not self._check_frame_exist(frame_name_from)):
            print("error")
        if(not self._check_frame_exist(frame_name_to)):
            print("error")

        self._transformations_relation[frame_name_from] = frame_name_to
        key_relation = self._hash_relation(frame_name_from,frame_name_to)
        self._transformations[key_relation] = transformation 

    def _compute_path_transformations(self,frame_name_from, frame_name_to):
        path_transformations = []
        current_frame_name = frame_name_from
        while(current_frame_name != frame_name_to): 
            next_frame_name = self._transformations_relation[current_frame_name]
            path_transformations.append((current_frame_name,next_frame_name))
            current_frame_name = next_frame_name 
        return path_transformations

    def transform(self, frame_name_from, frame_name_to, point): 
        path_transformations = self._compute_path_transformations(frame_name_from,frame_name_to)
        for transformation_relation in path_transformations: 
            key_transformation = self._hash_relation(transformation_relation[0],transformation_relation[1])
            transformation = self._transformations[key_transformation]
            point = transformation.transform(point)
        return point

class Frame: 
    
    def __init__(self,name,is_origin=False):
        self._is_origin = is_origin
        self._name = name      
        if(not HANDLER_FRAMES.register_frame(self)): 
            print("frame doesn't registered") 

    def get_name(self):
        return self._name 

    def get_is_origin(self): 
        return self._is_origin    


def rescale_point_polar(point,length,max_value_show): 
    new_r = point.r * length / (max_value_show*1.0)
    return PointPolar(point.theta,new_r,theta_in_deg=False)

HANDLER_FRAMES = HandlerFrames()



