import json
import random
from src.model.entities import Entity
from src.references.data import DIALOGS
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
        self.avoidable = False
        self.name = self.get_new_name()
        self.dialogs = {key:DIALOGS[key] for key in INNOCENTS[self.name]}


