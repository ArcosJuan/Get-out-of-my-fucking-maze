import random
from lib.abstract_data_types import Matrix
from lib.abstract_data_types import NonDirectionalGraph
from lib.position import Position 
from src.model import EntityFactory
from src.references.data import MAZES

class Maze:
    available_mazes = list()


    @classmethod
    def get_new_name(cls):
        if not cls.available_mazes:
            cls.available_mazes =  [name for name in MAZES.keys()] 
        
        maze_name = random.choice(cls.available_mazes)
        cls.available_mazes.remove(maze_name)
        return maze_name


    def __init__(self):
        self.name = self.get_new_name()
        self.positions = Matrix()
        self.cells = dict()
        self.entities = NonDirectionalGraph() 
        
        self._load()


    def _load(self):
        """ Based on the data files, 
            create the positions, cells and entities of the maze.
        """

        tile_map = MAZES[self.name][0] # Matrix
        entity_map = MAZES[self.name][1] # Dict

        size = tile_map.length()
        self.positions =  Matrix(
            Position.create_collection((0,0), (size[0] -1 ,size[1] -1))
        )

        self.cells = {
            position: tile_map.get_element(position.get_index())
            for position in self.positions
        }

        for position in self.positions:
            if position.get_index() in entity_map.keys():
                entity = EntityFactory.get_object(entity_map[position.get_index()])
                self.entities.add_edge((position, entity))


    