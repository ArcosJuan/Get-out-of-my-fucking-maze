from src.controller import EventDispatcher as Ed
from src.events import ExitMaze
from src.model.entities import Entity


class Ladder(Entity):
    
    def __init__(self):
        super().__init__(walkable=True)

    def interact(self):
        Ed.post(ExitMaze())