from .vector import *

class Obstacle:
    def __init__ (self, radius:int|float, posv:Vector) -> None:
        self.x, self.y = posv.i, posv.j
        self.pos = (self.x, self.y)
        self.posv = posv
        self.radius = radius