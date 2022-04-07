from enum import auto
from enum import Enum

class Layer(Enum):
    """ A separator of sprites. 
        The order of the variables here is the same order in which 
        they will be drawn.
    """

    CELL = auto()
    ENTITY = auto()
    CHARACTOR = auto()
