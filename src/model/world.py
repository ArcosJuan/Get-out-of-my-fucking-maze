import random 
from src.events import MoveEntity
from src.events import WorldUpdated
from lib.abstract_data_types import NonDirectionalGraph
from lib.abstract_data_types import DirectionalGraph
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from src.model import BiomesManager
from src.model import Maze
from src.model import Innocent
from src.controller.event_dispatcher import EventDispatcher as Ed
from src.references.biome import Biome


class World:
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """
    
    def __init__(self, size:tuple = (128,128), min_size:tuple = (20,30), biomes:int=64):
        assert biomes <= 128, \
            "So many biomes take a long time to generate the world"
        
        assert size[0]/2 >= biomes, (
            "The requested number of biomes" 
            "is not very suitable for the size of the map"
        )

        Ed.add(MoveEntity, self.move_entity)

        self.size = size
        self.positions: Matrix = self._generate_positions(size)
        self.entities = NonDirectionalGraph() # {Position -- Object}
        self.chunks= self._generate_chunks(min_size, size, self.positions)
        self.cells = self._generate_cells(self.positions,biomes)


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


    def _generate_chunks(self, min_size:tuple, size:tuple, positions:Matrix) -> Matrix:
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

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


    def _generate_cells(self, positions:Matrix, biomes_qty=64) -> dict:
        """ Receives an iterable of Position type objects and
            generate a dict of Biomes with a position as key.
        """
        
        rows = sorted({
            BiomesManager.get_temperature(biome) 
            for biome in BiomesManager.get_biomes()
        })

        heat_zones = list()
        for temperature in rows:
            heat_zones.append(temperature)

        for temperature in reversed(rows):
            heat_zones.append(temperature)

        rows_biome = positions.length()[0]/ biomes_qty
        biomes= dict()
        for i in range (biomes_qty):
            biome = BiomesManager.select_random(BiomesManager.get_biomes())
            temperature = BiomesManager.get_temperature(biome)
            biomes.setdefault(temperature, list())
            biomes[temperature].append(biome)

        rows_temperature = {
            temperature: int((len(biomes[temperature]) * rows_biome) /
            (heat_zones.count(temperature))) for temperature in biomes
        }
        
        seeds = dict()
        seeds_index = dict()
        seed = 1
        while biomes:
            start_row = 0
            stop_row = int(rows_temperature[min(rows_temperature)]-1)
            for i,temperature in enumerate(heat_zones):
                if temperature in biomes and biomes[temperature]:
                    if i != 0:
                        start_row = stop_row
                        stop_row += rows_temperature[temperature]

                    row = positions.get_row(
                        random.randrange(start_row, stop_row)
                    )
                    biome = biomes[temperature].pop()
                    seeds[seed] = biome
                    seeds_index[seed] = (random.choice(row).get_index())
                    seed +=1

                else:
                    if temperature in biomes:
                        biomes.pop(temperature)
                    continue
                    
        sorted_index = [seeds_index[key] for key in sorted(seeds_index)]
        zones = iter(positions.generate_voronoi_tesselation(sorted_index))
        self._generate_mazes(sorted_index, biomes_qty//8)
        return {position:seeds[next(zones)] for position in positions}

    def _generate_mazes(self, seeds, qty):
        seeds = iter(seeds)
        for _ in range(qty):
            position = self.positions.get_element(next(seeds))
            self.add_entity(position, Maze())
        pass    


    def generate_spawn_points(self, quantity:int=1) -> set[Position]:
        """ Returns a Chunk and a Position on that 
            chunk where to place a charactor.
        """

        positions = set()
        while True:
            chunk = self.chunks.random()
            positions = set()
            for _ in range(quantity):
                position = chunk.get_random_position()
                
                if BiomesManager.get_passable(self.cells[position]):
                    positions.add(position)
            
            if len(positions) == quantity: break
        
        return positions

    
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
        
        if not BiomesManager.get_passable(self.cells[position]): 
            return True

        elif self.entities.has_node(position): 
            for entity in self.entities.get_adjacencies(position):
                entity
                if isinstance(entity, Innocent):
                    return True


        else: return False    


    def get_size(self): return self.size
    
