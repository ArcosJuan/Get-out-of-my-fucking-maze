

class Entity:
    def __init__(self, walkable=False, reachable=False):
        # Indicates if the entity can be passed over.
        self.walkable = walkable 
        
        # Indicates whether the entity can be interacted with from a distance cell.
        self.reachable = reachable 


    def get_walkable(self): return self.walkable


    def get_reachable(self): return self.reachable


    def interact(self): raise NotImplementedError

