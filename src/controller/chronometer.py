from src.events import Tick
import pygame as pg

class Chronometer:
    def __init__(self, time, mode=1):
        # Modes = 1: Switch, 2: Shots.

        if mode == 1:
            self.mode = self._get_switch
            self.switch = True
        elif mode == 2:
            self.mode == self._get_shot
        
        self.time = time*1000
        self.time_cut = pg.time.get_ticks()

    
    def get_update(self):
        """ Depending on the mode, it will return a boolean value
            representing whether the period is complete.
        """

        return self.mode()


    def _get_switch(self):
        """ It will return a boolean switch that change its
            value each time the period completes.  
        """

        if(pg.time.get_ticks() - self.time_cut >= self.time):
            self.time_cut = pg.time.get_ticks()
            self.switch = not self.switch

        return self.switch


    def _get_shot(self):
        """ It will return True if the period is complete. 
            Else returns False.  
        """

        if(pg.time.get_ticks() - self.time_cut >= self.time):
            self.time_cut = pg.time.get_ticks()
            return True

        return False

