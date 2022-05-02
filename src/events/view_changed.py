from src.events import Event


class ViewChanged(Event):
    def __init__(self):
        super().__init__()
