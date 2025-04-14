import pygame as pg

from src import *

if __name__ == "__main__":
    pg.init()
    new_sim = Sim()
    new_sim.run()
    pg.quit()
    quit()