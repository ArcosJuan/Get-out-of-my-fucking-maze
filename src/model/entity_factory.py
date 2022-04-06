from src.references import Entity
from src.model import Innocent


class EntityFactory:

    entities_equivalences = {
        Entity.INNOCENT: Innocent
    }


    @classmethod
    def get_object(cls, entity):
        return cls.entities_equivalences[entity]()