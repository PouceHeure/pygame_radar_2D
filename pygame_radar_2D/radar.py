import math 
import pygame 

from .transformation import *

BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)


class ElementUI: 

    def paint(self,screen): 
        pass 

class CircleUI(ElementUI): 

    def __init__(self,point_center,radius): 
        self.point_center = point_center
        self.radius = radius

    def paint(self,screen): 
        pygame.draw.circle(screen, GREEN, self.point_center.to_pos(), self.radius, 2)

class PointUI(ElementUI): 

    def __init__(self,point):
        self.point = point 

    def paint(self,screen):
        pygame.draw.circle(screen, RED, self.point.to_pos(), 5)

class ScannLineUI(ElementUI): 

    def __init__(self,point_center,radius,theta): 
        self.point_center = point_center
        self.point_end = self.compute_end_point(radius,theta)

    def compute_end_point(self,r,theta):
        x = self.point_center.x + r * math.cos(theta)
        y = self.point_center.y + r * math.sin(theta)
        return Point(x,y)

    def paint(self,screen): 
        pygame.draw.line(screen, GREEN, self.point_center.to_pos(),self.point_end.to_pos(), 2)


class RadarUI: 

    def __init__(self,side,r_lim):
        self.scannlines_ui = [] 
        self.points_UI = []
        self.circles_UI = []

        self.side = side
        self.r_lim = r_lim 

        frame_origin = Frame("origin",is_origin=True)
        frame_1 = Frame("frame_1")
        v1_t = VectorTranslation(side/2,side/2)
        v1_o = VectorOrientation(-90)
        Transformation("frame_1","origin",v1_t,v1_o)

        self.point_center = HANDLER_FRAMES.transform("frame_1","origin",Point(0,0))

    def paint(self,screen):
        screen.fill(BLACK)
        elements_UI = self.scannlines_ui + self.circles_UI + self.points_UI
        for element in elements_UI: 
            element.paint(screen)
        pygame.display.update()

    def update_circles(self,circles_radius): 
        self.circles_UI = []
        for radius in circles_radius: 
            self.circles_UI.append(CircleUI(self.point_center,radius))

    def update_points(self,points_polar): 
        self.points_UI = []
        for p in points_polar: 
            p = rescale_point_polar(p,self.side/2,self.r_lim)
            p_cart = p.convert_to_point()
            p_transform = HANDLER_FRAMES.transform("frame_1","origin",p_cart)
            self.points_UI.append(PointUI(p_transform))

    def update_scannlines(self,radius,theta_deg): 
        self.scannlines_ui = []
        self.scannlines_ui.append(ScannLineUI(self.point_center,radius,math.radians(theta_deg)))

class Radar: 

    def __init__(self,side,r_lim=300,fps=30):
        self.side = side 
        circles_percent = [0.25,0.50,0.75,0.100]
        circles_radius = []
        for percent in circles_percent: 
            circles_radius.append(int(side*percent))
        self.radar_ui = RadarUI(side,r_lim)
        self.radar_ui.update_circles(circles_radius)
        self.fps = fps

    def _start(self):
        pygame.init()
        screen = pygame.display.set_mode((self.side, self.side))
        clock = pygame.time.Clock()
        deg = 0
        while True:
            for event in pygame.event.get():
                if((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) 
                                or (event.type == pygame.QUIT)):
                        pygame.quit()
                        return
            deg += 1
            deg = deg % 360

            self.radar_ui.update_scannlines(self.side/2,deg)
            self.radar_ui.paint(screen)
            clock.tick(self.fps)

    def start(self): 
        import threading
        self.thread = threading.Thread(target=self._start)
        self.thread.start()

    def set_points(self,points_polar): 
        self.radar_ui.update_points(points_polar)