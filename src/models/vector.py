import math

class Vector:
    pass

class Vector:
    def __init__ (self, i:int|float, j:int|float) -> None:
        if type(i) not in (int, float) or type(j) not in (int, float):
            raise TypeError(f"cannot create Vector with types {type(i)} and {type(j)}")
        self.i, self.j = i, j

    @staticmethod
    def from_tuple(components:tuple[int|float, int|float]) -> Vector:
        return Vector(components[0], components[1])
    
    @staticmethod
    def from_polar(argument_radians:int|float, magnitude:int|float) -> Vector:
        return Vector(math.cos(argument_radians)*magnitude, math.sin(argument_radians)*magnitude)

    @property
    def tup(self) -> tuple:
        return (self.i, self.j)

    @property
    def heading(self) -> int|float:
        """
        Returns unit circle heading in radians
        """
        return math.atan2(self.j, self.i)

    @property
    def magnitude(self) -> int|float:
        return math.sqrt(self.i**2 + self.j**2)
    
    @property
    def unit(self) -> Vector:
        if self.magnitude == 0:
            return self
        return self/self.magnitude
    
    def dot_product(self, vect2:Vector) -> int|float:
        if type(vect2) != Vector:
            raise TypeError(f"cannot calculate dot product with type {vect2}")
        return self.__mul__(vect2)
    
    def limit(self, magnitude) -> Vector:
        if self.magnitude < magnitude:
            return self
        
        return self.unit*magnitude
    
    # Equality
    
    def __eq__ (self, vect2:Vector) -> bool:
        if type(vect2) != Vector:
            return NotImplemented
        
        return self.i == vect2.i and self.j == vect2.j
    
    def __ne__ (self, vect2:Vector) -> bool:
        return not self.__eq__(vect2)
    
    # SIGNS

    def __neg__ (self) -> Vector:
        return Vector(-self.i, -self.j)
    
    def __pos__ (self) -> Vector:
        return self
    
    def __abs__ (self) -> Vector:
        return Vector(abs(self.i), abs(self.j))
    
    # OPERATIONS
    
    def __add__ (self, vect2: Vector) -> Vector:
        if type(vect2) not in (int, float, Vector):
            return NotImplemented
        
        if type(vect2) in (int, float):
            return Vector(self.i+vect2, self.j+vect2)
        
        return Vector(self.i+vect2.i, self.j+vect2.j)
    
    def __radd__ (self, vect2:Vector) -> Vector:
        return self.__add__(vect2)
    
    def __sub__ (self, vect2:Vector) -> Vector:
        return self.__add__(-vect2)
    
    def __rsub__ (self, vect2:Vector) -> Vector:
        return (-self).__add__(vect2)
    
    def __mul__ (self, vect2:int|float|Vector) -> int|float|Vector:
        if type(vect2) not in (int, float, Vector):
            return NotImplemented
        
        if type(vect2) in (int, float):
            return Vector(self.i*vect2, self.j*vect2)
        
        return self.i*vect2.i + self.j*vect2.j
    
    def __rmul__ (self, vect2:int|float|Vector) -> int|float|Vector:
        return self.__mul__(vect2)
    
    def __truediv__ (self, scalar:int|float) -> Vector:
        if type(scalar) not in (int, float):
            return NotImplemented
        if scalar == 0:
            raise ZeroDivisionError("cannot divide vector by 0")
        return self.__mul__(scalar**-1)
    
    def __rtruediv__ (self, scalar:int|float) -> Vector:
        if type(scalar) not in (int, float):
            return NotImplemented
        return Vector(0 if self.i == 0 else scalar/self.i, 0 if self.j == 0 else scalar/self.j)
    
    def __floordiv__ (self, vect2:Vector) -> Vector:
        return int(self.__mul__(vect2**-1))
    
    # CONVERSIONS
    
    def __repr__ (self) -> str:
        return f"<{self.i}, {self.j}>"