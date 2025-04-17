from .settings import *
from .vector import *
from .obstacle import *
from .boid import *

class Mouse:
    def __init__ (self) -> None:
        self.x, self.y = 0, 0
        self.radius = 20
    
    @property
    def pos(self) -> tuple:
        return (self.x, self.y)

    @pos.setter
    def pos(self, mouse_pos:tuple) -> None:
        self.x, self.y = mouse_pos
    
    @property
    def posv(self) -> Vector:
        return Vector(self.x, self.y)

class Sim:
    def __init__ (self, output_interface:object):
        self.running = True
        
        self.output_interface = output_interface

        self.mouse = Mouse()

        self.boids = [Boid(BOID_SIZE, BOID_MAX_SPEED, Vector.from_tuple(self.output_interface.get_random_screen_position()), random.randint(0, 359)) for _ in range(NUM_BOIDS)]
        self.boid_local_dict = {}

        self.obstacles = []
    
    def __get_local_boids(self, boid_index:int) -> list[tuple[Vector, int|float]]:
        """
        Returns a list of local boid positions and headings (pos, heading)
        """
        local_boids = []
        for i in range(NUM_BOIDS):
            if i == boid_index:
                continue
            
            access_tuple = (i, boid_index) if i < boid_index else (boid_index, i)
            if access_tuple not in self.boid_local_dict:
                self.boid_local_dict[access_tuple] = ((self.boids[i].posv-self.boids[boid_index].posv).magnitude < BOID_LOCAL)
            if self.boid_local_dict[access_tuple]:
                local_boids.append((self.boids[i].posv, self.boids[i].heading))

        return local_boids
    
    def __get_local_obstacles(self, boid_index:int) -> list[tuple[tuple, int]]:
        return [obstacle.posv for obstacle in self.obstacles+[self.mouse] if (obstacle.posv-self.boids[boid_index].posv).magnitude <= OBSTACLE_AVOID_DIST + obstacle.radius]
    
    def __keep_boid_onscreen(self, boid_pos:tuple) -> tuple:
        """
        Modify boid position such that it is always onscreen
        """
        new_x, new_y = boid_pos[0], boid_pos[1]

        if boid_pos[0] < 0: new_x = self.output_interface.SCREEN_W
        elif boid_pos[0] > self.output_interface.SCREEN_W: new_x = 0

        if boid_pos[1] < 0: new_y = self.output_interface.SCREEN_H
        elif boid_pos[1] > self.output_interface.SCREEN_H: new_y = 0

        return new_x, new_y
    
    def add_obstacle(self, radius:int|float, position:tuple) -> None:
        self.obstacles.append(Obstacle(radius, Vector(position[0], position[1])))
        print("> Placed Obstacle")
        print("> Total Obstacles:", len(self.obstacles))

    def add_boid(self, size:int|float, max_speed:int|float, position:tuple[int|float, int|float], heading:int|float=0) -> None:
        self.boids.append(Boid(size, max_speed, Vector(position[0], position[1]), heading))
        print("> Added Boid")
        print("> Total Boids:", len(self.boids))

    def update(self) -> None:
        self.output_interface.update(len(self.boids), len(self.obstacles))

        mousedowns = self.output_interface.get_mousedowns()

        self.mouse.pos = self.output_interface.get_mouse_pos()

        if 1 in mousedowns:
            self.add_obstacle(15, self.mouse.pos)
        if 3 in mousedowns:
            self.add_boid(BOID_SIZE, BOID_MAX_SPEED, self.mouse.pos, random.randint(0, 359))

        self.output_interface.clear_screen()

        self.boid_local_dict = {}

        for obstacle in self.obstacles:
            self.output_interface.draw_obstacle(obstacle)

        for boid_index, boid in enumerate(self.boids):
            # update
            boid.update(self.output_interface.get_delta_time(), self.__get_local_boids(boid_index), self.__get_local_obstacles(boid_index))
            boid.pos = self.__keep_boid_onscreen(boid.pos)
            # draw
            if boid_index == 0:
                self.output_interface.draw_boid_details(boid)
            self.output_interface.draw_boid(boid)
        
        self.output_interface.load_screen()

    def run(self) -> None:
        while self.running:
            self.running = not self.output_interface.check_quit()
            self.update()