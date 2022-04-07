from src.events import Event


class ExitMaze(Event):
    def __init__(self):
        super().__init__()