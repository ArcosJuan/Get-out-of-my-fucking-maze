from src.events import EndScene
from src.events import Tick
from src.events import ArrowKey
from src.view.scenes import Scene
from src.controller.event_dispatcher import EventDispatcher as Ed


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Ed.add(Tick, Scene.window.update)
        Ed.add(Tick, self.update)
        Ed.add(ArrowKey, self.__exit)


    def update(self, event):
        pass


    def __exit(self, event):
        Ed.post(EndScene(self.__class__))