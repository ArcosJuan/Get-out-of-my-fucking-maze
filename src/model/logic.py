from src.events import ArrowKey
from src.events import MoveEntity
from src.events import MoveCamera
from src.events import CellPressed
from src.events import GameStart
from src.events import PointEntity
from src.events import WorldGenerated
from src.model.biomes_manager import BiomesManager
from src.model import World
from src.controller.event_dispatcher import EventDispatcher as Ed
from src.model.charactors import Player
from src.view import Window
from src.view.sprites import Sprite


class Logic:
    def __init__(self):
        Ed.add(ArrowKey, self.move_player)
        Ed.add(GameStart, self.game_start)
        self.player: Player = Player()
        self.world: World = None 


    def game_start(self, event):
        self.world = self._create_world()
        player_position = list(self.world.generate_spawn_points())[0]
        self.world.add_entity(player_position, self.player)
        Ed.post(WorldGenerated(self.world))
        
        position = self.world.get_position(player_position.get_index())
        Ed.post(PointEntity(
            position[1],
            position[0]
        ))


    def _create_world(self):
        # Needs to get the quantity of cells in the window, 
        # in order to get a correct size to the horizon line.
        grid_lenght = Window().calculate_grid(Sprite.get_min_size())
        horizon_line = grid_lenght[1] if grid_lenght[1] > grid_lenght[0] else grid_lenght[0]

        world = World(horizon_line)
        return world


    def move_player(self, event):
        player_position = self.world.get_entity_position(self.player)

        
        player_position_x = player_position.get_index()[1] + event.get_x()
        player_position_y = player_position.get_index()[0] - event.get_y()

        if player_position_x < self.world.get_size()[0] and player_position_y < self.world.get_size()[1]  and player_position_x > 0 and player_position_y > 0:

            player_destination = self.world.get_position((player_position_y, player_position_x))
            if self.world.move_entity(MoveEntity(self.player, player_destination[1])):
                Ed.post(MoveCamera(event.get_x(), event.get_y()))
            