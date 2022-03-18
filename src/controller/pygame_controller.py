import pygame as pg
from src.events import ArrowKey
from src.events import Click
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
        self.arrow_keys_pressed = dict()

    def iterate_events(self, event):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                Ed.post(Quit())

            elif event.type == pg.KEYUP:
                if event.key in self.arrow_keys_pressed:
                    self.arrow_keys_pressed.pop(event.key)
                if event.key == pg.K_n:
                    Ed.post(ShiftEnded())

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

            elif event.type == pg.MOUSEWHEEL:
                Ed.post(Wheel(event.y))
                

        if self.arrow_keys_pressed: 
            [Ed.post(event) for event in self.arrow_keys_pressed.values()]