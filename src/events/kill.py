from src.events import Event


class Kill(Event):
    def __init__(self):
        super().__init__()