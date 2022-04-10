import pygame as pg
from src.events import ArrowKey
from src.events import Click
from src.events import Interact
from src.events import PassDialog
from src.events import Interact
from src.events import Quit
from src.events import Tick
from src.events import Wheel
from src.controller.event_dispatcher import EventDispatcher as Ed


class PygameController:
    """ It receives events from pygame, translates them to an event 
        of the Event class, and post them in the EventDispatcher.
    """

    def __init__(self):
        Ed.add(Tick, self.iterate_events)
        self._mode = 0 # 0: Default, 1: Dialog, 2: PopupMenu
        self.arrow_keys_pressed = dict()

    def iterate_events(self, event):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Ed.post(Quit())

            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP: 
                    Ed.post(ArrowKey(y=1))
                elif event.key == pg.K_DOWN: 
                    Ed.post(ArrowKey(y=-1))
                elif event.key == pg.K_RIGHT: 
                    Ed.post(ArrowKey(x=1))
                elif event.key == pg.K_LEFT: 
                    Ed.post(ArrowKey(x=-1)) 
                    
                elif event.key == pg.K_RETURN: 
                    Ed.post(Interact())

            elif event.type == pg.MOUSEBUTTONUP:
                Ed.post(Click(event.pos, event.button))
            

            elif self._mode == 1: 
                if event.type == pg.KEYUP:
                    if event.key == pg.K_n:
                        Ed.post(PassDialog())

            