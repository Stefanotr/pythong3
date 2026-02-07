"""
MapPageView Module

Handles the interactive map view between game acts.
Allows player navigation and transitions to different acts.
"""

import pygame
import os
from Views.PageView import PageView
from Views.MapView import MapView
from Views.CaracterView import CaracterView
from Views.PauseMenuView import PauseMenuView
from Views.ShopPageView import ShopPageView
from Controllers.PlayerController import PlayerController
from Controllers.ShopController import ShopController
from Controllers.GameSequenceController import GameSequenceController
from Models.ShopModel import ShopModel
from Models.PlayerModel import PlayerModel
from Models.MapModel import MapModel
from Models.TileModel import TileModel
from Models.BottleModel import BottleModel
from Utils.Logger import Logger
from Utils.AssetManager import AssetManager
from Controllers.GameState import GameState
import random


# === MAP PAGE VIEW CLASS ===

class MapPageView(PageView):
    """
    Interactive map view for navigation between acts.
    Displays the map, player character, and handles transitions to acts.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, current_act=1, player=None, sequence_controller=None):
        """
        Initialize the map page view.
        
        Args:
            screen: Pygame display surface
            current_act: Current act number (1 = Act 1, 2 = Act 2, 3 = Rhythm)
            player: Optional PlayerModel instance to preserve state (if None, creates new)
            sequence_controller: Optional GameSequenceController for stage navigation
        """
        try:
            # Get screen dimensions
            screen_info = pygame.display.Info()
            screen_width = screen_info.current_w
            screen_height = screen_info.current_h
            
            # Set window to center
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except:
                pass
            
            # Create resizable window at full screen size
            self.screen = pygame.display.set_mode(
                (screen_width, screen_height),
                pygame.FULLSCREEN
            )
            
            # Initialize PageView without background image to avoid visual artifacts on the map
            super().__init__("Map - Six-String Hangover", screen_width, screen_height, pygame.FULLSCREEN, None)
            
            # Store screen dimensions for camera calculations
            self.screen_width = screen_width
            self.screen_height = screen_height
            
            self.sequence_controller = sequence_controller
            Logger.debug("MapPageView.__init__", "Map view created with no background image to avoid visual bugs")
            self.current_act = current_act
            
            Logger.debug("MapPageView.__init__", "Map page view initialized", 
                        current_act=current_act, 
                        width=screen_width, 
                        height=screen_height)
            
            # === MAP INITIALIZATION ===
            
            try:
                # Use TMX map file if available
                tmx_path = "Game/Assets/maps/map.tmx"
                try:
                    self.map = MapModel(tmx_path, [], None)
                    Logger.debug("MapPageView.__init__", "TMX Map loaded", path=tmx_path)
                except Exception as e:
                    Logger.error("MapPageView.__init__", e)
                    # Fallback to old simple map if TMX not available
                    tile_kinds = [
                        TileModel("road", "Game/Assets/road3_carre.png", False),
                        TileModel("road2", "Game/Assets/road3_carre.png", False)
                    ]
                    self.map = MapModel("Game/Assets/maps/map.map", tile_kinds, 16)
                    Logger.debug("MapPageView.__init__", "Fallback map loaded")
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === PLAYER INITIALIZATION ===
            
            try:
                # Load player config first
                player_config = None
                try:
                    asset_manager = AssetManager()
                    player_config = asset_manager.load_player_config()
                    Logger.debug("MapPageView.__init__", f"Successfully loaded player_config with {len(player_config.get('actions', {}))} actions")
                except Exception as e:
                    Logger.debug("MapPageView.__init__", f"Failed to load player_config: {e}")
                    player_config = None
                
                # Get map dimensions
                map_width = len(self.map.tiles[0]) * self.map.tile_size if self.map.tiles else screen_width
                map_height = len(self.map.tiles) * self.map.tile_size if self.map.tiles else screen_height
                
                # Try to get spawn point from map TMX (if spawn objects are defined)
                spawn_x, spawn_y = None, None
                try:
                    spawn_points = self.map.get_spawn_points()
                    if spawn_points:
                        chosen_spawn = random.choice(spawn_points)
                        # Use center of spawn object, or top-left if no size
                        spawn_x = chosen_spawn.get('x', 0) + chosen_spawn.get('width', 0) // 2
                        spawn_y = chosen_spawn.get('y', 0) + chosen_spawn.get('height', 0) // 2
                        Logger.debug("MapPageView.__init__", 
                                   f"Using spawn point from TMX: ({spawn_x}, {spawn_y})", 
                                   spawn_name=chosen_spawn.get('name', 'unnamed'))
                except Exception as e:
                    Logger.debug("MapPageView.__init__", f"No valid spawn points in TMX: {e}")
                    spawn_x, spawn_y = None, None
                
                # Fallback: use position from player_config.json or map center
                if spawn_x is None or spawn_y is None:
                    try:
                        # Try to use position from player config
                        if player_config and 'positions' in player_config:
                            map_pos = player_config['positions'].get('map', {})
                            h_offset = map_pos.get('horizontal_offset', 50)  # percentage
                            v_offset = map_pos.get('vertical_offset', 50)   # percentage
                            spawn_x = int(map_width * h_offset / 100)
                            spawn_y = int(map_height * v_offset / 100)
                            Logger.debug("MapPageView.__init__", 
                                       f"Using player_config fallback position: ({spawn_x}, {spawn_y})")
                        else:
                            # Final fallback: center of map
                            spawn_x = map_width // 2
                            spawn_y = map_height // 2
                            Logger.debug("MapPageView.__init__", 
                                       f"No spawn config found, using map center: ({spawn_x}, {spawn_y})")
                    except Exception as e:
                        spawn_x = map_width // 2
                        spawn_y = map_height // 2
                        Logger.debug("MapPageView.__init__", f"Error getting spawn position: {e}")
                
                if player is not None:
                    # Use provided player to preserve state (drunkenness, etc.)
                    self.johnny = player
                    # Set position to calculated spawn point
                    self.johnny.setX(spawn_x)
                    self.johnny.setY(spawn_y)
                    Logger.debug("MapPageView.__init__", "Using provided player", 
                               name=self.johnny.getName(), 
                               drunkenness=self.johnny.getDrunkenness(),
                               position=(spawn_x, spawn_y))
                else:
                    # Create new player if none provided
                    self.johnny = PlayerModel("Lola Coma", spawn_x, spawn_y)
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.johnny.setSelectedBottle(beer)
                    Logger.debug("MapPageView.__init__", "New player created", 
                               name=self.johnny.getName(),
                               position=(spawn_x, spawn_y))
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                # Don't re-raise - continue with defaults
                # Create minimal player if all else fails
                if not hasattr(self, 'johnny'):
                    self.johnny = PlayerModel("Lola Coma", screen_width // 2, screen_height // 2)
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.johnny.setSelectedBottle(beer)
            
            # === CONTROLLER INITIALIZATION ===
            
            try:
                # Instantiate controller; shop collision rects will be assigned after shop geometry is computed below
                self.controller = PlayerController(self.screen, self.johnny)
                Logger.debug("MapPageView.__init__", "Player controller created (collisions assigned later)")
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === VIEW INITIALIZATION ===
            
            try:
                # Load player config
                try:
                    asset_manager = AssetManager()
                    player_config = asset_manager.load_player_config()
                    Logger.debug("MapPageView.__init__", f"Successfully loaded player_config with {len(player_config.get('actions', {}))} actions")
                except Exception as e:
                    Logger.error("MapPageView.__init__", f"Failed to load player_config: {e}")
                    player_config = None
                
                # Lola in map: small size (2 tiles = 64x64)
                self.player_view = CaracterView("Game/Assets/lola.png", base_name="lola", 
                                               sprite_size=(64, 64),
                                               character_config=player_config,
                                               game_mode="map")
                self.map_view = MapView(self.map)
                
                Logger.debug("MapPageView.__init__", "Character and map views created")
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === TRANSITION STATE ===
            
            self.show_transition_prompt = False
            self.transition_ready = True  # Enable transition immediately
            
            # === SHOP STATE ===
            # Determine shop location by preferring TMX object layers (explicit shop object) then by finding buildings
            try:
                tiles = self.map.tiles
                h = len(tiles)
                w = len(tiles[0]) if h > 0 else 0

                # Check for explicit shop object in object layers
                shop_obj = None
                try:
                    if hasattr(self.map, 'object_layers'):
                        for layer_name, objs in self.map.object_layers.items():
                            for o in objs:
                                props = o.get('properties', {}) or {}
                                name = (o.get('name') or '').lower()
                                otype = (o.get('type') or '').lower()
                                if name == 'shop' or otype == 'shop' or props.get('shop') in ('true', True, '1', 'yes') or props.get('is_shop') in ('true', '1'):
                                    shop_obj = o
                                    break
                            if shop_obj:
                                break
                except Exception as e:
                    Logger.error('MapPageView.__init__', e)

                # If found, use it directly
                if shop_obj:
                    sx = shop_obj['x']
                    sy = shop_obj['y']
                    sw = max(1, int(shop_obj.get('width', self.map.tile_size)))
                    sh = max(1, int(shop_obj.get('height', self.map.tile_size)))
                    # TMX object y is top coordinate; use as-is
                    self.shop_left = sx
                    self.shop_top = sy
                    self.shop_tile_x = self.shop_left // self.map.tile_size
                    self.shop_tile_y = self.shop_top // self.map.tile_size
                    self.shop_tile_width = 3  # 3x3 collision hitbox
                    self.shop_tile_height = 3  # 3x3 collision hitbox
                    # Recalculate pixel dimensions based on 3x3 tile collision
                    self.shop_width = self.shop_tile_width * self.map.tile_size
                    self.shop_height = self.shop_tile_height * self.map.tile_size
                    self.shop_rect_world = pygame.Rect(self.shop_left, self.shop_top, self.shop_width, self.shop_height)
                    # door at bottom center unless door property specified
                    door_w = max(8, self.map.tile_size // 2)
                    door_h = max(8, self.map.tile_size // 2)
                    door_x = self.shop_left + (self.shop_width - door_w) // 2
                    door_y = self.shop_top + self.shop_height - door_h
                    self.shop_door_rect = pygame.Rect(door_x, door_y, door_w, door_h)
                    self.chosen_building = (self.shop_tile_x, self.shop_tile_y, self.shop_tile_x + self.shop_tile_width - 1, self.shop_tile_y + self.shop_tile_height -1)
                    Logger.debug('MapPageView.__init__', 'Using shop object from TMX', shop=self.chosen_building, obj=shop_obj)
                else:
                    # === No explicit object -> use predefined shop positions ===
                    SHOP_ROW = 16
                    SHOP_COLUMNS = [0, 3, 6, 10, 17, 20, 23, 28, 32, 50, 55, 60, 71, 76, 81, 96, 101, 106]
                    
                    # Choose a random shop location from predefined positions
                    chosen_col = random.choice(SHOP_COLUMNS)
                    self.shop_tile_x = chosen_col
                    self.shop_tile_y = SHOP_ROW
                    self.shop_tile_width = 3  # 3x3 hitbox
                    self.shop_tile_height = 3  # 3x3 hitbox
                    
                    self.chosen_building = (self.shop_tile_x, self.shop_tile_y, self.shop_tile_x, self.shop_tile_y)
                    Logger.debug("MapPageView.__init__", "Shop placed at predefined position", 
                               position=(self.shop_tile_x, self.shop_tile_y), 
                               columns=SHOP_COLUMNS)

                # Pixel dimensions
                self.shop_width = self.shop_tile_width * self.map.tile_size
                self.shop_height = self.shop_tile_height * self.map.tile_size
                self.shop_left = self.shop_tile_x * self.map.tile_size
                self.shop_top = self.shop_tile_y * self.map.tile_size
                self.shop_rect_world = pygame.Rect(self.shop_left, self.shop_top, self.shop_width, self.shop_height)

                # Initialize collision rects early to avoid attribute errors during spawn checks
                # Start with structure collision rects from TMX object layers if present
                self.world_collision_rects = []
                
                # === LOAD SHOP FROM OBJECT LAYER ===
                shop_obj = None
                # === LOAD ALL SHOPS FROM OBJECT LAYER ===
                self.shops = []  # List of all shop objects
                self.drink_shop_index = -1  # Index of the drink shop (only this one opens ShopPageView)
                
                try:
                    if hasattr(self.map, 'object_layers') and 'shop' in self.map.object_layers:
                        shop_objs = self.map.object_layers['shop']
                        if shop_objs:
                            # Load all shops
                            for idx, shop_obj in enumerate(shop_objs):
                                try:
                                    shop_data = {
                                        'obj': shop_obj,
                                        'x': int(shop_obj.get('x', 0)),
                                        'y': int(shop_obj.get('y', 0)),
                                        'width': int(shop_obj.get('width', self.map.tile_size * 3)),
                                        'height': int(shop_obj.get('height', self.map.tile_size * 3)),
                                        'name': shop_obj.get('name', f'Shop_{idx}'),
                                        'is_drink_shop': False  # Will be set randomly below
                                    }
                                    self.shops.append(shop_data)
                                    
                                    Logger.debug("MapPageView.__init__", "Shop loaded", 
                                               index=idx, 
                                               name=shop_data['name'])
                                except Exception as e:
                                    Logger.error("MapPageView.__init__", e)
                                    continue
                            
                            # Choose drink shop randomly from all available shops
                            if len(self.shops) > 0:
                                self.drink_shop_index = random.randint(0, len(self.shops) - 1)
                                self.shops[self.drink_shop_index]['is_drink_shop'] = True
                                Logger.debug("MapPageView.__init__", "Randomly selected drink shop", 
                                           total_shops=len(self.shops), 
                                           drink_shop_idx=self.drink_shop_index,
                                           drink_shop_name=self.shops[self.drink_shop_index]['name'])
                            else:
                                Logger.debug("MapPageView.__init__", "No shops available")
                except Exception as e:
                    Logger.error("MapPageView.__init__", e)
                
                # If shops loaded from TMX, use the randomly selected drink shop as primary
                if self.shops and self.drink_shop_index >= 0:
                    drink_shop = self.shops[self.drink_shop_index]
                    self.shop_left = drink_shop['x']
                    self.shop_top = drink_shop['y']
                    self.shop_width = drink_shop['width']
                    self.shop_height = drink_shop['height']
                    self.shop_tile_x = self.shop_left // self.map.tile_size
                    self.shop_tile_y = self.shop_top // self.map.tile_size
                    self.shop_tile_width = (self.shop_left + self.shop_width) // self.map.tile_size - self.shop_tile_x
                    self.shop_tile_height = (self.shop_top + self.shop_height) // self.map.tile_size - self.shop_tile_y
                    self.shop_rect_world = pygame.Rect(self.shop_left, self.shop_top, self.shop_width, self.shop_height)
                    
                    # Door at bottom center
                    door_w = max(8, self.map.tile_size // 2)
                    door_h = max(8, self.map.tile_size // 2)
                    door_x = self.shop_left + (self.shop_width - door_w) // 2
                    door_y = self.shop_top + self.shop_height - door_h
                    self.shop_door_rect = pygame.Rect(door_x, door_y, door_w, door_h)
                    self.chosen_building = (self.shop_tile_x, self.shop_tile_y, self.shop_tile_x + self.shop_tile_width - 1, self.shop_tile_y + self.shop_tile_height - 1)
                    
                    Logger.debug('MapPageView.__init__', 'Using drink shop from TMX', shop=drink_shop['name'])
                    
                    # Add all shops to world collisions
                    for shop in self.shops:
                        rect = pygame.Rect(shop['x'], shop['y'], shop['width'], shop['height'])
                        self.world_collision_rects.append(rect)
                else:
                    # === No explicit objects -> use predefined shop positions ===
                    SHOP_ROW = 16
                    SHOP_COLUMNS = [0, 3, 6, 10, 17, 20, 23, 28, 32, 50, 55, 60, 71, 76, 81, 96, 101, 106]
                    
                    # Choose a random shop location from predefined positions
                    chosen_col = random.choice(SHOP_COLUMNS)
                    self.shop_tile_x = chosen_col
                    self.shop_tile_y = SHOP_ROW
                    self.shop_tile_width = 3  # 3x3 hitbox
                    self.shop_tile_height = 3  # 3x3 hitbox
                    
                    self.chosen_building = (self.shop_tile_x, self.shop_tile_y, self.shop_tile_x, self.shop_tile_y)
                    Logger.debug("MapPageView.__init__", "Shop placed at predefined position", 
                               position=(self.shop_tile_x, self.shop_tile_y), 
                               columns=SHOP_COLUMNS)

                    # Pixel dimensions
                    self.shop_width = self.shop_tile_width * self.map.tile_size
                    self.shop_height = self.shop_tile_height * self.map.tile_size
                    self.shop_left = self.shop_tile_x * self.map.tile_size
                    self.shop_top = self.shop_tile_y * self.map.tile_size
                    self.shop_rect_world = pygame.Rect(self.shop_left, self.shop_top, self.shop_width, self.shop_height)
                    self.world_collision_rects.append(self.shop_rect_world)
                
                # === LOAD COLLISIONS FROM OBJECT LAYERS ===
                # Add objects from "ville" layer (buildings collisions)
                try:
                    if hasattr(self.map, 'object_layers') and 'ville' in self.map.object_layers:
                        for obj in self.map.object_layers['ville']:
                            try:
                                r = pygame.Rect(int(obj['x']), int(obj['y']), int(obj['width']), int(obj['height']))
                                self.world_collision_rects.append(r)
                                Logger.debug("MapPageView.__init__", "Added ville collision", rect=r)
                            except Exception:
                                continue
                except Exception as e:
                    Logger.error("MapPageView.__init__", e)

                # Door -- place at bottom center of the building if not already set by object
                door_w = max(8, self.map.tile_size // 2)
                door_h = max(8, self.map.tile_size // 2)
                door_x = self.shop_left + (self.shop_width - door_w) // 2
                door_y = self.shop_top + self.shop_height - door_h
                self.shop_door_rect = pygame.Rect(door_x, door_y, door_w, door_h)

                # After computing shop geometry, force window size to map pixel dim to avoid scaling artifacts
                try:
                    map_pixel_width = len(self.map.tiles[0]) * self.map.tile_size if self.map.tiles else screen_width
                    map_pixel_height = len(self.map.tiles) * self.map.tile_size if self.map.tiles else screen_height
                    # Use PageView helper to set window size and keep resizable flag as configured
                    self.set_window_size(map_pixel_width, map_pixel_height, self.resizable)
                    Logger.debug("MapPageView.__init__", "Window resized to map dimensions", width=map_pixel_width, height=map_pixel_height)
                except Exception as e:
                    Logger.error("MapPageView.__init__", e)

                # Ensure player spawn not inside blocking collision rects
                try:
                    half = self.controller.PLAYER_SIZE // 2 if hasattr(self, 'controller') else 25
                    px = int(self.johnny.getX())
                    py = int(self.johnny.getY())
                    player_rect = pygame.Rect(px - half, py - half, half*2, half*2)
                    for r in self.world_collision_rects:
                        if player_rect.colliderect(r):
                            # move player above collision
                            new_y = r.top - half - 10
                            self.johnny.setY(new_y)
                            Logger.debug("MapPageView.__init__", "Player repositioned to avoid spawn inside collision", new_y=new_y)
                            break
                except Exception as e:
                    Logger.error("MapPageView.__init__", e)
                # Collision rects: left and right of the door (blocking building body) - also add to world_collision_rects
                left_width = (self.shop_width - door_w) // 2
                right_x = door_x + door_w
                right_width = self.shop_width - left_width - door_w

                self.shop_collision_rects = [
                    pygame.Rect(self.shop_left, self.shop_top, left_width, self.shop_height),
                    pygame.Rect(right_x, self.shop_top, right_width, self.shop_height),
                ]

                # Always include building body collisions in world collision set
                for r in self.shop_collision_rects:
                    self.world_collision_rects.append(r)

                Logger.debug("MapPageView.__init__", "Shop geometry determined", tile_rect=(self.shop_tile_x, self.shop_tile_y, self.shop_tile_width, self.shop_tile_height), world_rect=self.shop_rect_world, world_collisions=len(self.world_collision_rects))

            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                # Fallback
                self.world_collision_rects = []  # Initialize collision rects list
                self.shops = []  # Initialize shops list
                self.shop_tile_x = 18
                self.shop_tile_y = 8
                self.shop_tile_width = 3
                self.shop_tile_height = 3
                self.shop_left = self.shop_tile_x * self.map.tile_size
                self.shop_top = self.shop_tile_y * self.map.tile_size
                self.shop_width = self.shop_tile_width * self.map.tile_size
                self.shop_height = self.shop_tile_height * self.map.tile_size
                self.shop_rect_world = pygame.Rect(self.shop_left, self.shop_top, self.shop_width, self.shop_height)
                door_w = self.map.tile_size // 2
                door_h = self.map.tile_size // 2
                door_x = self.shop_left + (self.shop_width - door_w) // 2
                door_y = self.shop_top + self.shop_height - door_h
                self.shop_door_rect = pygame.Rect(door_x, door_y, door_w, door_h)
                self.shop_collision_rects = [self.shop_rect_world]

            self.near_shop = False
            self.show_shop_prompt = False

            # Simple cooldown to avoid re-entering shop every frame when overlapping the door
            self._shop_cooldown_frames = 0

            # Debug overlay toggle (press F1 in-map to toggle)
            self.show_debug_overlay = False
            Logger.debug("MapPageView.__init__", "Shop & map debug", shop_rect=self.shop_rect_world, door_rect=self.shop_door_rect, tile_size=self.map.tile_size, map_size=(getattr(self.map,'width',None), getattr(self.map,'height',None)))

# Assign world collision rects to player controller now that they exist
            try:
                if hasattr(self, 'controller') and self.controller is not None:
                    self.controller.collision_rects = self.world_collision_rects
                    Logger.debug("MapPageView.__init__", "Assigned world collision rects to PlayerController", collisions=len(self.world_collision_rects))
            except Exception as e:
                Logger.error("MapPageView.__init__", e)

            # Shop enter delay counters (frames)
            self._shop_enter_counter = 0
            self._shop_enter_frames_required = 45  # ~0.75s at 60fps
            
        except Exception as e:
            Logger.error("MapPageView.__init__", e)
            raise
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main game loop for the map page view.
        Handles events, updates game state, and renders the map.
        Returns a string indicating the next view (GameState values): "ACT1", "ACT2", "RHYTHM", or "QUIT".
        """
        try:
            clock = pygame.time.Clock()
            running = True
            transition_triggered = False
            Logger.debug("MapPageView.run", "Map page loop started", current_act=self.current_act)
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    events = pygame.event.get()

                    for event in events:
                        if event.type == pygame.QUIT:
                            Logger.debug("MapPageView.run", "QUIT event received")
                            return GameState.QUIT.value
                        
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.set_window_size(new_width, new_height, self.resizable)
                                Logger.debug("MapPageView.run", "Window resized", 
                                          width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("MapPageView.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                            # === HANDLE F11 FOR FULLSCREEN TOGGLE ===
                            if event.key == pygame.K_F11:
                                try:
                                    self._toggle_fullscreen()
                                except Exception as e:
                                    Logger.error("MapPageView.run", e)
                            # === HANDLE NUMERIC KEYS (1-8) FOR STAGE NAVIGATION ===
                            if self.sequence_controller and event.key >= pygame.K_1 and event.key <= pygame.K_8:
                                stage_number = event.key - pygame.K_1 + 1  # Convert to 1-8
                                if self.sequence_controller.handle_numeric_input(stage_number):
                                    Logger.debug("MapPageView.run", "Navigation to stage requested", 
                                               stage=stage_number, 
                                               stage_name=self.sequence_controller.get_current_stage_name())
                                    # Return a special code to indicate stage change
                                    return f"STAGE_{stage_number}"
                            
                            # Toggle debug overlay
                            if event.key == pygame.K_F1:
                                try:
                                    self.show_debug_overlay = not getattr(self, 'show_debug_overlay', False)
                                    Logger.debug('MapPageView.run', 'Toggled debug overlay', show=self.show_debug_overlay)
                                except Exception as e:
                                    Logger.error('MapPageView.run', e)

                            # Check for pause menu (ESC)
                            if event.key == pygame.K_ESCAPE:
                                # Open pause menu
                                try:
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()

                                    if pause_result == GameState.QUIT.value:
                                        Logger.debug("MapPageView.run", "Quit requested from pause menu")
                                        return GameState.QUIT.value
                                    elif pause_result == GameState.MAIN_MENU.value:
                                        Logger.debug("MapPageView.run", "Main menu requested from pause menu")
                                        return GameState.MAIN_MENU.value
                                    elif pause_result == GameState.CONTINUE.value:
                                        Logger.debug("MapPageView.run", "Resuming from pause menu")
                                    else:
                                        Logger.debug("MapPageView.run", "Resuming from pause menu (default)")
                                except Exception as e:
                                    Logger.error("MapPageView.run", e)

                            # Enter drink shop if near door and press E
                            elif event.key == pygame.K_e:
                                try:
                                    # Respect shop cooldown
                                    if getattr(self, '_shop_cooldown_frames', 0) > 0:
                                        Logger.debug("MapPageView.run", "E pressed but shop cooldown active", frames=self._shop_cooldown_frames)
                                    else:
                                        px = int(self.johnny.getX())
                                        py = int(self.johnny.getY())
                                        # Player rectangle (centered on player's coordinates)
                                        half = 25
                                        player_rect = pygame.Rect(px - half, py - half, half * 2, half * 2)
                                        
                                        # Check if near drink shop door
                                        if self.shops and self.drink_shop_index >= 0:
                                            drink_shop = self.shops[self.drink_shop_index]
                                            door_w = max(8, self.map.tile_size // 2)
                                            door_h = max(8, self.map.tile_size // 2)
                                            door_x = drink_shop['x'] + (drink_shop['width'] - door_w) // 2
                                            door_y = drink_shop['y'] + drink_shop['height'] - door_h
                                            door_rect = pygame.Rect(door_x, door_y, door_w, door_h)
                                            
                                            try:
                                                infl_w = int(self.map.tile_size * 1.5)
                                                infl_h = int(self.map.tile_size * 1.0)
                                                door_hit = door_rect.inflate(infl_w, infl_h)
                                            except Exception:
                                                door_hit = door_rect
                                            
                                            if player_rect.colliderect(door_hit):
                                                Logger.debug("MapPageView.run", "Entering drink shop via door (collision)", player=(px, py))
                                                shop_result = self._run_shop()
                                                if shop_result == GameState.QUIT.value:
                                                    return GameState.QUIT.value
                                            else:
                                                Logger.debug("MapPageView.run", "E pressed but player not colliding with drink shop door", player=(px, py))
                                except Exception as e:
                                    Logger.error("MapPageView.run", e)
                            
                            # Launch act if transition is ready and press SPACE
                            elif event.key == pygame.K_SPACE:
                                if self.transition_ready:
                                    Logger.debug("MapPageView.run", "Transition triggered by SPACE", next_act=self.current_act)
                                    transition_triggered = True
                                    running = False
                                    break
                            
                            # TEST: Press P to add money
                            elif event.key == pygame.K_p:
                                try:
                                    amount = 1000
                                    self.johnny.addCurrency(amount)
                                    new_money = self.johnny.getCurrency()
                                    Logger.debug("MapPageView.run", "Money added for testing", amount=amount, total=new_money)
                                except Exception as e:
                                    Logger.error("MapPageView.run.test_money", e)

                        # Handle mouse click on transition prompt or shop
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:  # Left click
                                mouse_x, mouse_y = event.pos
                                
                                # Check if click is on transition prompt area
                                if self.transition_ready:
                                    prompt_width = 400
                                    prompt_height = 100
                                    prompt_x = (self.screen.get_width() - prompt_width) // 2
                                    prompt_y = self.screen.get_height() - 150
                                    
                                    if (prompt_x <= mouse_x <= prompt_x + prompt_width and
                                        prompt_y <= mouse_y <= prompt_y + prompt_height):
                                        Logger.debug("MapPageView.run", "Transition triggered by click", next_act=self.current_act)
                                        transition_triggered = True
                                        running = False
                                        break
                                
                                # Check if click is on shop building
                                shop_left = self.shop_tile_x * self.map.tile_size
                                shop_right = (self.shop_tile_x + self.shop_tile_width) * self.map.tile_size
                                shop_top = self.shop_tile_y * self.map.tile_size
                                shop_bottom = (self.shop_tile_y + self.shop_tile_height) * self.map.tile_size

                                if (shop_left <= mouse_x <= shop_right and
                                    shop_top <= mouse_y <= shop_bottom):
                                    # Open shop on click (respect cooldown)
                                    try:
                                        if getattr(self, '_shop_cooldown_frames', 0) > 0:
                                            Logger.debug('MapPageView.run', 'Click on shop ignored due to cooldown', frames=self._shop_cooldown_frames)
                                        else:
                                            shop_model = ShopModel(self.johnny)
                                            shop_view = ShopPageView(self.screen, shop_model)
                                            shop_controller = ShopController(shop_model, shop_view)
                                            
                                            # Shop loop
                                            shop_running = True
                                            shop_clock = pygame.time.Clock()
                                            
                                            while shop_running:
                                                for shop_event in pygame.event.get():
                                                    if shop_event.type == pygame.QUIT:
                                                        shop_running = False
                                                        return GameState.QUIT.value
                                                    
                                                    result = shop_controller.handleInput(shop_event)
                                                    if result == "exit":
                                                        shop_running = False
                                                        Logger.debug("MapPageView.run", "Shop closed")
                                                
                                                shop_controller.update()
                                                shop_view.draw(self.johnny)
                                                pygame.display.flip()
                                                shop_clock.tick(60)
                                            
                                            Logger.debug("MapPageView.run", "Returned from shop")
                                    except Exception as e:
                                        Logger.error("MapPageView.run", e)

                    # === PLAYER CONTROLLER UPDATE (continuous movement) ===
                    try:
                        self.controller.handle_events(events)
                    except Exception as e:
                        Logger.error("MapPageView.run", e)

                    # === UPDATE ===
                    
                    # Check if player is near shop (within 2 tiles distance)
                    try:
                        player_x = self.johnny.getX()
                        player_y = self.johnny.getY()
                        
                        # Check if player is near the drink shop (proximity-based prompts)
                        try:
                            self.near_shop = False
                            self.show_shop_prompt = False
                            
                            if self.shops and self.drink_shop_index >= 0:
                                drink_shop = self.shops[self.drink_shop_index]
                                shop_area = pygame.Rect(drink_shop['x'], drink_shop['y'], drink_shop['width'], drink_shop['height'])
                                interaction_range = self.map.tile_size * 2
                                shop_area_expanded = shop_area.inflate(interaction_range, interaction_range)
                                
                                if shop_area_expanded.collidepoint((player_x, player_y)):
                                    self.near_shop = True
                                    # Show prompt only when player is near the door specifically (more forgiving)
                                    try:
                                        door_w = max(8, self.map.tile_size // 2)
                                        door_h = max(8, self.map.tile_size // 2)
                                        door_x = drink_shop['x'] + (drink_shop['width'] - door_w) // 2
                                        door_y = drink_shop['y'] + drink_shop['height'] - door_h
                                        door_rect = pygame.Rect(door_x, door_y, door_w, door_h)
                                        
                                        infl_w = int(self.map.tile_size * 1.5)
                                        infl_h = int(self.map.tile_size * 1.0)
                                        if door_rect.inflate(infl_w, infl_h).collidepoint((player_x, player_y)):
                                            self.show_shop_prompt = True
                                        else:
                                            self.show_shop_prompt = False
                                    except Exception:
                                        self.show_shop_prompt = False
                        except Exception as e:
                            Logger.error("MapPageView.run.proximity_check", e)
                            self.near_shop = False
                            self.show_shop_prompt = False

                        # Check collision with any shop door
                        try:
                            half = 25
                            player_rect = pygame.Rect(int(player_x) - half, int(player_y) - half, half * 2, half * 2)
                            
                            # Check if colliding with drink shop door specifically
                            if self.shops and self.drink_shop_index >= 0:
                                drink_shop = self.shops[self.drink_shop_index]
                                door_w = max(8, self.map.tile_size // 2)
                                door_h = max(8, self.map.tile_size // 2)
                                door_x = drink_shop['x'] + (drink_shop['width'] - door_w) // 2
                                door_y = drink_shop['y'] + drink_shop['height'] - door_h
                                shop_door_rect = pygame.Rect(door_x, door_y, door_w, door_h)
                                
                                try:
                                    infl_w = int(self.map.tile_size * 1.5)
                                    infl_h = int(self.map.tile_size * 1.0)
                                    door_hit = shop_door_rect.inflate(infl_w, infl_h)
                                except Exception:
                                    door_hit = shop_door_rect
                                
                                if getattr(self, '_shop_cooldown_frames', 0) == 0:
                                    if player_rect.colliderect(door_hit):
                                        # Increment counter while touching the door; require sustained contact
                                        self._shop_enter_counter = getattr(self, '_shop_enter_counter', 0) + 1
                                        Logger.debug('MapPageView.run', 'Player at drink shop door', counter=self._shop_enter_counter)
                                        if self._shop_enter_counter >= getattr(self, '_shop_enter_frames_required', 45):
                                            Logger.debug("MapPageView.run", "Player dwell reached - auto-entering drink shop", player=(player_x, player_y))
                                            shop_result = self._run_shop()
                                            # Apply longer cooldown (10s) to prevent immediate re-opening
                                            self._shop_cooldown_frames = 60 * 10
                                            self._shop_enter_counter = 0
                                            if shop_result == GameState.QUIT.value:
                                                return GameState.QUIT.value
                                    else:
                                        # Reset if player moves away
                                        self._shop_enter_counter = 0
                        except Exception as e:
                            Logger.error("MapPageView.run", e)
                    except Exception as e:
                        Logger.error("MapPageView.run", e)
                    
                    # Show transition prompt if ready
                    if self.transition_ready and not self.show_transition_prompt:
                        self.show_transition_prompt = True
                        Logger.debug("MapPageView.run", "Transition prompt shown")
                    
                    # === RENDERING ===
                    
                    try:
                        # Draw background first
                        self.draw()

                        # Calculate camera position to follow player
                        try:
                            player_x = int(self.johnny.getX())
                            player_y = int(self.johnny.getY())
                            
                            screen_w = self.screen.get_width()
                            screen_h = self.screen.get_height()
                            
                            # Center camera on player
                            camera_x = player_x - screen_w // 2
                            camera_y = player_y - screen_h // 2
                            
                            # Clamp camera to map boundaries
                            if hasattr(self.map, 'tiles') and self.map.tiles:
                                map_width = len(self.map.tiles[0]) * self.map.tile_size if len(self.map.tiles) > 0 else 0
                                map_height = len(self.map.tiles) * self.map.tile_size
                                
                                camera_x = max(0, min(camera_x, map_width - screen_w))
                                camera_y = max(0, min(camera_y, map_height - screen_h))
                            
                            # Apply camera offset (negative to translate the world towards screen origin)
                            camera_offset = (-camera_x, -camera_y)
                        except Exception as e:
                            Logger.error("MapPageView.camera", e)
                            camera_offset = (0, 0)
                        
                        # Draw map and objects with camera following player
                        try:
                            self.map_view.draw(self.screen, camera_offset)
                            self._drawShopBuilding(camera_offset)
                            self.player_view.drawCaracter(self.screen, self.johnny, offset=camera_offset, is_map=True)
                        except Exception as e:
                            Logger.error("MapPageView.render.draw", e)

# Marker: show shop positions on map
                        try:
                            # Draw all shops (different colors)
                            for shop_idx, shop in enumerate(self.shops):
                                try:
                                    shop_left = shop['x']
                                    shop_top = shop['y']
                                    is_drink = shop['is_drink_shop']
                                    
                                    # Apply camera offset to shop center
                                    shop_center_world_x = int(shop_left + shop['width'] // 2)
                                    shop_center_world_y = int(shop_top + shop['height'] // 2)
                                    shop_center = (shop_center_world_x + camera_offset[0], shop_center_world_y + camera_offset[1])
                                    
                                    # Only draw if visible on screen
                                    if -50 < shop_center[0] < screen_w + 50 and -50 < shop_center[1] < screen_h + 50:
                                        try:
                                            # Draw appropriate label
                                            try:
                                                font = pygame.font.SysFont('Arial', 12, bold=True)
                                            except Exception:
                                                font = pygame.font.Font(None, 12)
                                            
                                            if is_drink:
                                                label_text = 'OPEN'
                                                label_color = (100, 255, 100)  # Green for open
                                            else:
                                                label_text = 'CLOSED'
                                                label_color = (255, 100, 100)  # Red for closed
                                            
                                            label = font.render(label_text, True, label_color)
                                            
                                            # Draw label without background
                                            lbl_x = shop_center[0] - label.get_width()//2
                                            lbl_y = shop_center[1] - shop['height']//2 - label.get_height() - 4
                                            self.screen.blit(label, (lbl_x, lbl_y))
                                        except Exception:
                                            pass
                                except Exception as e:
                                    Logger.error("MapPageView.run.shop_marker", e)
                            
                            Logger.debug("MapPageView.run", "Shop markers drawn", total_shops=len(self.shops))
                        except Exception as e:
                            Logger.error("MapPageView.debugPositions", e)

                        # Draw shop prompt (door-specific)
                        if self.show_shop_prompt:
                            self.drawShopPrompt()

                        # Draw transition prompt
                        if self.show_transition_prompt:
                            self.drawTransitionPrompt()
                        
                        # Draw level display
                        try:
                            self._drawLevelDisplay()
                        except Exception as e:
                            Logger.error("MapPageView.run", e)

                        # Draw debug overlay if enabled
                        try:
                            if getattr(self, 'show_debug_overlay', False):
                                try:
                                    font = pygame.font.SysFont('Consolas', 14)
                                except Exception:
                                    font = pygame.font.Font(None, 14)
                                lines = []
                                lines.append(f'tile_size={self.map.tile_size} map={getattr(self.map, "width",None)}x{getattr(self.map,"height",None)}')
                                lines.append(f'map_pixels={len(self.map.tiles[0])*self.map.tile_size}x{len(self.map.tiles)*self.map.tile_size}')
                                lines.append(f'shop_rect={self.shop_rect_world}')
                                lines.append(f'shop_door={self.shop_door_rect}')
                                px, py = int(self.johnny.getX()), int(self.johnny.getY())
                                lines.append(f'player=({px},{py})')
                                lines.append(f'shop_collision_count={len(getattr(self, "shop_collision_rects", []))}')
                                y0 = 10
                                for ln in lines:
                                    surf = font.render(ln, True, (255,255,255))
                                    self.screen.blit(surf, (10, y0))
                                    y0 += surf.get_height() + 2
                        except Exception as e:
                            Logger.error('MapPageView.debugOverlay', e)
                    except Exception as e:
                        Logger.error("MapPageView.render", e)

                    # Decrement shop cooldown
                    try:
                        if self._shop_cooldown_frames > 0:
                            self._shop_cooldown_frames -= 1
                    except Exception:
                        pass

                    # Present the frame
                    pygame.display.flip()
                    clock.tick(60)
                except Exception as e:
                    Logger.error("MapPageView.run", e)
                    return GameState.QUIT.value
            if transition_triggered:
                # === DETERMINE NEXT VIEW ===
                try:
                    if self.current_act == 1:
                        Logger.debug("MapPageView.run", "Transitioning to Act 1")
                        return GameState.ACT1.value
                    elif self.current_act == 2:
                        Logger.debug("MapPageView.run", "Transitioning to Act 2")
                        return GameState.ACT2.value
                    elif self.current_act == 3:
                        Logger.debug("MapPageView.run", "Transitioning to Rhythm")
                        return GameState.RHYTHM.value
                    else:
                        Logger.debug("MapPageView.run", "No more acts, returning to menu")
                        return GameState.QUIT.value
                except Exception as e:
                    Logger.error("MapPageView.run", e)
                    return GameState.QUIT.value
            else:
                # Loop exited without transition (shouldn't happen normally)
                Logger.debug("MapPageView.run", "Loop exited without transition")
                return GameState.QUIT.value
        except Exception as e:
            Logger.error("MapPageView.run", e)
            return GameState.QUIT.value

    def drawTransitionPrompt(self):
        """
        Draws the transition prompt on screen.
        Shows which act the player can access next.
        """
        try:
            # Font setup
            try:
                font = pygame.font.SysFont("Arial", 24, bold=True)
                small_font = pygame.font.SysFont("Arial", 18)
            except Exception as e:
                Logger.error("MapPageView.drawTransitionPrompt", e)
                font = pygame.font.Font(None, 24)
                small_font = pygame.font.Font(None, 18)
            
            # Determine act name
            if self.current_act == 1:
                act_name = "ACT I : THE DRY THROAT"
            elif self.current_act == 2:
                act_name = "ACT II : WOOD-STOCK-OPTION"
            elif self.current_act == 3:
                act_name = "FINAL RHYTHM SEQUENCE"
            else:
                act_name = "UNKNOWN ACT"
            
            # Draw prompt background
            prompt_width = 400
            prompt_height = 100
            prompt_x = (self.screen.get_width() - prompt_width) // 2
            prompt_y = self.screen.get_height() - 150
            
            try:
                # Semi-transparent background
                prompt_surface = pygame.Surface((prompt_width, prompt_height))
                prompt_surface.set_alpha(200)
                prompt_surface.fill((0, 0, 0))
                self.screen.blit(prompt_surface, (prompt_x, prompt_y))
                
                # Draw border
                pygame.draw.rect(self.screen, (255, 215, 0), 
                               (prompt_x, prompt_y, prompt_width, prompt_height), 3)
                
                # Draw text
                act_text = font.render(act_name, True, (255, 215, 0))
                act_x = prompt_x + (prompt_width - act_text.get_width()) // 2
                act_y = prompt_y + 20
                self.screen.blit(act_text, (act_x, act_y))
                
                instruction = "Press SPACE to continue"
                inst_text = small_font.render(instruction, True, (200, 200, 200))
                inst_x = prompt_x + (prompt_width - inst_text.get_width()) // 2
                inst_y = prompt_y + 60
                self.screen.blit(inst_text, (inst_x, inst_y))
            except Exception as e:
                Logger.error("MapPageView.drawTransitionPrompt", e)
                
        except Exception as e:
            Logger.error("MapPageView.drawTransitionPrompt", e)
    
    def drawShopPrompt(self):
        """
        Draws the shop entry prompt on screen.
        Shows when player is near the shop building.
        """
        try:
            # Font setup
            try:
                font = pygame.font.SysFont("Arial", 24, bold=True)
                small_font = pygame.font.SysFont("Arial", 18)
            except Exception as e:
                Logger.error("MapPageView.drawShopPrompt", e)
                font = pygame.font.Font(None, 24)
                small_font = pygame.font.Font(None, 18)
            
            # Draw prompt background
            prompt_width = 300
            prompt_height = 80
            prompt_x = (self.screen.get_width() - prompt_width) // 2
            prompt_y = 50  # Top of screen
            
            try:
                # Semi-transparent background
                prompt_surface = pygame.Surface((prompt_width, prompt_height), pygame.SRCALPHA)
                prompt_surface.fill((0, 0, 0, 180))  # Black with 180 alpha
                pygame.draw.rect(prompt_surface, (255, 215, 0), (0, 0, prompt_width, prompt_height), 3, border_radius=10)
                self.screen.blit(prompt_surface, (prompt_x, prompt_y))
            except Exception as e:
                Logger.error("MapPageView.drawShopPrompt", e)

            # Draw text
            try:
                title_surf = font.render("SHOP", True, (0, 0, 0))
                instruction_surf = small_font.render("Press E to enter shop", True, (0, 0, 0))
                
                self.screen.blit(title_surf, (prompt_x + (prompt_width - title_surf.get_width()) // 2, prompt_y + 15))
                self.screen.blit(instruction_surf, (prompt_x + (prompt_width - instruction_surf.get_width()) // 2, prompt_y + 50))
            except Exception as e:
                Logger.error("MapPageView.drawShopPrompt", e)
        except Exception as e:
            Logger.error("MapPageView.drawShopPrompt", e)

    def _run_shop(self):
        """
        Blocking loop to handle shop interaction. Returns GameState.QUIT.value if quit requested, else None.
        """
        try:
            clock = pygame.time.Clock()
            shop_model = ShopModel(self.johnny)
            shop_view = ShopPageView(self.screen, shop_model)
            shop_controller = ShopController(shop_model, shop_view)

            in_shop = True
            Logger.debug("MapPageView._run_shop", "Shop interaction started")
            while in_shop:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        Logger.debug("MapPageView._run_shop", "QUIT received in shop")
                        return GameState.QUIT.value
                    # Let shop controller handle inputs
                    try:
                        res = shop_controller.handle_input(event)
                        if res == "exit":
                            in_shop = False
                            Logger.debug("MapPageView._run_shop", "Exit requested from shop")
                            break
                    except Exception as e:
                        Logger.error("MapPageView._run_shop", e)

                try:
                    shop_view.draw(self.johnny)
                except Exception as e:
                    Logger.error("MapPageView._run_shop.draw", e)

                pygame.display.flip()
                clock.tick(60)

            # Apply cooldown after leaving shop to avoid immediate re-opening (10 seconds @ 60fps)
            try:
                self._shop_cooldown_frames = 60 * 10
                Logger.debug("MapPageView._run_shop", "Applied shop exit cooldown", frames=self._shop_cooldown_frames)
            except Exception:
                pass
            Logger.debug("MapPageView._run_shop", "Shop interaction ended")
            return None
        except Exception as e:
            Logger.error("MapPageView._run_shop", e)
            return None

    def _drawShopBuilding(self, offset=(0, 0)):
        """
        Draw the shop building on the map as a visual indicator.
        The shop is drawn on specific tiles of the map. Accepts a camera offset (dx, dy)
        to draw in screen coordinates.
        """
        try:
            dx, dy = offset
            # Calculate shop position based on tile coordinates and camera offset
            shop_left = self.shop_tile_x * self.map.tile_size + dx
            shop_top = self.shop_tile_y * self.map.tile_size + dy

            # Draw the door as a visible opening (screen coords)
            try:
                door_rect_screen = pygame.Rect(self.shop_door_rect.x + dx, self.shop_door_rect.y + dy, self.shop_door_rect.width, self.shop_door_rect.height)
                # Draw a slightly larger bright outline and a dark center so it's visible on any background
                outline_rect = door_rect_screen.inflate(6, 6)
                try:
                    # Hidden: don't draw the yellow shop access square
                    # pygame.draw.rect(self.screen, (255, 215, 0), outline_rect)  # bright outline
                    # pygame.draw.rect(self.screen, (40, 40, 40), door_rect_screen)  # dark door
                    pass
                except Exception:
                    # Drawing might fail if screen/surface invalid
                    pass

                # If player is near, draw a subtle glow
                try:
                    if getattr(self, 'show_shop_prompt', False):
                        glow_rect = door_rect_screen.inflate(self.map.tile_size // 2, self.map.tile_size // 2)
                        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                        glow_surf.fill((255, 215, 0, 80))
                        self.screen.blit(glow_surf, (glow_rect.x, glow_rect.y))
                except Exception:
                    pass

                # Optional small label for clarity
                try:
                    door_font = pygame.font.SysFont("Arial", 12)
                    door_text = door_font.render("E", True, (255, 255, 255))
                    self.screen.blit(door_text, (door_rect_screen.x + (door_rect_screen.width - door_text.get_width())//2, door_rect_screen.y - door_text.get_height() - 2))
                except Exception:
                    pass

            except Exception as e:
                Logger.error("MapPageView._drawShopDoor", e)
        
        except Exception as e:
            Logger.error("MapPageView._drawShopBuilding", e)
    
    def _drawLevelDisplay(self):
        """
        Draw the level display in the bottom left corner.
        """
        try:
            font = pygame.font.Font(None, 36)
            level = self.johnny.getLevel() if hasattr(self.johnny, 'getLevel') else 1
            level_text = font.render(f"LEVEL {level}", True, (0, 255, 0))
            
            # Draw black rectangle background
            text_x = 20
            text_y = self.screen.get_height() - 50
            bg_rect = pygame.Rect(text_x - 5, text_y - 5, level_text.get_width() + 10, level_text.get_height() + 10)
            pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
            
            self.screen.blit(level_text, (text_x, text_y))
            
            # Draw Alcohol level above the level display
            try:
                alcohol = self.johnny.getDrunkenness() if hasattr(self.johnny, 'getDrunkenness') else 0
                alcohol_text = font.render(f"Alcohol: {alcohol}%", True, (0, 255, 0))
                alcohol_x = text_x
                alcohol_y = text_y - alcohol_text.get_height() - 10
                bg_rect_alcohol = pygame.Rect(alcohol_x - 5, alcohol_y - 5, alcohol_text.get_width() + 10, alcohol_text.get_height() + 10)
                pygame.draw.rect(self.screen, (0, 0, 0), bg_rect_alcohol)
                self.screen.blit(alcohol_text, (alcohol_x, alcohol_y))
            except Exception:
                pass
        except Exception as e:
            Logger.error("MapPageView._drawLevelDisplay", e)
    
    def _toggle_fullscreen(self):
        """Toggle between fullscreen and resizable window modes."""
        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
                # Currently fullscreen, switch to resizable
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height),
                    pygame.RESIZABLE
                )
                Logger.debug("MapPageView._toggle_fullscreen", "Switched to RESIZABLE mode")
            else:
                # Currently resizable, switch to fullscreen
                screen_info = pygame.display.Info()
                self.screen = pygame.display.set_mode(
                    (screen_info.current_w, screen_info.current_h),
                    pygame.FULLSCREEN
                )
                self.screen_width = screen_info.current_w
                self.screen_height = screen_info.current_h
                Logger.debug("MapPageView._toggle_fullscreen", "Switched to FULLSCREEN mode")
        except Exception as e:
            Logger.error("MapPageView._toggle_fullscreen", e)
