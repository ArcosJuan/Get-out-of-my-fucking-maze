from src.events import Event


class DialogInit(Event):
    def __init__(self, dialogues):
        super().__init__()
        self.dialogues = dialogues

    
    def get_dialogues(self): return self.dialogues