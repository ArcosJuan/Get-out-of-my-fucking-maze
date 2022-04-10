from src.events import Event


class ChangeMode(Event):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode


    def get_mode(self): return self.mode