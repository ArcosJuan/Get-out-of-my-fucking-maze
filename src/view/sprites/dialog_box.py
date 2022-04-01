import pygame as pg
from src.references.images import DIALOG
from src.view.window import Window


class DialogBoxSprite:
    def __init__(self, min_size = 20, max_size = 38, margins = (10, 10)):
        """ Creates the dialog box image and act as the
            mediator to the dialog box image.
        """

        # Left, right and bottom margins (NOT top margins).
        # The horizontal margins may vary according 
        # to the proportions of the box so it's more like the 
        # min size of horizontal margins :).
        self.box_pieces = {"topleft": DIALOG["TOPLEFT"], "top": DIALOG["TOP"], "center": DIALOG["CENTER"]}
        self.margins = margins 

        self.validate_window_size()
        self.set_box_proportions(min_size, max_size)
        
        self.box_image = self.get_box_image()
        self.box_rect = self.get_box_rect(self.box_image)


    def set_box_proportions(self, min_size, max_size):
        """ Scale the box_pieces as much as possible 
            given a maximum and minimum size.
        """

        x = (Window().resolution[0] * 10) // 100
        y = (Window().resolution[1] * 10) // 100

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

        if Window().resolution[0] < box_min_size[0] + self.margins[0] \
            or Window().resolution[1] // 3 < box_min_size[1] + self.margins[1]:
            raise AssertionError(
            f"Current Window resolution cannot show dialogue box properly.\n"
                + "Window witdh needs to be larger or equal than"
                + f" {box_min_size[0] + self.margins[0]} and the"
                + "third part of the height larger or equal than"
                + f" {box_min_size[1] + self.margins[1]}."
            )


    def get_box_image(self):
        """ Build the dialog box image with the box_pieces 
            and according to the window size.
        """
        
        # For this to work the size of the TOPLEFT, TOP, and CENTER
        # need to be equal.

        corner_size = self.box_pieces["topleft"].get_size()

        box_size = [0,0]
        box_size[0] += ((Window().resolution[0]  - self.margins[0] * 2) // corner_size[0]) * corner_size[0]

        box_size[1] += ((Window().resolution[1] // 3 - self.margins[1]) // corner_size[1]) * corner_size[1]

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


    def get_box_rect(self, edges_image):
        """ Creates the dialog box rect and position it on the screen.
        """

        box_rect = self.box_image.get_rect()

        # Position the rect on the window.  
        box_rect = (
            (Window().resolution[0]  - self.box_image.get_size()[0]) // 2,
            Window().resolution[1] - self.box_image.get_size()[1] - self.margins[1]
            )
        
        return box_rect


    def draw(self, surface = None):
        (surface if surface else Window().surface).blit(self.box_image, self.box_rect)