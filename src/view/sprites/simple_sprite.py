import pygame as pg
from src.view.window import Window

class SimpleSprite(pg.sprite.Sprite):
    def __init__(self, image, height=-1, window_percentage=-1, min_height=(None, None), max_height=(None, None)):
        super().__init__()
        
        self.image = self._size_image(image, height, window_percentage, min_height, max_height)
        self._rect = self.image.get_rect()

        
    def _size_image(self, image, height=-1, window_percentage=-1, min_height=None, max_height=None):
        assert (
            height != -1 and window_percentage == -1 
            or height == -1 and window_percentage != -1
            ), "Please indicate just one of the measure arguments."

        if window_percentage != -1:
            x = (Window().resolution[0] * window_percentage) // 100
            y = (Window().resolution[1] * window_percentage) // 100

            if x < y:
                scale = (x, image.get_size()[1] - abs(x - image.get_size()[0]))
            else:
                scale = (image.get_size()[0] - abs(y - image.get_size()[1]), y)
            
            if scale[1] < min_height: 
                scale = (
                    image.get_size()[0] - abs(min_height - image.get_size()[1]),
                    min_height
                    ) # Do not scale.

            if scale[1] > max_height:
                scale = (
                    image.get_size()[0] - abs(max_height - image.get_size()[1]),
                    max_height
                    ) # Just be the max size.

            return pg.transform.scale(image, (scale[0], scale[1]))

        elif height !=-1:
            width =  image.get_size()[0] + abs(image.get_size()[1] - height) 
            return pg.transform.scale(image, (height, width))


    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, rect): self._rect = rect
    

    def draw(self, surface = None):
        (surface if surface else Window().surface).blit(self.image, self.rect)
