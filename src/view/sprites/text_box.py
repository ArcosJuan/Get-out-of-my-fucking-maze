import pygame as pg
from src.references.fonts import FONT_ADDRESS
from src.view.window import Window


class TextBoxSprite:
    _min_height = 20
    _height = _min_height
    _font = pg.font.Font(FONT_ADDRESS, _height)

    @classmethod
    def set_font_height(cls, height):
        cls._height = int(height)
        cls._font = pg.font.Font(FONT_ADDRESS, cls._height)

    @classmethod
    def get_font_height(cls): return cls._height


    @classmethod
    def get_font(cls): return cls._font


    def __init__(self, text, color=(255,0,255)):
        self.image = self._font.render(text, True, color)
        self.rect = self.image.get_rect()

    def get_rect(self): return self.rect

    def draw(self, surface = None):
        (surface if surface else Window().surface).blit(self.image, self.rect)        