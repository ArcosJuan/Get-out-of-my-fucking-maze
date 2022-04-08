from src.events import Event


class ChangeDialogMode(Event):
    def __init__(self):
        super().__init__()