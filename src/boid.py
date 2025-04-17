import math, random

from .settings import *
from .vector import *

class Boid:
    def __init__ (self, size:int|float, max_speed:int|float,  posv:tuple|Vector, heading_degrees:int|float) -> None:
        """
        Class representing a boid https://en.wikipedia.org/wiki/Boids

        :param int|float size: maximum size of boid in a given unit (if drawing to screen then pixels)
        :param int|float max_speed: maximum speed of boid unit/ms
        :param tuple|Vector posv: initial position vector of boid
        :param int|float heading: initial heading of boid in degrees (will be converted to radians)
        """
        self.radius = size/2
        self.max_speed = max_speed
        if type(posv) == tuple:
            posv = Vector(posv[0], posv[1])
        self.x, self.y = posv.i, posv.j
        self.heading = heading_degrees*math.pi/180
        self.colour = "#FFFFFF"
        
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

    def __get_noise_vector(self) -> Vector:
        """
        Generate random noise vector
        """
        new_heading = random.randint(-5, 5)*math.pi/180 + self.heading
        speed = random.randint(1, 10)/10
        return Vector(math.cos(new_heading), math.sin(new_heading)).unit*speed
    
    def __get_boid_vectors(self, local_boids:list[tuple]) -> tuple[Vector, Vector, Vector]:
        """
        Returns seperation, alignment and cohesion vectors
        """
        sep_vectors, heading_vectors, centre_of_mass = [], [], 0
        for posv, heading in local_boids:
            distance = (posv-self.posv).magnitude
            if distance == 0:
                distance = 0.01 # prevent zero division error
            if distance <= BOID_AVOID_DIST:
                sep_vectors.append(1/(self.posv-posv))
            heading_vectors.append(Vector(math.cos(heading)*100*(1/distance), math.sin(heading)*100*(1/distance)))
            centre_of_mass += posv
        
        seperation_v = Vector(0, 0) if len(sep_vectors) == 0 else sum(sep_vectors).unit
        alignment_v = sum(heading_vectors).unit
        cohesion_v = ((centre_of_mass/len(local_boids)-self.posv)*0.3).unit

        return seperation_v, alignment_v, cohesion_v
    
    def __get_obstacle_avoidance_vector(self, local_obstacles:list[Vector]) -> Vector:
        """
        Returns calculated avoidance vector
        """
        avoid_vectors = [1/(self.posv-posv) for posv in local_obstacles]
        return Vector(0, 0) if len(avoid_vectors) == 0 else sum(avoid_vectors).unit
    
    def __move(self, speed:int|float, delta_time:int|float) -> None:
        """
        Move forward with given speed (accounts for time delay between frames)
        """
        move_speed = min(speed, self.max_speed)
        self.x += math.cos(self.heading)*move_speed*delta_time
        self.y += math.sin(self.heading)*move_speed*delta_time
    
    def __calculate_move(self, delta_time:int|float, vect:Vector) -> None:
        """
        Calculate new boid angle and position based on movement vector
        (Boids can only move forward so the angle is incremented towards the direction of movement)
        """
        get_alt_heading = lambda heading: heading-2*math.pi if heading > 0 else heading+2*math.pi
        choose_dir = lambda dir1, dir2: dir1 if abs(dir1) <= abs(dir2) else dir2
        delta_heading = vect.heading - self.heading
        if delta_heading != 0:
            heading_dir = choose_dir(delta_heading, get_alt_heading(delta_heading))
            self.heading += heading_dir*0.3
        self.__move(vect.magnitude, delta_time)
    
    def update(self, delta_time:int|float, local_boids:list[tuple], local_obstacles:list[Vector]) -> None:
        noise_v = self.__get_noise_vector()
        if len(local_boids) == 0:
            self.__calculate_move(delta_time, noise_v)
            return

        seperation_v, alignment_v, cohesion_v = self.__get_boid_vectors(local_boids)
        avoid_v = self.__get_obstacle_avoidance_vector(local_obstacles)

        self.__calculate_move(delta_time, (noise_v*0.5+seperation_v*2+alignment_v*5+cohesion_v*0.4+avoid_v*7)/15)