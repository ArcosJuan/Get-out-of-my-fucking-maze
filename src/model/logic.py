from src.controller import EventDispatcher as Ed
from src.events import ArrowKey
from src.events import EnterMaze
from src.events import ExitMaze
from src.events import ReturnKey
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
        Ed.add(ReturnKey, self.interact)
        Ed.add(GameStart, self.game_start)
        Ed.add(EnterMaze, self.enter_maze)
        Ed.add(ExitMaze, self.exit_maze)
        Ed.add(ViewChanged, self.point_player)
        self.player: Player = Player()
        self.world: World = None 
        self.maze = None


    def get_actual_place(self): return self.maze if self.maze else self.world


    def get_player_position(self): return self.get_actual_place().get_entity_position(self.player)


    def game_start(self, event):
        self.world =  World(min_size=event.get_min_size())
        player_position = list(self.world.generate_spawn_points())[0]
        self.world.add_entity(player_position, self.player)
        Ed.post(WorldGenerated(self.world))


    def move_player(self, event):
        player_position = self.get_player_position()

        player_position_x = player_position.get_index()[1] + event.get_x()
        player_position_y = player_position.get_index()[0] - event.get_y()

        if player_position_x < self.get_actual_place().get_size()[1] \
            and player_position_y < self.get_actual_place().get_size()[0] \
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
        actual_place = self.get_actual_place()
        player_position = actual_place.get_entity_position(self.player)
        entities = actual_place.get_entity(player_position)
        if entities: entities = entities[player_position]

        for entity in entities:
            if isinstance(entity, Entity):
                entity.interact()
                return
        
        # If it is not on any entity, check if it is in the range of a reachable entity.
        adjacent_pos = actual_place.get_adjacent_positions(player_position, False)
        adjacent_entities = actual_place.get_entities(adjacent_pos)
        if adjacent_entities:
            for pos in adjacent_entities.keys():
                for entity in adjacent_entities[pos]:
                    if isinstance(entity, Entity):
                        if entity.get_reachable():
                            entity.interact()


    def enter_maze(self, event):
        self.maze = event.get_maze()
        player_position = list(self.maze.generate_spawn_points())[0]
        self.maze.add_entity(player_position, self.player)


    def exit_maze(self, event):
        self.maze = None


    def point_player(self, event=None):
        player_chunk = self.get_actual_place().get_chunk_by_position(self.get_player_position())
        Ed.post(PointEntity(self.get_player_position(),player_chunk))

