from src.events import Event


class UpdateResolution(Event):
    def __init__(self):
        super().__init__()