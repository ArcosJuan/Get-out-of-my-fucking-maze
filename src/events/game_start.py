from src.events import Event


class GameStart(Event):
    def __init__(self, min_size):
        super().__init__()        
        self.min_size = min_size

    
    def get_min_size(self): return self.min_size