import pygame as pg
from src.references import Biome
from src.references import Tile


PLAYER =  pg.image.load('assets/graphics/entities/charactors/player.png').convert_alpha()

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

_dialog_images = pg.image.load('assets/graphics/dialog/dialog_tiles20x20.png').convert()

DIALOG = {
    "TOPLEFT":pg.transform.chop(_dialog_images, (20,20,40,20)),
    "TOP":pg.transform.chop(pg.transform.chop(_dialog_images, (0,20,20,20)), (20,20,20,20)),
    "CENTER":pg.transform.chop(_dialog_images, (0,20,40,20)),
}

PRESS_N = pg.image.load('assets/graphics/dialog/press_n600x600.png').convert_alpha()

MAZE = pg.image.load('assets/graphics/entities/maze.png').convert_alpha()
