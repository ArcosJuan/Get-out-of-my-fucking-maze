from src.events import Tick
from src.events import EnterMaze
from src.events import ExitMaze
from src.events import MapUpdated
from src.events import PointEntity
from src.events import ViewChanged
from src.events import WorldGenerated
from src.view.dialog_system.dialog_manager import DialogManager 
from src.view.scenes import Scene
from src.references import Layer
from src.controller.event_dispatcher import EventDispatcher as Ed



class Game(Scene):
    def __init__(self):
        super().__init__()
        self.view = None
        self.maze_view = None
        self.camera  = None
        dialog_manager = DialogManager()
        
        Ed.add(WorldGenerated, self.create_world_view)
        Ed.add(PointEntity, self.point_entity)
        Ed.add(MapUpdated, self.update_sprites)
        Ed.add(EnterMaze, self.load_maze)
        Ed.add(ExitMaze, self.load_world)

 
    def _create_view(self, model=None):
        from src.view import MapView
        from src.view import Camera
        
        self.view = MapView(model)
        self.camera = Camera(self.view)
        Ed.post(ViewChanged())
 

    def create_world_view(self, event):
        from src.view import MapView
        MapView.set_world_model(event.get_world())
        self._create_view()


    def load_world(self, event):
        self._create_view()


    def load_maze(self, event):
        self._create_view(event.get_maze())


    def point_entity(self, event):
        chunks = self.view.get_adjacent_chunks([event.get_chunk()])
        self.view.set_renderized_chunks("Player", chunks)
        
        self.camera.point(event.get_position())

    
    def update_sprites(self, event):
        """ Updates the state of the sprites 
            in the view and the camera.
        """
        
        self.view.update_entities(event.get_positions())

        for position in event.get_positions():
            # If the position is not being renderized 
            # view will not care about update sprites.
            if self.view.is_renderized(position):
                sprites = self.view.get_sprites([position])

                # If the position is not being seen 
                # camera will not care about update sprites.
                if self.camera.is_visible(position):
                    self.camera.update_visible_sprites({position: sprites[position]})

