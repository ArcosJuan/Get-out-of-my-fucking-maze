import pygame as pg
import os
from src.references import Biome
from src.references import Tile

def load_innocent_sprites():
    with os.scandir('assets/graphics/entities/charactors') as files:
        sprites = [file for file in files if file.is_file()]
        if not sprites: raise AssertionError('error loading sprites')
        innocents = dict()
        for sprite in sprites:
            name = sprite.name.replace(".png", "")
            innocents[name] = pg.image.load(sprite.path).convert_alpha()
        return innocents


PLAYER =  pg.image.load('assets/graphics/entities/player.png').convert_alpha()
INNOCENTS =  load_innocent_sprites()
LADDER =  pg.image.load('assets/graphics/entities/ladder.png').convert_alpha()
WALL =  pg.image.load('assets/graphics/entities/wall.png').convert_alpha()

CELL = {
    Biome.DESERT:pg.image.load('assets/graphics/biomes/desert.png').convert(),
    Biome.FLOWERED:pg.image.load('assets/graphics/biomes/flowered.png').convert(),
    Biome.GRASS:pg.image.load('assets/graphics/biomes/grass.png').convert(),
    Biome.TUNDRA:pg.image.load('assets/graphics/biomes/tundra.png').convert(),
    Biome.SAVANNA:pg.image.load('assets/graphics/biomes/savanna.png').convert(),
    Biome.SNOW:pg.image.load('assets/graphics/biomes/snow.png').convert(),
    Biome.OCEAN:pg.image.load('assets/graphics/biomes/ocean.png').convert(),
    Tile.EMPTY:pg.image.load('assets/graphics/tiles/empty.png').convert(),
    Tile.STONE:pg.image.load('assets/graphics/tiles/stone.png').convert(),
}

_dialog_images = pg.image.load('assets/graphics/dialog/dialog_tiles.png').convert()

DIALOG = {
    "TOPLEFT":pg.transform.chop(_dialog_images, (20,20,40,20)),
    "TOP":pg.transform.chop(pg.transform.chop(_dialog_images, (0,20,20,20)), (20,20,20,20)),
    "CENTER":pg.transform.chop(_dialog_images, (0,20,40,20)),
}

NEXT_DIALOG = pg.image.load('assets/graphics/dialog/next_dialog.png').convert_alpha()

MAZE = pg.image.load('assets/graphics/entities/maze.png').convert_alpha()
