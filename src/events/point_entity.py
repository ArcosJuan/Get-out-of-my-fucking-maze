from src.events import Event


class PointEntity(Event):
    def __init__(self, position, chunk):
        super().__init__()
        self.chunk = chunk
        self.position = position

    
    def get_entity(self): return self.entity


    def get_chunk(self): return self.chunk


    def get_position(self): return self.position