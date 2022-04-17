import pygame as pg
from src.references.images import DIALOG
from src.view.window import Window
from src.view.sprites import TextBoxSprite


class DialogBoxSprite:
    def __init__(self, min_size = 20, max_size = 38, box_margins = (10, 10), text_height_percentage=25, text_margins_percentage=(3,10), text_color=(255,255,255), text_line_spacing=0):
        """ Creates the dialog box image and act as the
            mediator to the dialog box image.
        """
        # BOX INITIALIZATION:

        # Left, right and bottom margins (NOT top margins).
        # The horizontal margins may vary according 
        # to the proportions of the box so it's more like the 
        # min size of horizontal margins :).
        self.box_pieces = {"topleft": DIALOG["TOPLEFT"], "top": DIALOG["TOP"], "center": DIALOG["CENTER"]}
        self.box_margins = box_margins 

        self.validate_window_size()
        self.set_box_proportions(min_size, max_size)
        
        self.box_image = self._create_box_image()
        self.box_rect = self._create_box_rect(self.box_image)

        # TEXT INITIALIZATION:

        # Text properties:
        self.text_p = {
            'height':self.box_image.get_size()[1] * text_height_percentage // 100,
            'margins_percentage': text_margins_percentage,
            'color': text_color,
            'line_spacing': text_line_spacing
        }

        # Text itself:
        self.text_rows = []

        self.text_area = self._create_text_area(self.text_p['margins_percentage'])


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

        if Window().get_resolution()[0] < box_min_size[0] + self.box_margins[0] \
            or Window().get_resolution()[1] // 3 < box_min_size[1] + self.box_margins[1]:
            raise AssertionError(
            f"Current Window resolution cannot show dialogue box properly.\n"
                + "Window witdh needs to be larger or equal than"
                + f" {box_min_size[0] + self.box_margins[0]} and the"
                + "third part of the height larger or equal than"
                + f" {box_min_size[1] + self.box_margins[1]}."
            )


    def _create_box_image(self):
        """ Build the dialog box image with the box_pieces 
            and according to the window size.
        """
        
        # For this to work the size of the TOPLEFT, TOP, and CENTER
        # need to be equal.

        corner_size = self.box_pieces["topleft"].get_size()

        box_size = [0,0]
        box_size[0] += ((Window().get_resolution()[0]  - self.box_margins[0] * 2) // corner_size[0]) * corner_size[0]

        box_size[1] += ((Window().get_resolution()[1] // 3 - self.box_margins[1]) // corner_size[1]) * corner_size[1]

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


    def _create_box_rect(self, edges_image):
        """ Creates the dialog box rect and position it on the screen.
        """

        box_rect = self.box_image.get_rect()

        # Position the rect on the window.  
        box_rect.topleft = (
            (Window().get_resolution()[0]  - self.box_image.get_size()[0]) // 2,
            Window().get_resolution()[1] - self.box_image.get_size()[1] - self.box_margins[1]
            )
        
        return box_rect


    def _create_text_area(self, margin_percentage):
        """ Creates the rect where the text will be drawn.
            Recives: 
                margin_percentage<tuple(<int>,<int>)>
            
            Returns:
                text_area<pygame.Rect>
        """
        
        box_size = self.box_image.get_size()

        width = box_size[0] - box_size[0] * margin_percentage[0] / 100
        height = box_size[1] - box_size[1] * margin_percentage[1] / 100
        
        text_area = pg.Rect(0, 0, width, height)
        text_area.center = self.box_rect.center
        return text_area


    def draw(self, surface = None):
        (surface if surface else Window().surface).blit(self.box_image, self.box_rect)
        if self.text_rows: 
            for text_box in self.text_rows:
                text_box.draw()


    def set_text(self, text):
        """ Set the text that will be shown.
        """

        self.text_rows = []

        for row in range(0, len(text)):
            self.text_rows.append(TextBoxSprite(text[row], self.text_p["height"], self.text_p['color']))
            if row == 0:
                self.text_rows[0].get_rect().topleft = self.text_area.topleft
            else: 
                x = self.text_rows[row-1].get_rect().bottomleft[0]
                y = self.text_rows[row-1].get_rect().bottomleft[1] + self.text_p['line_spacing']
                self.text_rows[row].get_rect().topleft =  (x,y)


    def _cut_text_horizontally(self, text):
        """ Given a text, it is cut in such a way that each row can
            be printed inside the text_area.
            Recives: 
        """

        cut_text = []
        text_font = TextBoxSprite.get_font(self.text_p["height"])
        text_width = text_font.size(text)[0]
        if text_font.size(text)[0] > self.text_area.width:
            line_width = self.text_area.width *  100 / text_width
            line_width = int(line_width * len(text) // 100)

            while True:
                if text_font.size(text[:line_width])[0] + text_font.size('-')[0] >= self.text_area.width:
                    line_width -= 1
                else: break

            
            if self._hyphen_validation(text, line_width):
                cut_text.append(text[:line_width] + '-')
            else: cut_text.append(text[:line_width])
            
            cut_text.extend(self._cut_text_horizontally(text[line_width:].strip()))

            return cut_text  

        else: 
            return [text]
            

    def _hyphen_validation(self, text, line_width):
        """ The conditions used to know if the cut text needs
            a hyphen in the next row.
        """

        conditions = (
            text[line_width - 1] != ' '
            and text[line_width] != ' ' 
            and text[line_width - 1] != '-' 
            and text[line_width - 1] != ','
            )

        return conditions


    def _cut_text_vertically(self, text):
        """ Given a list of text rows, it cuts them into groups where
            each group can fit in the text_area.
        """

        rows = self.text_area.height // (self.text_p["height"] + self.text_p['line_spacing'])
        cut_text = []
        while text:
            group = []
            for i in range(rows):
                if len(text) != 0:
                    group.append(text.pop(0)) 

                else: break

            cut_text.append(group)
        return cut_text

    
    def adjust_text(self, text):
        """ Adjust the text to fit the text_area. If the text is too big,
            it returns groups of text where each group can fit
            in the textarea.
        """

        horizontally_adjusted_text = self._cut_text_horizontally(text)
        adjusted_text = self._cut_text_vertically(horizontally_adjusted_text)
        return adjusted_text