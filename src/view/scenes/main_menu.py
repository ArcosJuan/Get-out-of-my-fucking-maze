from src.events import EndScene
from src.events import Tick
from src.events import Click
from src.view.scenes import Scene
from src.controller.event_dispatcher import EventDispatcher as Ed
from src.view.sprites.popup_menu import PopupMenu
from lib.weak_bound_method import WeakBoundMethod as Wbm
from src.view import Window

class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Ed.add(Tick, Scene.window.update)
        self.resolution = (960,540)
        Ed.add(Tick, self.update)
        self.showing_menu = None
        self.change_showing_menu("Main")

    def change_showing_menu(self, new_menu):
        if self.resolution == (960,540):
            if new_menu == "Main":
                self.showing_menu = PopupMenu([("Play", EndScene(self.__class__)), ("Resolution", Wbm(self.change_showing_menu, "Resolution"))], (100, 100), max_size=40, text_height_percentage=10)
        
            if new_menu == "Resolution":
                self.showing_menu = PopupMenu([("960x540", Wbm(self.set_window_resolution, (960,540))), ("600x900", Wbm(self.set_window_resolution, (600,900))), ("Back", Wbm(self.change_showing_menu, "Main"))], (100, 100), max_size=40, text_height_percentage=10)

        if self.resolution == (600,900):
            if new_menu == "Main":
                self.showing_menu = PopupMenu([("Play", EndScene(self.__class__)), ("Resolution", Wbm(self.change_showing_menu, "Resolution"))], (50, 50), max_size=40, text_height_percentage=5)
        
            if new_menu == "Resolution":
                self.showing_menu = PopupMenu([("960x540", Wbm(self.set_window_resolution, (960,540))), ("600x900", Wbm(self.set_window_resolution, (600,900))), ("Back", Wbm(self.change_showing_menu, "Main"))], (50, 50), max_size=40, text_height_percentage=5)


    def set_window_resolution(self, resolution):
        self.resolution = resolution
        if resolution == (600,900):
            self.showing_menu = PopupMenu([("960x540", Wbm(self.set_window_resolution, (960,540))), ("600x900", Wbm(self.set_window_resolution, (600,900))), ("Back", Wbm(self.change_showing_menu, "Main"))], (50, 50), max_size=40, text_height_percentage=5)
        
        if resolution == (960,540):
            self.showing_menu = PopupMenu([("960x540", Wbm(self.set_window_resolution, (959,530))), ("600x900", Wbm(self.set_window_resolution, (600,900))), ("Back", Wbm(self.change_showing_menu, "Main"))], (100, 100), max_size=40, text_height_percentage=10)

        Window().resolution = resolution


        
    def __del__(self): 
        self.showing_menu.__del__()



    def update(self, event):
        pass