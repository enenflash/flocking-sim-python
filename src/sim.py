from .settings import *
from .models import *

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
        
        # interface for drawing
        self.output_interface = output_interface
        self.mouse = Mouse()

        # list of boids and obstacles
        self.boids = [SimpleBoid(BOID_SIZE, BOID_MAX_SPEED, Vector.from_tuple(self.output_interface.get_random_screen_position()), random.randint(0, 359), BOID_AVOID_DIST) for _ in range(NUM_BOIDS)]
        self.obstacles = []

        # store boid distance data to prevent recalculation with every boid
        self.boid_local_dict = {}

        # display extra boid details for the boid with this index
        self.target_boid_index = 0
    
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
    
    def __get_local_obstacles(self, boid_index:int) -> list[Vector]:
        """
        Returns a list of local obstacle position vectors
        """
        return [obstacle.posv for obstacle in self.obstacles+[self.mouse] if (obstacle.posv-self.boids[boid_index].posv).magnitude <= OBSTACLE_AVOID_DIST + obstacle.radius]
    
    def __keep_boid_onscreen(self, boid:SimpleBoid) -> None:
        """
        Modify boid position such that it is always onscreen
        """
        new_x, new_y = boid.pos

        if new_x < 0: new_x = self.output_interface.SCREEN_W
        elif new_x > self.output_interface.SCREEN_W: new_x = 0

        if new_y < 0: new_y = self.output_interface.SCREEN_H
        elif new_y > self.output_interface.SCREEN_H: new_y = 0

        boid.pos = new_x, new_y
    
    def add_obstacle(self, radius:int|float, position:tuple) -> None:
        self.obstacles.append(Obstacle(radius, Vector(position[0], position[1])))
        print(" Placed Obstacle")

    def add_boid(self, size:int|float, max_speed:int|float, position:tuple[int|float, int|float], heading:int|float=0) -> None:
        self.boids.append(SimpleBoid(size, max_speed, Vector(position[0], position[1]), heading, BOID_AVOID_DIST))
        print(" Added Boid")

    def increment_target_boid_index(self) -> None:
        self.target_boid_index += 1
        if self.target_boid_index >= len(self.boids):
            self.target_boid_index = 0

    def update(self) -> None:
        self.output_interface.update(len(self.boids), len(self.obstacles))
        self.mouse.pos = self.output_interface.get_mouse_pos()

        if self.output_interface.check_add_obstacle():
            self.add_obstacle(15, self.mouse.pos)
        if self.output_interface.check_add_boid():
            self.add_boid(BOID_SIZE, BOID_MAX_SPEED, self.mouse.pos, random.randint(0, 359))
        if self.output_interface.check_increment_target_boid_index():
            self.increment_target_boid_index()

        # clear screen for drawing
        self.output_interface.clear_screen()

        self.boid_local_dict = {}

        for obstacle in self.obstacles:
            self.output_interface.draw_obstacle(obstacle)

        for boid_index, boid in enumerate(self.boids):
            # update boid
            boid.update(self.output_interface.get_delta_time(), self.__get_local_boids(boid_index), self.__get_local_obstacles(boid_index))
            self.__keep_boid_onscreen(boid)
            # draw boid
            if boid_index == self.target_boid_index:
                self.output_interface.draw_boid_details(boid)
            self.output_interface.draw_boid(boid)
        
        self.output_interface.load_screen()

    def run(self) -> None:
        while self.running:
            self.running = not self.output_interface.check_quit()
            self.update()