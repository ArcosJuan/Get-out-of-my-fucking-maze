import random
from lib.abstract_data_types import NonDirectionalGraph
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from src.controller import EventDispatcher as Ed
from src.events import MapUpdated
from src.events import MoveEntity
from src.events import EnterMaze
from src.model import EntityFactory
from src.model import Map
from src.model.entities import Entity
from src.model.entities import Innocent
from src.model.entities import Ladder
from src.references import Tile
from src.references.data import MAZES


class Maze(Map, Entity):
    available_mazes = list()


    @classmethod
    def get_new_name(cls):
        if not cls.available_mazes:
            cls.available_mazes =  [name for name in MAZES.keys()] 
        
        maze_name = random.choice(cls.available_mazes)
        cls.available_mazes.remove(maze_name)
        return maze_name


    def __init__(self):
        self.avoidable = True
        Ed.add(MoveEntity, self.move_entity)

        self.name = self.get_new_name()
        size = self._calculate_size()
        self.positions: Matrix = self._generate_positions(size)
        self.entities = NonDirectionalGraph() # {Position -- Object} 
        self.chunks= self._generate_chunks(size, self.positions)
        self.cells = self._generate_cells(self.positions)

        self._load()


    def _calculate_size(self):
        """ Based on the size of the map to be loaded, 
            and the size of the chunks returns the size 
            that the position matrix should have.
        """

        chunk_size = list(Chunk.get_length())
        map_size = list(MAZES[self.name][0].length())
        map_size = [size*2 for size in map_size]
        min_size = list((max(chunk_size[0], map_size[0]), max(chunk_size[1], map_size[1])))
        for i in range(2):
            while True:
                if not (min_size[i]%chunk_size[i]):
                    break
                min_size[i] +=1

        return min_size


    def _load(self):
        """ Based on the data files, 
            create the positions, cells and entities of the maze.
        """

        tile_map = MAZES[self.name][0] # Matrix
        entity_map = MAZES[self.name][1] # Dict

        size = tile_map.length()
        center_pos = self.positions.get_center()

        for pos in self.positions:
            corrected_index = (center_pos.y + pos.y, center_pos.x + pos.x) 
            try:
                corrected_pos = self.positions.get_element(corrected_index)
            
                if pos.get_index() in entity_map.keys():
                    entity = EntityFactory.get_object(entity_map[pos.get_index()])
                    self.entities.add_edge((corrected_pos, entity))
            
                self.cells |= {corrected_pos: tile_map.get_element(pos.get_index())}
            except IndexError:
                continue
        

    
    def interact(self): Ed.post(EnterMaze(self))


    def _generate_chunks(self, min_size:tuple, positions:Matrix) -> Matrix:
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        size = positions.length()
        chunk_size = Chunk.get_length()

        chunks_amount = (size[0] * size[1]) // (chunk_size[0] * chunk_size[1])

        splited_positions = positions.split(chunks_amount)

        return Matrix(
            [[Chunk(positions, (y,x)) for x, positions in enumerate(row)]
            for y, row in enumerate(splited_positions.iter_rows())]
        )
        

    def _generate_cells(self, positions:Matrix) -> dict:
        """ Receives an iterable of Position type objects and
            generate a dict of Biomes with a position as key.
        """
        
        return {position:Tile.EMPTY for position in positions}


    def generate_spawn_points(self, quantity:int=1) -> set[Position]:
        """ Returns a set of positions to place 
            the given quantity of caractors.
        """

        for position in self.positions:
            if self.entities.has_node(position): 
                for entity in self.entities.get_adjacencies(position):
                    if isinstance(entity, Ladder):
                        return {position}
        return {self.positions.get_element((0,0))}


    def get_cells(self, positions:iter):
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """

        return {position:self.cells[position] for position in positions}


    def avoid_position(self, position):
        """ Returns True if it's no problem with pass over a position.
        """

        if self.entities.has_node(position): 
            for entity in self.entities.get_adjacencies(position):
                if isinstance(entity, Entity):
                    return not entity.get_avoidable()


        else: return False    
    
