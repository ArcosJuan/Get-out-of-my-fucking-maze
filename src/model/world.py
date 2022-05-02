import random 
from lib.abstract_data_types import NonDirectionalGraph
from lib.abstract_data_types import Matrix
from lib.chunk import Chunk
from lib.position import Position
from src.controller import EventDispatcher as Ed
from src.events import MapUpdated
from src.events import MoveEntity
from src.model import BiomesManager
from src.model import Map
from src.model import Maze
from src.model.entities import Entity
from src.references.biome import Biome


class World(Map):
    """ Class that represents the physical space where 
        are all the characters and buildings of the game
    """
    
    def __init__(self, size:tuple = (128,128), min_size:tuple = (20,30), biomes:int=64, maze_ratio:int=4):
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
        self.chunks= self._generate_chunks(self.positions, min_size, size)
        self.cells = self._generate_cells(self.positions, biomes, maze_ratio)



    def _generate_chunks(self, positions:Matrix, min_size:tuple, size:tuple) -> Matrix:
        """ Returns a Matrix of Chunk objects based on a given size 
            (the minimum number of cells that can fit in a Chunk).
        """

        chunk_size = list(min_size)
        Chunk.set_length(chunk_size)
        for i in range(2):
            while True:
                if not (size[i]%chunk_size[i]):
                    break
                chunk_size[i] +=1

        Chunk.set_length(chunk_size)
        chunks_amount = (size[0] * size[1]) // (chunk_size[0] * chunk_size[1])

        splited_positions = positions.split(chunks_amount, chunk_size)

        return Matrix(
            [[Chunk(positions, (y,x)) for x, positions in enumerate(row)]
            for y, row in enumerate(splited_positions.iter_rows())]
        )


    def _generate_cells(self, positions:Matrix, biomes_qty, maze_ratio) -> dict:
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
        self._generate_mazes(sorted_index, biomes_qty//maze_ratio)
        return {position:seeds[next(zones)] for position in positions}


    def _generate_mazes(self, seeds, qty):
        seeds = iter(seeds)
        for _ in range(qty):
            position = self.positions.get_element(next(seeds))
            self.add_entity(position, Maze())    


    def generate_spawn_points(self, quantity:int=1) -> set[Position]:
        """ Returns a set of positions to place 
            the given quantity of caractors.
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


    def passable_position(self, position):
        """ Returns True if it's no problem with pass over a position.
        """
        
        if not BiomesManager.get_passable(self.cells[position]): 
            return False

        elif self.entities.has_node(position): 
            for entity in self.entities.get_adjacencies(position):
                if isinstance(entity, Entity):
                    return entity.get_walkable()


        else: return True    


    
