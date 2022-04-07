import pygame as pg
from src.references.fonts import FONT_ADDRESS
from src.view.window import Window


class TextBoxSprite:
    @staticmethod
    def get_font(height): return pg.font.Font(FONT_ADDRESS, int(height))


    def __init__(self, text, height, color=(255,0,255)):
        self.image = pg.font.Font(FONT_ADDRESS, height).render(text, True, color)
        self.rect = self.image.get_rect()

    def get_rect(self): return self.rect

    def draw(self, surface = None):
        (surface if surface else Window().surface).blit(self.image, self.rect)        