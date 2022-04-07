import colorsys
import pygame as pg
import random
from src.references import images as img
from src.references import Layer
from src.model import Maze
from src.model import Player
from src.view.sprites import MazeSprite
from src.view.sprites import PlayerSprite



class SpriteFactory:
    """ Translates entities of the model to Sprites for use in the view.
    """

    sprite_equivalences = {
        Maze: (Layer.ENTITY, MazeSprite),
        Player: (Layer.CHARACTOR, PlayerSprite),
    }

    hue = random.random()

    @classmethod
    def get_sprite(cls, entity):
        """ Creates and returns a Sprite instance that correspond
            with the class of the object passed by value
        """

        equivalence = cls.sprite_equivalences[entity.__class__]

        return equivalence[0], equivalence[1]()


    @classmethod
    def translate_entity_dict(cls, entities: dict):
        entity_sprites = dict()

        for position in entities:
            for entity in entities[position]:
                layer, sprite = cls.get_sprite(entity)
                if entity_sprites.get(position): 
                    entity_sprites[position] |= {layer: sprite}
                else: 
                    entity_sprites |= {position: {layer:sprite}}
                    

        return entity_sprites