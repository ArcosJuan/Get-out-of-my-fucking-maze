import pygame as pg
from src.events import Tick
from src.controller.event_dispatcher import EventDispatcher as Ed

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