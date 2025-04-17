import pygame as pg

from src import *

if __name__ == "__main__":
    pg.init()
    pg_inter = PGInterface()
    new_sim = Sim(pg_inter)
    new_sim.run()
    pg.quit()
    quit()