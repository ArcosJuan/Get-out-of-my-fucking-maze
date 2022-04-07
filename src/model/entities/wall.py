from src.model.entities import Entity


class Wall(Entity):
    
    def __init__(self):
        self.avoidable = False