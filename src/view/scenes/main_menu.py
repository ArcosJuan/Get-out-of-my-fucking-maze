from lib.weak_bound_method import WeakBoundMethod as Wbm
from src.controller import EventDispatcher as Ed
from src.events import Click
from src.events import EndScene
from src.events import Tick
from src.events import Quit
from src.view import Window
from src.view.scenes import Scene
from src.view.sprites import PopupMenu


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Ed.add(Tick, Scene.window.update)
        self.resolution = (960,540)
        Ed.add(Tick, self.update)
        self.showing_menu = None
        self.change_showing_menu("Main")

    def change_showing_menu(self, new_menu):
        if new_menu == "Main":
            self.showing_menu = PopupMenu(
                [
                    ("Play", EndScene(self.__class__)),
                    ("Resolution", Wbm(self.change_showing_menu, None, "Resolution")),
                    ("Exit", Quit())
                ],
                (1/2, 1/2),
                max_size=40,
                txt_a_pct=1
            )
    
        if new_menu == "Resolution":
            self.showing_menu = PopupMenu(
                [
                    ("960x540", Wbm(self.set_window_resolution, None, (960,540))),
                    ("600x900", Wbm(self.set_window_resolution, None, (600,900))), 
                    ("300x900", Wbm(self.set_window_resolution, None, (900,300))), 
                    ("Back", Wbm(self.change_showing_menu, None, "Main"))
                ], 
                    (1/2, 1/2),
                    max_size=40,
                    txt_a_pct=1
            )

    
    def set_window_resolution(self, resolution, flags=0):
        Window().set_resolution(resolution, flags)
        Window().background = (0,0,0)

        
    def __del__(self): 
        self.showing_menu.__del__()


    def update(self, event):
        pass