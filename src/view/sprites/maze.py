import pygame as pg
from src.view.sprites import Sprite
from src.references.images import MAZE

class MazeSprite(Sprite):

    def __init__(self):
        self.sprite = MAZE
        self.image = self.sprite
        self.rect = self.image.get_rect()

    def get_image(self): return self.image


    def get_rect(self): return self.rect


    def update_size(self):
        """ Scales the image to the given size.
        """

        height = MazeSprite.get_actual_size()

        surface = self.sprite
        self.image = pg.transform.scale(surface,(height,height))
        