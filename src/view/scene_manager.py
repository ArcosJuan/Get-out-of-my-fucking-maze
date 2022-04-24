from src.controller import EventDispatcher as Ed
from src.events import EndScene
from src.events import GameStart
from src.view import Window
from src.view.scenes import Game
from src.view.scenes import MainMenu
from src.view.scenes import Scene
from src.view.sprites import Sprite


class SceneManager:
    def __init__(self):
        Ed.add(EndScene, self.end_scene)

        self.scenes = {
            'menu' : MainMenu,
            'game' : Game
        }
        self.current_scene = None

        self._set_current_scene(self.scenes['menu'])


    def end_scene(self, event):
        scene = event.get_scene()
        if scene == self.scenes['menu']:
            self._set_current_scene(self.scenes['game'])
            Ed.post(GameStart(min_size=Sprite.calculate_length(resolution=Window().get_resolution())))


    def _set_current_scene(self, scene):
        """ Change the current scene for another
        
            Receives:
                scene:<scene>
        """
        
        self.current_scene = scene()

