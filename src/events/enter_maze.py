from src.events import Event


class EnterMaze(Event):
    def __init__(self, maze):
        super().__init__()
        self.maze = maze

    
    def get_maze(self): return self.maze