import pygame as pg
import random

from .settings import *
from .vector import *
from .boid import *

pg.init()

screen_info = pg.display.Info()

SCREEN_W, SCREEN_H = screen_info.current_w, screen_info.current_h
FPS = 60

rand_posv = lambda: Vector(random.randint(0, SCREEN_W), random.randint(0, SCREEN_H))

class Obstacle:
    def __init__ (self, radius:int|float, posv:Vector) -> None:
        self.x, self.y = posv.i, posv.j
        self.pos = (self.x, self.y)
        self.posv = posv
        self.radius = radius

class Mouse:
    def __init__ (self) -> None:
        self.x, self.y = 0, 0
        self.radius = 20
    
    @property
    def pos(self) -> tuple:
        return (self.x, self.y)
    
    @property
    def posv(self) -> Vector:
        return Vector(self.x, self.y)
    
    def update(self, mouse_pos:tuple) -> None:
        self.x, self.y = mouse_pos

class Sim:
    def __init__ (self):
        self.running = True
        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))

        self.delta_time = 1
        self.clock = pg.time.Clock()
        self.events = pg.event.get()
        self.keydowns = []

        self.mouse = Mouse()

        self.boids = [Boid(BOID_SIZE, BOID_MAX_SPEED, rand_posv(), random.randint(0, 359)) for _ in range(NUM_BOIDS)]
        self.boid_local_dict = {}

        self.obstacles = []
    
    def get_local_boids(self, boid_index:int) -> list[tuple[Vector, int|float]]:
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
    
    def get_local_obstacles(self, boid_index:int) -> list[tuple[tuple, int]]:
        return [obstacle.posv for obstacle in self.obstacles+[self.mouse] if (obstacle.posv-self.boids[boid_index].posv).magnitude <= OBSTACLE_AVOID_DIST + obstacle.radius]
    
    def keep_boid_onscreen(self, boid_pos:tuple) -> tuple:
        """
        Modify boid position such that it is always onscreen
        """
        new_x, new_y = boid_pos[0], boid_pos[1]

        if boid_pos[0] < 0: new_x = SCREEN_W
        elif boid_pos[0] > SCREEN_W: new_x = 0

        if boid_pos[1] < 0: new_y = SCREEN_H
        elif boid_pos[1] > SCREEN_H: new_y = 0

        return new_x, new_y

    def update(self) -> None:
        pg.display.set_caption(f"Flocking Sim FPS: {round(self.clock.get_fps(), 2)}")
        self.delta_time = self.clock.tick(FPS)
        self.events = pg.event.get()
        self.keydowns = [event.key for event in self.events if event.type == pg.KEYDOWN]
        mousedowns = [event.button for event in self.events if event.type == pg.MOUSEBUTTONDOWN]

        self.mouse.update(pg.mouse.get_pos())

        if 1 in mousedowns:
            self.obstacles.append(Obstacle(15, Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])))
        if 2 in mousedowns:
            self.boids.append(Boid(BOID_SIZE, BOID_MAX_SPEED, pg.mouse.get_pos(), random.randint(0, 359)))

        self.screen.fill("BLACK")

        self.boid_local_dict = {}

        for obstacle in self.obstacles:
            pg.draw.circle(self.screen, "RED", obstacle.pos, obstacle.radius)

        for boid_index, boid in enumerate(self.boids):
            # update
            boid.update(self.delta_time, self.get_local_boids(boid_index), self.get_local_obstacles(boid_index))
            boid.set_pos(self.keep_boid_onscreen(boid.pos))
            # draw
            if boid_index == 0:
                pg.draw.circle(self.screen, "#999999", boid.pos, BOID_LOCAL/2)
                pg.draw.line(self.screen, "RED", boid.pos, boid.heading_line)
                pg.draw.polygon(self.screen, "RED", boid.draw_points, 3)
                continue
            pg.draw.line(self.screen, boid.colour, boid.pos, boid.heading_line)
            pg.draw.polygon(self.screen, boid.colour, boid.draw_points, 3)
        
        pg.display.flip()

    def run(self) -> None:
        while self.running:
            event_types = [i.type for i in self.events]
            if pg.QUIT in event_types or pg.K_ESCAPE in self.keydowns:
                print("[*] ANTI-GRAVITY closing . . .")
                self.running = False

            self.update()