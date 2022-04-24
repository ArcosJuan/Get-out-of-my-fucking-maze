import pygame as pg
from lib.weak_bound_method import WeakBoundMethod as Wbm
from src.controller import EventDispatcher as Ed
from src.events import ArrowKey
from src.events import Click
from src.events import Event
from src.events import Interact
from src.events import Tick
from src.events import UpdateResolution
from src.references.images import DIALOG
from src.view.sprites import TextBoxSprite
from src.view.window import Window



class PopupMenu:
    box_pieces = {"topleft": DIALOG["TOPLEFT"], "top": DIALOG["TOP"], "center": DIALOG["CENTER"]}
    
    def __init__(self, options, box_relative_pos=(1/2,1/2), min_size = 20, max_size = 30, txt_to_pct=5, text_default_color=(255,255,255), text_active_color = (255,0,0), initial_index=0):
        Ed.add(Interact, self.interact)
        Ed.add(Tick, self.draw)
        Ed.add(UpdateResolution, self.update_size)
        
        Ed.add_exclusive_listener(ArrowKey, self.move_option)
        Ed.add_exclusive_listener(Interact, self.interact)

        # TEXT INITIALIZATION:
        self.txt_to_pct = txt_to_pct # It is the percentage of the screen that the text occupies.
        self.options = options # list[tuple(string, Event/WeakBoundMethod)]
        
        # Text properties:
        self.text_p = {
            'height': self._get_text_height(),
            'dcolor': text_default_color,
            'acolor': text_active_color
        }
        
        # BOX INITIALIZATION:
        self.box_relative_pos = box_relative_pos
        self.max_size, self.min_size = max_size, min_size
        self.validate_window_size()
        
        self._box_sprite_init()
        
        self.option_sprites = self._get_option_sprites()
        self._set_index(initial_index)


    def _set_index(self, option_index):
        self.index = option_index
        for option_sprite in self.option_sprites:
            option_sprite.change_color(self.text_p["dcolor"])

        self.option_sprites[option_index].change_color(self.text_p["acolor"])


    def _get_text_height(self):
        return int(
                (
                    self.txt_to_pct*(Window().get_resolution()[0]
                    *Window().get_resolution()[1])/100
                )**(1/2)
            )


    def _box_sprite_init(self):
        self.set_box_proportions(self.min_size, self.max_size)
        self.box_image = self._create_box_image()
        self.box_rect = self.box_image.get_rect()
        self._set_relative_position()


    def _set_relative_position(self):
        self.box_rect.center = (
            Window().get_resolution()[0] * self.box_relative_pos[0],
            Window().get_resolution()[1] * self.box_relative_pos[1]
        )


    def update_size(self, event):
        self.text_p["height"] = self._get_text_height()

        self._box_sprite_init()
        
        self.option_sprites = self._get_option_sprites()
        self.option_sprites[self.index].change_color(self.text_p["acolor"])


    def set_box_proportions(self, min_size, max_size):
        """ Scale the box_pieces as much as possible 
            given a maximum and minimum size.
        """

        x = (Window().get_resolution()[0] * 10) // 100
        y = (Window().get_resolution()[1] * 10) // 100

        scale = x if x < y else y 

        if scale < min_size: scale = min_size # Do not scale.
        if scale > max_size: scale = max_size # Just be the max size.

        self.box_pieces["topleft"] = pg.transform.scale(DIALOG["TOPLEFT"], (scale, scale))
        self.box_pieces["top"] = pg.transform.scale(DIALOG["TOP"], (scale, scale))
        self.box_pieces["center"] = pg.transform.scale(DIALOG["CENTER"], (scale, scale))


    def validate_window_size(self):
        """ Validates that the Window meets the conditions
            to show the dialogue box properly.
        """

        box_min_size = list(self.box_pieces["topleft"].get_size())

        box_min_size[0] += self.box_pieces["topleft"].get_size()[0]
        box_min_size[1] += self.box_pieces["topleft"].get_size()[1]

        box_min_size[0] += self.box_pieces["top"].get_size()[0] * 3
        box_min_size[1] += self.box_pieces["top"].get_size()[1] * 2

        if Window().get_resolution()[0] < box_min_size[0] \
            or Window().get_resolution()[1] < box_min_size[1]:
            raise AssertionError("Current Window resolution cannot show dialogue box properly")


    def get_box_size(self):
        box_size = [None, None]

        box_size[0] = \
            round(round(TextBoxSprite.get_font(self.text_p["height"]).size(max([option[0] for option in self.options], key=len))[0] \
            / self.box_pieces["topleft"].get_size()[0]) \
            * self.box_pieces["topleft"].get_size()[0]
        )
        box_size[1] = \
            round(self.text_p["height"] \
            * len(self.options) \
            / self.box_pieces["topleft"].get_size()[1]) \
            * self.box_pieces["topleft"].get_size()[1]

        return box_size

    
    def _create_box_image(self):
        """ Build the dialog box image with the box_pieces 
            and according to the window size.
        """
        
        # For this to work the size of the TOPLEFT, TOP, and CENTER
        # need to be equal.

        corner_size = self.box_pieces["topleft"].get_size()

        box_size = self.get_box_size()
        box_size = (box_size[0] + corner_size[0], box_size[1] + corner_size[1])
        box_image = pg.Surface(box_size)

        # Blit TOPLEFT
        box_image.blit(self.box_pieces["topleft"], (0,0))
        # Blit TOPRIGHT
        box_image.blit(pg.transform.flip(self.box_pieces["topleft"], True, False),
                        (box_size[0] - corner_size[0], 0))
        # Blit BOTTOMLEFT
        box_image.blit(pg.transform.flip(self.box_pieces["topleft"], False, True),
                        (0, box_size[1] - corner_size[1]))
        # Blit BOTTOMRIGHT
        box_image.blit(pg.transform.flip(self.box_pieces["topleft"], True, True),
                        (box_size[0] - corner_size[0], 
                         box_size[1] - corner_size[1]))

        # Blit TOP
        for x in range(corner_size[0], box_size[0] - corner_size[0], corner_size[0]):
            box_image.blit(self.box_pieces["top"], (x, 0))
        # Blit BOTTOM
        for x in range(corner_size[0], box_size[0] - corner_size[0], corner_size[0]):
            box_image.blit(
                pg.transform.flip(self.box_pieces["top"], False, True), 
                (x, box_size[1] - corner_size[1])
                )
        # Blit LEFT
        for y in range(corner_size[1], box_size[1] - corner_size[1], corner_size[1]):
            box_image.blit(pg.transform.rotate(self.box_pieces["top"], 90), (0, y))
        # Blit RIGHT
        for y in range(corner_size[1], box_size[1] - corner_size[1], corner_size[1]):
            box_image.blit(pg.transform.rotate(self.box_pieces["top"], -90), (box_size[0] - corner_size[0], y))

        # Blit CENTER
        for x in range(corner_size[0], box_size[0] - corner_size[0], corner_size[0]):
            for y in range(corner_size[1], box_size[1] - corner_size[1], corner_size[1]):
                box_image.blit(self.box_pieces["center"], (x,y))

        return box_image


    def draw(self, event, surface = None):
        (surface if surface else Window().surface).blit(self.box_image, self.box_rect)    
        
        for option_sprite in self.option_sprites:
            option_sprite.draw()


    def move_option(self, arrow_event):
        if arrow_event.get_y() == 1:
            if self.index > 0:
                self._set_index(self.index - 1)
            else: self._set_index(len(self.options) - 1)
        elif arrow_event.get_y() == -1:
            if self.index < len(self.options) - 1:
                self._set_index(self.index + 1)
            else: self._set_index(0)


    def interact(self, interact_event):
        if isinstance(self.options[self.index][1], Wbm):
            self.options[self.index][1]()
        elif isinstance(self.options[self.index][1], Event):
            Ed.post(self.options[self.index][1])
    

    def __del__(self):
        Ed.remove_exclusive_listener(ArrowKey, self.move_option)
        Ed.remove_exclusive_listener(Interact, self.interact)


    def _get_option_sprites(self):
        """ Set the options that will be shown.
        """

        option_sprites = []

        for index in range(1, len(self.options) + 1):
            option_sprite = TextBoxSprite(self.options[index - 1][0], self.text_p["height"], self.text_p["dcolor"])
            option_sprite.get_rect().centerx = self.box_rect.centerx
            divition = round(self.box_rect.height / len(self.options))
            
            if index == 1:
                option_sprite.get_rect().centery = self.box_rect.top + (divition/2)
            
            else:
                option_sprite.get_rect().centery = option_sprites[index - 2].get_rect().centery + divition
            
            option_sprites.append(option_sprite)

        return option_sprites