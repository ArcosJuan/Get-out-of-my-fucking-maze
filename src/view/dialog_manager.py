from src.events import ArrowKey
from src.events import DialogInit
from src.events import ReturnKey
from src.events import Tick
from src.controller import Chronometer
from src.controller import EventDispatcher as Ed
from src.references.images import PRESS_N
from src.view.sprites import DialogBoxSprite
from src.view.sprites.simple_sprite import SimpleSprite
from src.view.window import Window


class DialogManager:
    def __init__(self):
        Ed.add(DialogInit, self.initialize_dialogue)

        self.dialog_box = DialogBoxSprite()
        
        self.press_n_alert = SimpleSprite(PRESS_N, window_percentage=10, min_height=20, max_height=50)
        self.press_n_alert.rect.bottomright = Window().resolution
        self.press_n_time = Chronometer(1)

        self.dialogues = []
    

    def initialize_dialogue(self, event):
        """ Change the game events to DialogMode and start the
            interface to show the given dialogues.

            Recives:
                dialogues: <list[string]>
        """

        Ed.add(Tick, self.update)
        Ed.add_exclusive_listener(ArrowKey, self.pass_dialog)
        Ed.add_exclusive_listener(ReturnKey, self.pass_dialog)

        for dialogue in event.get_dialogues():
            self.dialogues.extend(self.dialog_box.adjust_text(dialogue))

        self.pass_dialog()


    def pass_dialog(self, event=None): 
        if isinstance(event, ArrowKey):
            if event.get_y() != -1: return
    
        if self.dialogues:
            self.dialog_box.set_text(self.dialogues.pop(0))

        else:
            Ed.remove(Tick, self.update)
            Ed.remove_exclusive_listener(ArrowKey, self.pass_dialog)
            Ed.remove_exclusive_listener(ReturnKey, self.pass_dialog)


    def update(self, event= None):
        self.dialog_box.draw()
        if self.press_n_time.get_update(): self.press_n_alert.draw()

