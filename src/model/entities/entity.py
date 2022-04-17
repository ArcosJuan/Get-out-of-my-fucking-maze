

class Entity:
    def __init__(self, walkable=False):
        # Indicates if the entity can be passed over.
        self.walkable = walkable 
        


    def get_walkable(self): return self.walkable




    def interact(self): raise NotImplementedError

