from src.events import Event


class Die(Event):
    def __init__(self, innocent):
        super().__init__()
        self.innocent = innocent

    
    def get_innocent(self): return self.innocent