from lib.abstract_data_types import NonDirectionalGraph
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from src.controller import EventDispatcher as Ed
from src.events import MoveEntity
from src.events import MapUpdated


class Map:

    def __init__(self):
        self.positions: Matrix = self._generate_positions(size)
        self.entities = NonDirectionalGraph() # {Position -- Object} 
        self.chunks= self._generate_chunks(size, self.positions)
        self.cells = self._generate_cells(self.positions)


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


    def get_chunk_by_position(self, position) -> Chunk:
        """ Receive a position and return to the chunk it belongs to.
        """

        position_index = list(position.get_index())
        length = Chunk.get_length()

        chunk_index = (
            position_index[0] // (length[0]), position_index[1] // (length[1])
        )

        chunk = self.chunks.get_element(chunk_index)

        if not chunk.has(position): raise KeyError()

        return chunk
        

    def get_adjacent_positions(self, position, include_diagonals=True) -> list:
        """ Returns the list of Position objects 
            adjacent to the one given by parameter.
        """

        return self.positions.get_adjacencies(self.positions.index(position), include_diagonals)


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
        """ Receives a position and an Entity 
            and adds them to the non-directional graph of entities.
        """

        self.entities.add_edge((position, entity))


    def get_entities(self, positions: list) -> dict:
        """ Returns a dictionary with the passed positions as keys 
            and the list of entities of each position as value. 
            If nothing is found in the positions, it returns an empty dict.
        """
        
        entities = dict()
        entities |= {
            position: self.entities.get_adjacencies(position)
            for position in positions
            if self.entities.has_node(position)
            }
            
        return entities


    def get_entity(self, position) -> dict:
        """ Returns a dictionary with the passed position as key 
            and the list of entities at that position as value. 
            If nothing is found at that position, it returns None.
        """

        if self.entities.has_node(position):
            return {position: self.entities.get_adjacencies(position)}

        else: return None


    def get_entity_position(self, entity) -> Position:
        return list(self.entities.get_adjacencies(entity))[0]


    def get_size(self) -> tuple: return self.positions.length()


    def get_cells(self, positions:iter) -> dict:
        """ Return a dict of biomes with Positions
            as keys based on self.cells.
        """

        return {position:self.cells[position] for position in positions}
        

    def move_entity(self, event) -> bool:
        """ Moves an entity to another position.
            Recives an event with an entity and it's destination.
            Returns a bool that indicates if it could be moved.
        """

        if  not self.passable_position(event.get_destination()):
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
        
        Ed.post(MapUpdated([past_position, event.get_destination()]))

        return True 


    def _generate_chunks(self, positions:Matrix) -> Matrix:
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        raise NotImplementedError


    def _generate_cells(self, positions:Matrix) -> dict:
        """ Receives an iterable of Position type objects and
            generate a dict of Biomes with a position as key.
        """
        
        raise NotImplementedError


    def generate_spawn_points(self, quantity:int=1) -> set[Position]:
        """ Returns a set of positions to place 
            the given quantity of caractors.
        """

        raise NotImplementedError



    def passable_position(self, position) -> bool:
        """ Returns True if it's no problem with pass over a position.
        """

        raise NotImplementedError


    