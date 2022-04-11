import pygame as pg
from src.controller import EventDispatcher as Ed
from src.events import Tick

class TickController:
    """ Has the iteration of the game that
        runs at 60 frames per second
    """
    
    def __init__(self):
        self.fps = 60
        self.clock = pg.time.Clock()
        

    def run(self):
        while True:
            Ed.post(Tick())
            self.clock.tick(60)