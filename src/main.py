import pygame as pg
from src.controller import TickController
from src.controller import EventDispatcher
from src.controller import PygameController
from src.events import Quit
from src.model import Logic
from src.view import SceneManager
from src.controller.event_dispatcher import EventDispatcher as Ed


class Main:
    """ Initializes the game and execute it.
    """
    
    def __init__(self):        
        
        Ed.add(Quit, self.exit)

        self.tick_controller = TickController()
        self.pygame_event_catcher = PygameController()
        self.scene_manager = SceneManager()
        self.logic = Logic()

        self.run()

    def exit(self, event):
        pg.quit()
        exit()


    def run(self):
        self.tick_controller.run()


