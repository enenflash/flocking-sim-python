import math, random

from .boid import *
from .vector import *
from .boid_settings import *

class SimpleBoid(Boid):
    def __init__ (self, size:int|float, max_speed:int|float,  initial_pos:tuple|Vector, initial_heading_degrees:int|float, avoid_dist:int|float) -> None:
        """
        Simple boid that flocks with other boids https://en.wikipedia.org/wiki/Boids

        :param int|float size: maximum size of boid in a given unit (if drawing to screen then pixels)
        :param int|float max_speed: maximum speed of boid unit/ms
        :param tuple|Vector initial_pos: initial position vector of boid
        :param int|float initial_heading_degrees: initial heading of boid in degrees (will be converted to radians)
        :param int|float avoid_dist: avoid distance of boid from other boids
        """
        super().__init__(size, "#FFFFFF", max_speed, avoid_dist, initial_pos, initial_heading_degrees)

    def __get_noise_vector(self) -> Vector:
        """
        Generate random noise vector
        """
        new_heading = random.randint(-5, 5)*math.pi/180 + self.heading
        speed = random.randint(1, 10)/10
        return Vector.from_polar(new_heading, speed)
    
    def __get_boid_vectors(self, local_boids:list[tuple]) -> tuple[Vector, Vector, Vector]:
        """
        Returns seperation, alignment and cohesion vectors
        """
        sep_vectors, heading_vectors, centre_of_mass = [], [], 0
        for posv, heading in local_boids:
            distance = (posv-self.posv).magnitude
            if distance == 0:
                distance = 0.01 # prevent zero division error
            if distance <= self.avoid_dist:
                sep_vectors.append(1/(self.posv-posv))
            heading_vectors.append(Vector.from_polar(heading, 100/distance))
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
            self.heading += heading_dir*0.1 #0.3
        self.__move(vect.magnitude, delta_time)
    
    def update(self, delta_time:int|float, local_boids:list[tuple], local_obstacles:list[Vector]) -> None:
        noise_v = self.__get_noise_vector()
        if len(local_boids) == 0:
            self.__calculate_move(delta_time, noise_v)
            return

        seperation_v, alignment_v, cohesion_v = self.__get_boid_vectors(local_boids)
        avoid_v = self.__get_obstacle_avoidance_vector(local_obstacles)

        # 0.5, 2, 3, 0.4, 7
        self.__calculate_move(delta_time, (noise_v*NOISE_SCALAR+seperation_v*SEPARATION_SCALAR+alignment_v*ALIGNMENT_SCALAR+cohesion_v*COHESION_SCALAR+avoid_v*AVOIDENCE_SCALAR)/15)