import pygame as pg
from lib.singleton import Singleton


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
        
        self.resolution = (960, 540) # Current resolution.
        self.background = (0,0,0)


    @property
    def surface(self): 
        return self._surface


    @surface.setter
    def surface(self, new_surface):
        self._surface = new_surface


    @property
    def resolution(self) -> tuple[int,int]:
        return self._resolution


    @resolution.setter
    def resolution(self, new_resolution, flags=0):
        try:
            assert new_resolution <= self._display_size, \
                "The resolution is too large!"

            self._resolution = new_resolution

        except AttributeError:
            self._resolution = new_resolution

        self.surface = pg.display.set_mode(self.resolution, flags)        



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
