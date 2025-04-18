from src.models.vector import *

class Obstacle:
    def __init__ (self, radius:int|float, posv:Vector) -> None:
        """
        Class representing a circular obstacle

        :param int|float radius: radius of circular obstacle
        :param Vector posv: position vector of obstacle
        """
        self.x, self.y = posv.i, posv.j
        self.pos = (self.x, self.y)
        self.posv = posv
        self.radius = radius