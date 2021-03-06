import pygame as pg
from src.view import Window


class Sprite(pg.sprite.Sprite):
    ed = None
    min_size = 25
    actual_size = min_size

    @classmethod
    def calculate_length(cls, resolution) -> tuple[int, int]:
        """ Returns the length that the visible_cells should have,
            based on the given resolution of the window.
        """

        return (resolution[1] // cls.get_actual_size(), resolution[0] // cls.get_actual_size())


    @classmethod
    def set_size(cls, height):
        assert height >= cls.min_size, "Size must be larger than minimum."
        cls.actual_size = height


    @classmethod
    def get_min_size(cls) -> int:
        return cls.min_size


    @classmethod
    def get_actual_size(cls) -> int:
        """ Returns the current height of the surface.
        """

        return cls.actual_size


    def __init__(self):
        self.image = None
        self.rect = None


    def draw(self, surface):
        """ Receives a surface and is drawn on it.
        """

        surface.blit(self.image, self.rect)

    
    def refresh(self):
        """ Replace its Image and Rect with new ones 
            in order to update its information (e.g. size).
        """
        
        self.image = self.get_image()
        self.rect = self.image.get_rect()