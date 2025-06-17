import pygame as pg
from src.settings import *
from src.models import *

pg.init()

class PGInterface:
    def __init__ (self) -> None:
        screen_info = pg.display.Info()
        self.SCREEN_W, self.SCREEN_H = screen_info.current_w, screen_info.current_h
        self.__screen = pg.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        self.__clock = pg.time.Clock()
        self.__delta_time = 1
        self.__events = pg.event.get()
        self.__keydowns = []

        self.__font = pg.font.SysFont("Consolas", int(20))

        self.num_boids = 0
        self.num_obstacles = 0

        pg.display.set_caption(f"Flocking Simulation")

    def update(self, num_boids:int, num_obstacles:int) -> None:
        self.__events = pg.event.get()
        self.__delta_time = self.__clock.tick(FPS)
        self.__keydowns = [event.key for event in self.__events if event.type == pg.KEYDOWN]
        
        self.num_boids = num_boids
        self.num_obstacles = num_obstacles

    def get_mouse_pos(self) -> None:
        return pg.mouse.get_pos()

    def get_random_screen_position(self) -> tuple[int, int]:
        return (random.randint(0, self.SCREEN_W), random.randint(0, self.SCREEN_H))

    def get_delta_time(self) -> float:
        return self.__delta_time
    
    def check_add_obstacle(self) -> bool:
        return 1 in self.get_mousedowns()
    
    def check_add_boid(self) -> bool:
        return 3 in self.get_mousedowns()
    
    def check_increment_target_boid_index(self) -> bool:
        return pg.K_TAB in self.__keydowns
    
    def get_mousedowns(self) -> list:
        return [event.button for event in self.__events if event.type == pg.MOUSEBUTTONDOWN]

    def clear_screen(self) -> None:
        self.__screen.fill("BLACK")

    def draw_obstacle(self, obstacle:Obstacle) -> None:
        pg.draw.circle(self.__screen, "RED", obstacle.pos, obstacle.radius)

    def draw_boid_details(self, boid:Boid) -> None:
        pg.draw.circle(self.__screen, "#999999", boid.pos, BOID_LOCAL/2)

    def draw_boid(self, boid:Boid) -> None:
        pg.draw.line(self.__screen, boid.colour, boid.pos, boid.heading_line)
        pg.draw.polygon(self.__screen, boid.colour, boid.draw_points, 3)

    def display_boid_info(self, boid:Boid) -> None:
        display_text = f"Boid pos: ({round(boid.x, 2)}, {round(boid.y, 2)})  Boid heading: {round(boid.heading, 2)}"
        display_info = self.__font.render(display_text, False, "RED", "BLACK")
        self.__screen.blit(display_info, (0, self.SCREEN_H-display_info.get_height()))

    def load_screen(self) -> None:
        display_text = f"Boids: {self.num_boids}  Obstacles: {self.num_obstacles}  TargetFPS: {FPS}  FPS: {round(self.__clock.get_fps(), 2)}"
        display_info = self.__font.render(display_text, False, "GREEN", "BLACK")
        self.__screen.blit(display_info, (0, 0))
        pg.display.flip()

    def check_quit(self) -> bool:
        event_types = [i.type for i in self.__events]
        return pg.QUIT in event_types or pg.K_ESCAPE in self.__keydowns