"""
MapPageView Module

Handles the interactive map view between game acts.
Allows player navigation and transitions to different acts.
"""

import pygame
from Views.PageView import PageView
from Views.MapView import MapView
from Views.CaracterView import CaracterView
from Views.PauseMenuView import PauseMenuView
from Views.ShopPageView import ShopPageView
from Controllers.PlayerController import PlayerController
from Controllers.ShopController import ShopController
from Models.ShopModel import ShopModel
from Models.PlayerModel import PlayerModel
from Models.MapModel import MapModel
from Models.TileModel import TileModel
from Models.BottleModel import BottleModel
from Utils.Logger import Logger


# === MAP PAGE VIEW CLASS ===

class MapPageView(PageView):
    """
    Interactive map view for navigation between acts.
    Displays the map, player character, and handles transitions to acts.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, current_act=1, player=None):
        """
        Initialize the map page view.
        
        Args:
            screen: Pygame display surface
            current_act: Current act number (1 = Act 1, 2 = Act 2, 3 = Rhythm)
            player: Optional PlayerModel instance to preserve state (if None, creates new)
        """
        try:
            # Get screen dimensions
            screen_width = screen.get_width()
            screen_height = screen.get_height()
            
            # Initialize PageView
            super().__init__("Map - Six-String Hangover", screen_width, screen_height, pygame.RESIZABLE, "Game/Assets/welcomePage.png")
            self.screen = screen
            self.current_act = current_act
            
            Logger.debug("MapPageView.__init__", "Map page view initialized", 
                        current_act=current_act, 
                        width=screen_width, 
                        height=screen_height)
            
            # === MAP INITIALIZATION ===
            
            try:
                tile_kinds = [
                    TileModel("road", "Game/Assets/road3_carre.png", False),
                    TileModel("road2", "Game/Assets/road3_carre.png", False)
                ]
                self.map = MapModel("Game/Assets/maps/map.map", tile_kinds, 106)
                Logger.debug("MapPageView.__init__", "Map created")
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === PLAYER INITIALIZATION ===
            
            try:
                # Calculate map center for player spawn
                map_width = len(self.map.tiles[0]) * self.map.tile_size if self.map.tiles else screen_width
                map_height = len(self.map.tiles) * self.map.tile_size if self.map.tiles else screen_height
                center_x = map_width // 2
                center_y = map_height // 2
                
                if player is not None:
                    # Use provided player to preserve state (drunkenness, etc.)
                    self.johnny = player
                    # Set position to map center
                    self.johnny.setX(center_x)
                    self.johnny.setY(center_y)
                    Logger.debug("MapPageView.__init__", "Using provided player", 
                               name=self.johnny.getName(), 
                               drunkenness=self.johnny.getDrunkenness(),
                               position=(center_x, center_y))
                else:
                    # Create new player if none provided
                    self.johnny = PlayerModel("Johnny Fuzz", center_x, center_y)
                    beer = BottleModel("Beer", 15, 3, 5)
                    self.johnny.setSelectedBottle(beer)
                    Logger.debug("MapPageView.__init__", "New player created", 
                               name=self.johnny.getName(),
                               position=(center_x, center_y))
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === CONTROLLER INITIALIZATION ===
            
            try:
                self.controller = PlayerController(self.screen, self.johnny)
                Logger.debug("MapPageView.__init__", "Player controller created")
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === VIEW INITIALIZATION ===
            
            try:
                self.player_view = CaracterView("Game/Assets/guitare.png")
                self.map_view = MapView(self.map)
                
                Logger.debug("MapPageView.__init__", "Character and map views created")
            except Exception as e:
                Logger.error("MapPageView.__init__", e)
                raise
            
            # === TRANSITION STATE ===
            
            self.show_transition_prompt = False
            self.transition_ready = True  # Enable transition immediately
            
            # === SHOP STATE ===
            
            # Define shop building position based on map tiles
            # Shop will be on tiles at position (shop_tile_x, shop_tile_y)
            # Using tile coordinates: shop at column 18-20, row 8-10 (3x3 tiles)
            self.shop_tile_x = 18  # Column position
            self.shop_tile_y = 8   # Row position
            self.shop_tile_width = 3  # Shop spans 3 tiles wide
            self.shop_tile_height = 3  # Shop spans 3 tiles tall
            
            # Calculate pixel position from tile coordinates
            map_width = len(self.map.tiles[0]) * self.map.tile_size if self.map.tiles else screen_width
            map_height = len(self.map.tiles) * self.map.tile_size if self.map.tiles else screen_height
            self.shop_x = self.shop_tile_x * self.map.tile_size + (self.shop_tile_width * self.map.tile_size) // 2
            self.shop_y = self.shop_tile_y * self.map.tile_size + (self.shop_tile_height * self.map.tile_size) // 2
            self.shop_width = self.shop_tile_width * self.map.tile_size
            self.shop_height = self.shop_tile_height * self.map.tile_size
            self.near_shop = False
            self.show_shop_prompt = False
            
        except Exception as e:
            Logger.error("MapPageView.__init__", e)
            raise
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main game loop for the map page view.
        Handles events, updates game state, and renders the map.
        Returns a string indicating the next view: "ACT1", "ACT2", "RHYTHM", or "QUIT".
        """
        try:
            clock = pygame.time.Clock()
            running = True
            transition_triggered = False
            Logger.debug("MapPageView.run", "Map page loop started", current_act=self.current_act)
            
            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            Logger.debug("MapPageView.run", "QUIT event received")
                            return "QUIT"
                        
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen = pygame.display.set_mode((new_width, new_height), self.resizable)
                                self.rescaleBackground(new_width, new_height)
                                Logger.debug("MapPageView.run", "Window resized", 
                                          width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("MapPageView.run", e)
                        
                        elif event.type == pygame.KEYDOWN:
                            # Check for pause menu (ESC)
                            if event.key == pygame.K_ESCAPE:
                                # Open pause menu
                                try:
                                    pause_menu = PauseMenuView(self.screen)
                                    pause_result = pause_menu.run()
                                    
                                    if pause_result == "quit":
                                        Logger.debug("MapPageView.run", "Quit requested from pause menu")
                                        return "QUIT"
                                    elif pause_result == "main_menu":
                                        Logger.debug("MapPageView.run", "Main menu requested from pause menu")
                                        return "MAIN_MENU"
                                    elif pause_result == "continue":
                                        # If "continue", just resume the game loop
                                        Logger.debug("MapPageView.run", "Resuming from pause menu")
                                        # Continue the loop normally
                                    else:
                                        # Default: continue
                                        Logger.debug("MapPageView.run", "Resuming from pause menu (default)")
                                except Exception as e:
                                    Logger.error("MapPageView.run", e)
                            
                            # Check for shop entry (E key when near shop)
                            elif event.key == pygame.K_e and self.near_shop:
                                try:
                                    # Open shop
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
                                                return "QUIT"
                                            
                                            result = shop_controller.handleInput(shop_event)
                                            if result == "exit":
                                                shop_running = False
                                                Logger.debug("MapPageView.run", "Shop closed")
                                        
                                        shop_controller.update()
                                        shop_view.draw()
                                        pygame.display.flip()
                                        shop_clock.tick(60)
                                    
                                    Logger.debug("MapPageView.run", "Returned from shop")
                                except Exception as e:
                                    Logger.error("MapPageView.run", e)
                            
                            # Check for transition trigger (SPACE) - must be checked before movement
                            if event.key == pygame.K_SPACE and self.transition_ready:
                                Logger.debug("MapPageView.run", "Transition triggered by SPACE", next_act=self.current_act)
                                transition_triggered = True
                                running = False
                                break
                            
                            # Handle player movement (arrow keys and WASD) - only if not SPACE
                            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                                           pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                                try:
                                    # Create a copy of the event for movement
                                    movement_event = pygame.event.Event(pygame.KEYDOWN, key=event.key)
                                    # Convert WASD to arrow keys for controller
                                    if event.key == pygame.K_a:
                                        movement_event.key = pygame.K_LEFT
                                    elif event.key == pygame.K_d:
                                        movement_event.key = pygame.K_RIGHT
                                    elif event.key == pygame.K_w:
                                        movement_event.key = pygame.K_UP
                                    elif event.key == pygame.K_s:
                                        movement_event.key = pygame.K_DOWN
                                    self.controller.handleInput(movement_event)
                                except Exception as e:
                                    Logger.error("MapPageView.run", e)
                        
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
                                    # Open shop on click
                                    try:
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
                                                    return "QUIT"
                                                
                                                result = shop_controller.handleInput(shop_event)
                                                if result == "exit":
                                                    shop_running = False
                                                    Logger.debug("MapPageView.run", "Shop closed")
                                            
                                            shop_controller.update()
                                            shop_view.draw()
                                            pygame.display.flip()
                                            shop_clock.tick(60)
                                        
                                        Logger.debug("MapPageView.run", "Returned from shop")
                                    except Exception as e:
                                        Logger.error("MapPageView.run", e)
                    
                    # === UPDATE ===
                    
                    # Check if player is near shop (within 2 tiles distance)
                    try:
                        player_x = self.johnny.getX()
                        player_y = self.johnny.getY()
                        
                        # Calculate shop bounds
                        shop_left = self.shop_tile_x * self.map.tile_size
                        shop_right = (self.shop_tile_x + self.shop_tile_width) * self.map.tile_size
                        shop_top = self.shop_tile_y * self.map.tile_size
                        shop_bottom = (self.shop_tile_y + self.shop_tile_height) * self.map.tile_size
                        
                        # Check if player is within 2 tiles of shop (interaction range)
                        interaction_range = self.map.tile_size * 2
                        if (player_x >= shop_left - interaction_range and 
                            player_x <= shop_right + interaction_range and
                            player_y >= shop_top - interaction_range and 
                            player_y <= shop_bottom + interaction_range):
                            self.near_shop = True
                            self.show_shop_prompt = True
                        else:
                            self.near_shop = False
                            self.show_shop_prompt = False
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
                        # Draw map tiles
                        self.map_view.draw(self.screen)
                        # Draw shop building (visual indicator)
                        self._drawShopBuilding()
                        # Draw player character (centered, can move)
                        self.player_view.drawCaracter(self.screen, self.johnny)
                        
                        # Draw shop prompt
                        if self.show_shop_prompt:
                                    self.drawShopPrompt()
                        
                        # Draw transition prompt
                        if self.show_transition_prompt:
                                self.drawTransitionPrompt()
                    except Exception as e:
                        Logger.error("MapPageView.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                
                except Exception as e:
                    Logger.error("MapPageView.run", e)
                    return "QUIT"
            
            # After loop exits, check if transition was triggered
            if transition_triggered:
                # === DETERMINE NEXT VIEW ===
                try:
                    if self.current_act == 1:
                        Logger.debug("MapPageView.run", "Transitioning to Act 1")
                        return "ACT1"
                    elif self.current_act == 2:
                        Logger.debug("MapPageView.run", "Transitioning to Act 2")
                        return "ACT2"
                    elif self.current_act == 3:
                        Logger.debug("MapPageView.run", "Transitioning to Rhythm")
                        return "RHYTHM"
                    else:
                        Logger.debug("MapPageView.run", "No more acts, returning to menu")
                        return "QUIT"
                except Exception as e:
                    Logger.error("MapPageView.run", e)
                    return "QUIT"
            else:
                # Loop exited without transition (shouldn't happen normally)
                Logger.debug("MapPageView.run", "Loop exited without transition")
                return "QUIT"
                        
        except Exception as e:
            Logger.error("MapPageView.run", e)
            return "QUIT"
    
    # === RENDERING HELPERS ===
    
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
                title_surf = font.render("🛒 SHOP", True, (255, 215, 0))
                instruction_surf = small_font.render("Press E to enter shop", True, (200, 200, 200))
                
                self.screen.blit(title_surf, (prompt_x + (prompt_width - title_surf.get_width()) // 2, prompt_y + 15))
                self.screen.blit(instruction_surf, (prompt_x + (prompt_width - instruction_surf.get_width()) // 2, prompt_y + 50))
            except Exception as e:
                Logger.error("MapPageView.drawShopPrompt", e)
        except Exception as e:
            Logger.error("MapPageView.drawShopPrompt", e)
    
    def _drawShopBuilding(self):
        """
        Draw the shop building on the map as a visual indicator.
        The shop is drawn on specific tiles of the map.
        """
        try:
            # Calculate shop position based on tile coordinates
            shop_left = self.shop_tile_x * self.map.tile_size
            shop_top = self.shop_tile_y * self.map.tile_size
            
            # Draw shop building rectangle covering the tiles
            shop_rect = pygame.Rect(
                shop_left,
                shop_top,
                self.shop_width,
                self.shop_height
            )
            # Draw building with a distinct color
            pygame.draw.rect(self.screen, (139, 69, 19), shop_rect)  # Brown color
            pygame.draw.rect(self.screen, (255, 215, 0), shop_rect, 3)  # Gold border
            
            # Draw shop icon/text
            try:
                font = pygame.font.SysFont("Arial", 24, bold=True)
                shop_text = font.render("🛒 SHOP", True, (255, 255, 255))
                text_x = shop_left + (self.shop_width - shop_text.get_width()) // 2
                text_y = shop_top + (self.shop_height - shop_text.get_height()) // 2
                self.screen.blit(shop_text, (text_x, text_y))
            except Exception as e:
                Logger.error("MapPageView._drawShopBuilding", e)
        except Exception as e:
            Logger.error("MapPageView._drawShopBuilding", e)

