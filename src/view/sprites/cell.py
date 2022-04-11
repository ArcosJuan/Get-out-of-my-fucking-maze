import pygame as pg
from src.controller import EventDispatcher as Ed
from src.events import CellPressed
from src.events import Tick
from src.references import Biome
from src.references import Tile
from src.references.images import CELL
from src.view.sprites.sprite import Sprite


class CellSprite(Sprite):
    native_tiles = {biome:CELL[biome] for biome in Biome}
    native_tiles |= {tile:CELL[tile] for tile in Tile}
    tiles = native_tiles.copy()
    
    # native_tiles keep the original size in order to 
    # not to lose image quality.


    @classmethod
    def update_size(cls):
        """ Scales all the images to the given size.
        """

        height = cls.get_actual_size()

        for tile in cls.native_tiles:
            surface = cls.native_tiles[tile]
            new_surface = pg.transform.scale(surface,(height,height))
            cls.tiles[tile]= new_surface


    @classmethod
    def get_tile(cls, tile) -> list:
        """ Returns the list of tiles (Surfaces).
        """

        return cls.tiles[tile]


    def __init__(self, position, tile):
        self.tile = tile
        self.image = CellSprite.get_tile(tile)
        self.rect = self.image.get_rect()

        Ed.add(Tick, self.routine_update)

        # The cell is only interested in knowing its position
        # to be able to launch it as data for an event.
        self.position = position
        self.update_size()


    def draw(self, surface):
        """ Receives a surface and is drawn on it.
        """

        surface.blit(self.image, self.rect)


    def routine_update(self, event):
        """ Updates the cell state on every Tick.
        """

        pass


    def handle_collisions(self, event):
        """ Checks if the mouse has clicked on it and reacts.
        """

        if self.rect.collidepoint(event.get_pos()) and event.get_button() == 1:
            Ed.post(CellPressed(self.position))
            print(self.position)


    def refresh(self):
        """ Replace its Image and Rect with new ones 
            in order to update its information (e.g. size).
        """
        
        self.image = self.get_tile(self.tile)
        self.rect = self.image.get_rect()

    
    def get_position(self): return self.position


    def __hash__(self):
        return hash(self.position)