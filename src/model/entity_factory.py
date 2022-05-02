from src.references import Entity

from src.model.entities import Innocent
from src.model.entities import Ladder
from src.model.entities import Wall


class EntityFactory:

    entities_equivalences = {
        Entity.INNOCENT: Innocent,
        Entity.LADDER: Ladder,
        Entity.WALL: Wall,
    }


    @classmethod
    def get_object(cls, entity, *args):
        return cls.entities_equivalences[entity](*args)