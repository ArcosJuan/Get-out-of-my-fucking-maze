from src.events import Event
from src.references.data import DIALOGS


class DialogInit(Event):
    def __init__(self, dialog_id):
        super().__init__()
        self.dialogues = DIALOGS.get(dialog_id)

    
    def get_dialogues(self): return self.dialogues