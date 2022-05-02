from src.controller import EventDispatcher as Ed
from src.view import Window


class Scene:
    window = Window()

    @staticmethod
    def get_window():
        return Scene.window


    @classmethod
    def get_window_sur(cls):
        return Scene.window.surface


    def __init__(self):
        self.name = ''

    
    def update(self, event):
        """ Updates all the sprites it contains"""

        raise NotImplementedError()

    
    def draw(self):
        """ Draws all the sprites it contains"""

        raise NotImplementedError()