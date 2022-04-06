import pygame as pg
from src.events import ArrowKey
from src.events import Click
from src.events import ChangeDialogMode
from src.events import PassDialog
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
        Ed.add(ChangeDialogMode, self.change_dialog_mode)
        self.dialog_mode = False
        self.arrow_keys_pressed = dict()

    def iterate_events(self, event):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Ed.post(Quit())

            if not self.dialog_mode:
                if event.type == pg.KEYUP:
                    if event.key in self.arrow_keys_pressed:
                        self.arrow_keys_pressed.pop(event.key)

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP: 
                        self.arrow_keys_pressed[event.key] = ArrowKey(y=1)
                    if event.key == pg.K_DOWN: 
                        self.arrow_keys_pressed[event.key] = ArrowKey(y=-1)
                    if event.key == pg.K_RIGHT: 
                        self.arrow_keys_pressed[event.key] = ArrowKey(x=1)
                    if event.key == pg.K_LEFT: 
                        self.arrow_keys_pressed[event.key] = ArrowKey(x=-1)
                    

                elif event.type == pg.MOUSEBUTTONUP:
                    Ed.post(Click(event.pos, event.button))
                
            else: 
                if event.type == pg.KEYUP:
                    if event.key == pg.K_n:
                        Ed.post(PassDialog())


                
        if self.arrow_keys_pressed: 
            [Ed.post(event) for event in self.arrow_keys_pressed.values()]

    
    def change_dialog_mode(self, event):
        self.dialog_mode = not self.dialog_mode
