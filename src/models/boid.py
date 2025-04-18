from abc import ABC, abstractmethod
from .vector import *

class Boid(ABC):
    def __init__ (self, size:int|float, colour:str, max_speed:int|float, avoid_dist:int|float, initial_pos:tuple|Vector, initial_heading_degrees:int|float=0) -> None:
        """
        Abstract class representing a boid https://en.wikipedia.org/wiki/Boids

        :param int|float size: maximum size of boid in a given unit (if drawing to screen then pixels)
        :param str colour: colour of boid in hex
        :param int|float max_speed: maximum speed of boid unit/ms
        :param int|float avoid_dist: avoid distance of boid from other boids
        :param tuple|Vector initial_pos: initial position vector of boid
        :param int|float initial_heading_degrees: initial heading of boid in degrees (will be converted to radians)
        """
        super().__init__(size, "#FFFFFF", max_speed, avoid_dist, initial_pos, initial_heading_degrees)
        
        self.radius = size/2
        self.max_speed = max_speed
        if type(initial_pos) == Vector:
            initial_pos = (initial_pos.i, initial_pos.j)
        self.x, self.y = initial_pos
        self.heading = initial_heading_degrees*math.pi/180
        self.colour = colour
        self.avoid_dist = avoid_dist

        self.get_draw_point = lambda angle, scale=1: (math.cos(angle)*self.radius*scale+self.x, math.sin(angle)*self.radius*scale+self.y)

    @property
    def pos(self) -> tuple:
        """
        Boid position as tuple
        """
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, new_pos:tuple[float, float]) -> None:
        self.x, self.y = new_pos
    
    @property
    def posv(self) -> Vector:
        """
        Boid position as position vector
        """
        return Vector(self.x, self.y)
    
    @property
    def heading_line(self) -> tuple:
        """
        Point in direction boid is facing
        """
        return self.get_draw_point(self.heading, 2)

    @property
    def draw_points(self) -> list:
        """
        Points for drawing boid (connect points together)
        """
        head = self.get_draw_point(self.heading)
        point_1 = self.get_draw_point(self.heading+5*math.pi/6)
        point_2 = self.get_draw_point(self.heading-5*math.pi/6)
        middle_point = self.get_draw_point(self.heading+math.pi, 0.5)
        return [head, point_1, middle_point, point_2]
    
    @abstractmethod
    def update(self) -> None:
        """
        Update Boid
        """
        pass