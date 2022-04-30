from src.events import ArrowKey
from src.events import DialogInit
from src.events import ReturnKey
from src.events import Die
from src.events import Tick
from src.events import Kill
from src.controller import Chronometer
from src.controller import EventDispatcher as Ed
from src.references.images import NEXT_DIALOG
from src.view.sprites import DialogBoxSprite
from src.view.sprites.popup_menu import PopupMenu
from src.view.sprites.simple_sprite import SimpleSprite
from src.view.window import Window


class DialogManager:
    def __init__(self):
        Ed.add(DialogInit, self.initialize_dialogue)

        self.dialog_box = DialogBoxSprite()
        
        self.next_dialog_alert = self.initialize_alert()
        self.next_dialog_time = Chronometer(1)

        self.battle_menu = None

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
            self.battle_menu = PopupMenu(
                [
                    ("Kill", Kill())
                ], 
                    (1/2, 1/2),
                    max_size=40,
                    txt_to_pct=1
            )
            Ed.add(Die, self.remove_battle_menu)
            Ed.remove(Tick, self.update)
            Ed.remove_exclusive_listener(ArrowKey, self.pass_dialog)
            Ed.remove_exclusive_listener(ReturnKey, self.pass_dialog)


    def remove_battle_menu(self, event):
        Ed.remove(Die, self.remove_battle_menu)
        self.battle_menu = None

    def update(self, event= None):
        self.dialog_box.draw()
        if self.next_dialog_time.get_update(): self.next_dialog_alert.draw()


    def initialize_alert(self):
        next_dialog_alert = SimpleSprite(
            NEXT_DIALOG, window_percentage=10, min_height=20, max_height=50
        )

        next_dialog_pos = (
            self.dialog_box.box_rect.bottomright[0] - self.dialog_box.box_margins[0],
            self.dialog_box.box_rect.bottomright[1]
        )

        next_dialog_alert.rect.bottomright = next_dialog_pos
        return next_dialog_alert