from src.events.event import Event
# Non pygame events:
from src.events.dialog_init import DialogInit
from src.events.end_scene import EndScene
from src.events.enter_maze import EnterMaze
from src.events.exit_maze import ExitMaze
from src.events.game_start import GameStart
from src.events.interact import Interact
from src.events.world_generated import WorldGenerated
from src.events.cell_pressed import CellPressed
from src.events.point_entity import PointEntity
from src.events.pass_dialog import PassDialog
from src.events.interact import Interact
from src.events.move_camera import MoveCamera
from src.events.update_resolution import UpdateResolution
from src.events.move_entity import MoveEntity
from src.events.view_changed import ViewChanged
from src.events.map_updated import MapUpdated

# Pygame events:
from src.events.pygame_events.tick import Tick
from src.events.pygame_events.click import Click
from src.events.pygame_events.quit import Quit
from src.events.pygame_events.wheel import Wheel
from src.events.pygame_events.arrow_key import ArrowKey