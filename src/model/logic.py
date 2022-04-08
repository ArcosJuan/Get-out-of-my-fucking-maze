from src.controller import EventDispatcher as Ed
from src.events import ArrowKey
from src.events import EnterMaze
from src.events import Interact
from src.events import MoveEntity
from src.events import MoveCamera
from src.events import GameStart
from src.events import PointEntity
from src.events import ViewChanged
from src.events import WorldGenerated
from src.model import BiomesManager
from src.model import Player
from src.model import World
from src.model.entities import Entity 
from src.view import Window
from src.view.sprites import Sprite


class Logic:
    def __init__(self):
        Ed.add(ArrowKey, self.move_player)
        Ed.add(Interact, self.interact)
        Ed.add(GameStart, self.game_start)
        Ed.add(EnterMaze, self.enter_maze)
        Ed.add(ViewChanged, self.point_player)
        self.player: Player = Player()
        self.world: World = None 
        self.maze = None


    def get_actual_place(self): return self.maze if self.maze else self.world


    def get_player_position(self): return self.get_actual_place().get_entity_position(self.player)


    def game_start(self, event):
        self.world =  World()
        player_position = list(self.world.generate_spawn_points())[0]
        self.world.add_entity(player_position, self.player)
        Ed.post(WorldGenerated(self.world))


    def move_player(self, event):
        player_position = self.get_player_position()

        player_position_x = player_position.get_index()[1] + event.get_x()
        player_position_y = player_position.get_index()[0] - event.get_y()

        if player_position_x < self.get_actual_place().get_size()[0] \
            and player_position_y < self.get_actual_place().get_size()[1] \
            and player_position_x >= 0 \
            and player_position_y >= 0:

            player_destination = self.get_actual_place().get_position(
                (player_position_y, player_position_x)
                )
                
            if self.get_actual_place().move_entity(
                MoveEntity(self.player, player_destination[1])
                ):

                Ed.post(MoveCamera(
                    (player_position_y, player_position_x),
                    event.get_x(), event.get_y()
                    ))


    def interact(self, event):
        player_position = self.get_actual_place().get_entity_position(self.player)
        entities = self.get_actual_place().get_entity(player_position)
        if entities: entities = entities[player_position]
        for entity in entities:
            if isinstance(entity, Entity):
                entity.interact()


    def enter_maze(self, event):
        self.maze = event.get_maze()
        player_position = list(self.maze.generate_spawn_points())[0]
        self.maze.add_entity(player_position, self.player)


    def point_player(self, event=None):
        player_chunk = self.get_actual_place().get_chunk_by_position(self.get_player_position())
        Ed.post(PointEntity(self.get_player_position(),player_chunk))

