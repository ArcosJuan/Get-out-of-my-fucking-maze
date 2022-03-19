from src.events import Event


class MoveCamera(Event):
    def __init__(self, target_position, x = 0, y = 0):
        super().__init__()

        self.x = x
        self.y = y
        self.target_position = target_position

    
    def get_x(self): return self.x

    def get_y(self): return self.y

    def get_target_position(self): return self.target_position