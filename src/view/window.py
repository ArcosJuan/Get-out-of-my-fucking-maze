import pygame as pg
from lib.singleton import Singleton
from src.controller import EventDispatcher as Ed
from src.events import UpdateResolution


class Window(metaclass=Singleton):
    """ Implements all that concerns to the pygame class diplay
        and a backgroun managment
    """

    def __init__(self):
        pg.display.set_caption('Get out of my fucking maze')

        self._display_size = (
            pg.display.Info().current_w,
            pg.display.Info().current_h
        ) # Obtains the resolution of the screen.

        self.set_resolution((0,0)) # Intial resolution.
        self.background = (0,0,0)


    def get_display_size(self): return self._display_size

    @property
    def surface(self): 
        return self._surface


    @surface.setter
    def surface(self, new_surface):
        self._surface = new_surface


    def get_resolution(self) -> tuple[int,int]:
        return self.resolution


    def set_resolution(self, new_resolution, flags=0):
        try:
            assert new_resolution[0] <= self._display_size[0] \
            and new_resolution[1] <= self._display_size[1] , \
                "The resolution is too large!"

            self.resolution = new_resolution


        except AttributeError:
            self.resolution = new_resolution

        self.surface = pg.display.set_mode(self.resolution, flags)        
        Ed.post(UpdateResolution())


    def update(self, event):
        """ Update the display and draw the background.
        """

        pg.display.update()
        self.surface.blit(self.background, (0,0))



    @property
    def background(self):
        return self._background


    @background.setter
    def background(self, color=(0,0,0)):
        """ Change the color of the display background.
            
            Receives:
                color:<tuple>
        """
        try:
            background_sur = pg.Surface(self.resolution)
        except: return

        background_sur.fill(color)
        
        self._background = background_sur


    def calculate_grid(self, cell_size:int) -> tuple[int, int]:
        """ Returns the length that a grid should have,
            based on the given size of a cell.
        """

        return (self.resolution[1] // cell_size, self.resolution[0] // cell_size)
        return \
            self.resolution[1] // cell_size \
            if (self.resolution[1] // cell_size) >  (self.resolution[0] // cell_size) \
            else self.resolution[0] // cell_size
