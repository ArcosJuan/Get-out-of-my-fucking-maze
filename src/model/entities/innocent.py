import json
import random
from src.controller import EventDispatcher as Ed
from src.events import DialogInit
from src.events import Die
from src.events import Kill
from src.model.entities import Entity
from src.references.data import INNOCENTS


class Innocent(Entity):
    available_innocents = list()


    @classmethod
    def get_new_name(cls):
        if not cls.available_innocents:
            cls.available_innocents =  [name for name in INNOCENTS.keys()] 
        
        innocent_name = random.choice(cls.available_innocents)
        cls.available_innocents.remove(innocent_name)
        return innocent_name
           

    def __init__(self):
        super().__init__(reachable=True)
        self.name = self.get_new_name()
        self.dialogs = INNOCENTS[self.name]


    def interact(self):
        Ed.add(Kill, self.get_killed)
        Ed.post(DialogInit(random.choice(self.dialogs)))

    
    def get_killed(self, event):
        Ed.remove(Kill, self.get_killed)
        Ed.post(Die(self))
        
