import pygame as pg
from lib.weak_bound_method import WeakBoundMethod as Wbm
from src.controller import EventDispatcher as Ed
from src.events import Click
from src.events import EndScene
from src.events import Tick
from src.events import Quit
from src.view import Window
from src.view.scenes import Scene
from src.view.sprites import PopupMenu
from src.view.sprites import Sprite


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        Ed.add(Tick, Scene.window.update)
        Ed.add(Tick, self.update)
        self.resolutions = self.create_resolutions()
        self.set_window_resolution(self.resolutions[1])
        self.showing_menu = None
        self.change_showing_menu("Main")

    def create_resolutions(self):
        max_resolution = Window().get_display_size()
        sprite_size = Sprite.get_actual_size()
        resolutions = [
            (int(max_resolution[0]/i), int(max_resolution[1]/i)) 
            for i in range(1,4)
        ]
        
        # We calculate the optimal resolutions to avoid black borders on the screen.
        return [
            (int(res[0]/sprite_size)*sprite_size, int(res[1]/sprite_size)*sprite_size) 
            for res in resolutions
        ]
        

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
                txt_to_pct=1,
                text_active_color=(0,255,0),
            )
    
        elif new_menu == "Resolution":
            options = [(
                f"{res[0]}x{res[1]}", 
                Wbm(self.set_window_resolution, None, res)
                ) for res in self.resolutions
            ]
        
            options.extend([
                ("Full Screen", Wbm(self.set_window_resolution, None, Window().get_display_size(), pg.FULLSCREEN)),
                ("Back", Wbm(self.change_showing_menu, None, "Main")),
            ])

            current_resolution = self.resolutions.index(Window().get_resolution()) if Window().get_resolution() in self.resolutions else 0
            self.showing_menu = PopupMenu(
                options=options,
                box_relative_pos=(1/2, 1/2),
                max_size=40,
                txt_to_pct=1,
                text_active_color=(0,255,0),
                initial_index=current_resolution,
            )

    
    def set_window_resolution(self, resolution, flags=0):
        Window().set_resolution(resolution, flags)
        Window().background = (0,0,0)

        
    def __del__(self): 
        self.showing_menu.__del__()


    def update(self, event):
        pass