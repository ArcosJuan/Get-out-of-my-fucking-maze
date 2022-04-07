import random
from lib.abstract_data_types import Matrix
from lib.abstract_data_types import NonDirectionalGraph
from lib.chunk import Chunk
from lib.position import Position 
from src.events import EnterMaze
from src.events import MoveEntity
from src.events import WorldUpdated
from src.controller.event_dispatcher import EventDispatcher as Ed
from src.model import EntityFactory
from src.model.entities import Entity
from src.model.entities import Innocent
from src.model.entities import Ladder
from src.references.data import MAZES
from src.references import Tile


class Maze(Entity):
    available_mazes = list()


    @classmethod
    def get_new_name(cls):
        if not cls.available_mazes:
            cls.available_mazes =  [name for name in MAZES.keys()] 
        
        maze_name = random.choice(cls.available_mazes)
        cls.available_mazes.remove(maze_name)
        return maze_name


    def __init__(self, min_size:tuple = (40,40)):
        self.avoidable = True
        Ed.add(MoveEntity, self.move_entity)

        self.name = self.get_new_name()
        self.positions: Matrix = self._generate_positions(min_size)
        self.entities = NonDirectionalGraph() # {Position -- Object} 
        self.chunks= self._generate_chunks(min_size, self.positions)
        self.cells = self._generate_cells(self.positions)

        self._load()


    def _load(self):
        """ Based on the data files, 
            create the positions, cells and entities of the maze.
        """

        tile_map = MAZES[self.name][0] # Matrix
        entity_map = MAZES[self.name][1] # Dict

        size = tile_map.length()

        for position in self.positions:
            try:
                self.cells |= {position: tile_map.get_element(position.get_index())}
            except IndexError:
                continue
        

        for position in self.positions:
            if position.get_index() in entity_map.keys():
                entity = EntityFactory.get_object(entity_map[position.get_index()])
                self.entities.add_edge((position, entity))

    
    def interact(self): Ed.post(EnterMaze(self))
  

    def get_position(self, position_index) -> (Chunk,Position):
        """ Returns the chunk and position 
            object that match with the given position index.
        """
        
        position = self.positions.get_element(position_index)
        length = Chunk.get_length()

        chunk_index = (
            position_index[0] // (length[0]), position_index[1] // (length[1])
        )

        chunk = self.chunks.get_element(chunk_index)

        if not chunk.has(position): raise KeyError()

        return (chunk, position)


    def get_adjacent_chunks(self, chunk) -> list:
        """ Returns the list of Chunk objects 
            adjacent to the one given by parameter.
        """

        return self.chunks.get_adjacencies(chunk.get_index())


    def get_adjacent_positions(self, position) -> list:
        """ Returns the list of Position objects 
            adjacent to the one given by parameter.
        """

        return self.positions.get_adjacencies(self.positions.index(position))


    def get_limit(self) -> Position:
        """ Returns the last Position in the world.
        """

        index = self.positions.get_last_index()
        return self.positions.get_element(index)


    def _generate_positions(self, size:tuple) -> Matrix:
        """ Generates a Matrix of Position type objects 
            based on the given size.
        """

        return Matrix(
            Position.create_collection((0,0), (size[0] -1 ,size[1] -1))
        )


    def add_entity(self, position, entity):
        self.entities.add_edge((position, entity))


    def get_entities(self, positions: list):
        entities = dict()
        entities |= {
            position: self.entities.get_adjacencies(position)
            for position in positions
            if self.entities.has_node(position)
            }
            
        return entities


    def get_entity(self, position):
        if self.entities.has_node(position):
            return {position: self.entities.get_adjacencies(position)}

        else: return None


    def get_entity_position(self, entity):
        return list(self.entities.get_adjacencies(entity))[0]


    def _generate_chunks(self, min_size:tuple, positions:Matrix) -> Matrix:
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        size = min_size
        chunk_size = list(min_size)
        for i in range(2):
            while True:
                if not (size[i]%chunk_size[i]):
                    break
                chunk_size[i] +=1

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
        

    def move_entity(self, event):
        """ Moves an entity to another position.
            Recives an event with an entity and it's destination.
        """
        if  self.avoid_position(event.get_destination()):
            return False

        entity = event.get_entity()
        
        # Saves the position of ther charactor.
        past_position = list(self.entities.get_adjacencies(entity))[0]
        
        # Removes the position of ther charactor and the charactor 
        # from the entities graph.
        self.entities.remove_node(entity)
        self.entities.remove_empty_nodes()

        # Creates an edge between the charactor and the destination 
        # position in the graph.
        self.entities.add_edge((entity, event.get_destination()))
        
        Ed.post(WorldUpdated([past_position, event.get_destination()]))

        return True 


    def avoid_position(self, position):
        """ Returns True if it's no problem with pass over a position.
        """

        if self.entities.has_node(position): 
            for entity in self.entities.get_adjacencies(position):
                if isinstance(entity, Entity):
                    return not entity.get_avoidable()


        else: return False    


    def get_size(self): return self.positions.length()
    
