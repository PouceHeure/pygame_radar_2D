from pygame_radar_2D.radar import Radar
from pygame_radar_2D.point import PointPolar

if __name__ == '__main__':
    radar = Radar(300,r_lim=300)
    radar.start()
   
    import random 
    import time
    theta = 0
    r = 115 

    while True: 
        theta += random.choice([-5,5])
        r += random.choice([-1,1])
        radar.set_points([PointPolar(theta,r)])
        time.sleep(0.1) 