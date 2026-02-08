"""
WelcomePageView Module

Displays the welcome/main menu page with play and quit buttons.
Handles the transition to the main game view when play button is clicked.
"""

import pygame
from Utils.Logger import Logger
from Utils.AssetManager import AssetManager
from Controllers.ButtonController import ButtonController
from Controllers.GameState import GameState
from Controllers.GameSequenceController import GameSequenceController
from Views.PageView import PageView
from Views.ButtonView import ButtonView
from Views.MapPageView import MapPageView
from Views.Act1View import Act1View
from Views.Act2View import Act2View
from Views.RhythmPageView import RhythmPageView
from Views.RhythmCombatPageView import RhythmCombatPageView


# === WELCOME PAGE VIEW CLASS ===

class WelcomPageView(PageView):
    """
    Welcome page view displaying the main menu.
    Provides navigation to start the game or quit the application.
    """
    
    def __init__(self, name, width=800, height=800, RESIZABLE=0, background_image="Game/Assets/welcomePage.png"):
        """
        Initialize the welcome page view.
        
        Args:
            name: Window title
            width: Window width in pixels
            height: Window height in pixels
            RESIZABLE: Pygame flag for window resizability
            background_image: Path to background image file
        """
        try:
            # Ensure pygame is initialized once (WelcomePageView is responsible)
            try:
                if not pygame.get_init():
                    pygame.init()
                    Logger.debug("WelcomPageView.__init__", "Pygame initialized by WelcomePageView")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise

            # Always start the game in fullscreen mode
            super().__init__(name, width, height, pygame.FULLSCREEN, background_image)
            Logger.debug("WelcomPageView.__init__", "Welcome page initialized in FULLSCREEN", name=name)
            
            # === USER SESSION DATA ===
            self.current_user = None  # Username of logged-in user
            self.is_admin = False  # Whether current user is admin (allows cheats)
            self.user_progression = None  # Progression data for logged-in user
            
            # === BUTTON INITIALIZATION ===
            
            self.buttons = []
            self.buttons_controllers = []
            
            # Pre-calculate button sizes and positions for all buttons
            play_size = (225, 82)
            quit_size = (225, 82)
            logout_size = (225, 50)
            
            play_x = int(self.width * 0.82)
            play_y = int(self.height * 0.45)
            quit_x = int(self.width * 0.82)
            quit_y = play_y + play_size[1] // 2 + 5 + quit_size[1] // 2
            logout_x = int(self.width * 0.82)
            logout_y = quit_y + quit_size[1] // 2 + 5 + logout_size[1] // 2
            
            # Play button (far right, vertically centered)
            try:
                # Compute dynamic position: far right of window
                self.play_button = ButtonView(
                    image_path='Game/Assets/buttonPlay.png',
                    position=(play_x, play_y),
                    size=play_size,
                )
                self.buttons.append(self.play_button)
                
                play_button_controller = ButtonController(self.play_button, "start_game")
                self.buttons_controllers.append(play_button_controller)
                Logger.debug("WelcomPageView.__init__", "Play button created")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise
            
            # Quit button (just below Play)
            try:
                self.quit_button = ButtonView(
                    image_path='Game/Assets/buttonQuit.png',
                    position=(quit_x, quit_y),
                    size=quit_size,
                )
                self.buttons.append(self.quit_button)
                
                quit_button_controller = ButtonController(self.quit_button, "quit_game")
                self.buttons_controllers.append(quit_button_controller)
                Logger.debug("WelcomPageView.__init__", "Quit button created")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise
            
            # Logout button (just below Quit) - with Déconnexion label
            try:
                self.logout_button = pygame.Rect(logout_x - logout_size[0]//2, logout_y - logout_size[1]//2, logout_size[0], logout_size[1])
                self.logout_button_text = "Déconnexion"
                Logger.debug("WelcomPageView.__init__", "Logout button created as simple rectangle")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise
            
            # === STAGE SELECTION ===
            self.selected_stage = 1  # Default to stage 1
            Logger.debug("WelcomPageView.__init__", "Stage selector initialized", default_stage=self.selected_stage)
            
            # === WELCOME MUSIC ===
            self.music_playing = False
            try:
                pygame.mixer.init()
                music_path = "Game/Assets/Sounds/Fake Youth - What's Left Demo 11.01.25.mp3"
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(0.6)  # 60% volume
                Logger.debug("WelcomPageView.__init__", "Welcome music loaded successfully from", path=music_path)
            except FileNotFoundError as e:
                Logger.error("WelcomPageView.__init__", f"Welcome music file not found: {e}")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", f"Failed to load welcome music: {e}")
                
        except Exception as e:
            Logger.error("WelcomPageView.__init__", e)
            raise
    
    # === BUTTON POSITION UPDATE ===
    
    def _update_button_positions(self):
        """
        Update button positions based on current window size.
        Called after window resize to maintain proportional positioning.
        """
        try:
            # Update Play button position
            play_size = (225, 82)
            play_x = int(self.width * 0.82)
            play_y = int(self.height * 0.45)
            self.play_button.set_position((play_x, play_y))
            
            # Update Quit button position
            quit_size = (225, 82)
            quit_x = int(self.width * 0.82)
            quit_y = play_y + play_size[1] // 2 + 5 + quit_size[1] // 2
            self.quit_button.set_position((quit_x, quit_y))
            
            # Update Logout button position (simple rectangle)
            logout_size = (225, 50)
            logout_x = int(self.width * 0.82)
            logout_y = quit_y + quit_size[1] // 2 + 5 + logout_size[1] // 2
            self.logout_button = pygame.Rect(logout_x - logout_size[0]//2, logout_y - logout_size[1]//2, logout_size[0], logout_size[1])
            
            Logger.debug("WelcomPageView._update_button_positions", "Button positions updated")
        except Exception as e:
            Logger.error("WelcomPageView._update_button_positions", e)
    
    # === FULLSCREEN TOGGLE ===
    
    def _toggle_fullscreen(self):
        """Toggle between fullscreen and windowed modes with F11."""
        try:
            current_flags = self.screen.get_flags()
            
            if current_flags & pygame.FULLSCREEN:
                # Currently fullscreen, switch to windowed
                self.screen = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.RESIZABLE
                )
                Logger.debug("WelcomPageView._toggle_fullscreen", "Switched to WINDOWED mode")
            else:
                # Currently windowed, switch to fullscreen
                screen_info = pygame.display.Info()
                self.width = screen_info.current_w
                self.height = screen_info.current_h
                self.screen = pygame.display.set_mode(
                    (self.width, self.height),
                    pygame.FULLSCREEN
                )
                Logger.debug("WelcomPageView._toggle_fullscreen", "Switched to FULLSCREEN mode")
            
            # Update button positions for new screen size
            self._update_button_positions()
        except Exception as e:
            Logger.error("WelcomPageView._toggle_fullscreen", e)
    
    # === MAIN LOOP ===
    
    def run(self):
        """
        Main loop for the welcome page.
        Overrides PageView.run() to handle LOGOUT and QUIT states.
        
        Returns:
            GameState.LOGOUT.value: User clicked logout
            False: User quit the application
            None: Normal return from game flow
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("WelcomPageView.run", "Welcome page loop started")
            
            while running:
                try:
                    events = pygame.event.get()
                    result = self.handle_events(events)
                    
                    # Check if handle_events returned something special
                    if result is False:
                        Logger.debug("WelcomPageView.run", "Quit requested, exiting application")
                        return False
                    elif result == GameState.LOGOUT.value:
                        Logger.debug("WelcomPageView.run", "Logout requested, returning to login")
                        return GameState.LOGOUT.value
                    elif result is True:
                        # Normal operation, continue the loop
                        pass
                    else:
                        # Unknown result, treat as continue
                        pass
                    
                    self.update()
                    self.render()
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("WelcomPageView.run", e)
                    continue
            
            Logger.debug("WelcomPageView.run", "Welcome page loop ended")
            return None
        except Exception as e:
            Logger.error("WelcomPageView.run", e)
            raise

    # === GENERIC LOOP HOOKS (PageView) ===

    def handle_events(self, events):
        """
        Handle events for the welcome page.

        Returns:
            bool: True to keep running, False to exit the menu.
        """
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    Logger.debug("WelcomPageView.handle_events", "QUIT event received")
                    return False

                if event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    try:
                        new_width = event.w
                        new_height = event.h
                        self.set_window_size(new_width, new_height, self.resizable)
                        # Update button positions after resize
                        self._update_button_positions()
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Window resized",
                            width=new_width,
                            height=new_height,
                        )
                    except Exception as e:
                        Logger.error("WelcomPageView.handle_events", e)
                    # Continue running after resize
                    continue

                # Handle numeric keys 1-8 for stage selection (admin only)
                if event.type == pygame.KEYDOWN:
                    # Check for numeric keys 1-8
                    numeric_keys = {
                        pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4,
                        pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8
                    }
                    
                    if event.key in numeric_keys:
                        stage_num = numeric_keys[event.key]
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Numeric key detected",
                            key=event.key,
                            stage_num=stage_num,
                            is_admin=self.is_admin,
                            current_user=self.current_user
                        )
                        # Only allow stage selection for admin users
                        if self.is_admin:
                            self.selected_stage = stage_num
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Stage selected (ADMIN) - launching game",
                                stage=self.selected_stage
                            )
                            # Launch game directly with selected stage
                            try:
                                result = self._startGameFlow(self.selected_stage)
                                Logger.debug(
                                    "WelcomPageView.handle_events",
                                    "Returned from game flow via stage selection",
                                    result=result,
                                )
                                if result == GameState.QUIT.value:
                                    Logger.debug("WelcomPageView.handle_events", "Quit requested during game flow, exiting menu")
                                    return False
                            except Exception as e:
                                Logger.error("WelcomPageView.handle_events.stage_jump", e)
                        else:
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Stage selection blocked: admin only",
                                is_admin=self.is_admin
                            )
                        continue
                    
                    # === HANDLE F11 FOR FULLSCREEN TOGGLE ===
                    if event.key == pygame.K_F11:
                        try:
                            self._toggle_fullscreen()
                        except Exception as e:
                            Logger.error("WelcomPageView.handle_events", f"Failed to toggle fullscreen: {e}")
                        continue
                
                # Handle logout button click (simple rectangle)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = event.pos
                        if self.logout_button.collidepoint(mouse_pos):
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Logout button clicked - returning to login"
                            )
                            return GameState.LOGOUT.value
                
                # Delegate clicks/inputs to button controllers
                for button_controller in self.buttons_controllers:
                    action = button_controller.handleEvents(event)
                    if action == GameState.START_GAME.value:
                        # Use default (starting_stage=0) to load player progression
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Start game action received, loading from progression"
                        )
                        try:
                            result = self._startGameFlow()
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Returned from game flow, showing menu again",
                                result=result,
                            )
                            if result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView.handle_events", "Quit requested during game flow, exiting menu")
                                return False
                            elif result == GameState.LOGOUT.value:
                                Logger.debug("WelcomPageView.handle_events", "Logout requested during game flow, returning to login")
                                return GameState.LOGOUT.value
                        except Exception as e:
                            Logger.error("WelcomPageView.handle_events", e)
                    elif action == GameState.QUIT.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Quit game action received - closing application",
                        )
                        return False
                    elif action == GameState.LOGOUT.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Logout action received - returning to login",
                        )
                        return GameState.LOGOUT.value

            return True
        except Exception as e:
            Logger.error("WelcomPageView.handle_events", e)
            return False

    def update(self):
        """
        Update welcome page state.
        Handles welcome music playback.
        """
        try:
            # Start playing welcome music if it's not already playing
            if not self.music_playing:
                try:
                    pygame.mixer.music.play(-1)  # -1 means loop infinitely
                    self.music_playing = True
                    Logger.debug("WelcomPageView.update", "Welcome music started playing")
                except Exception as e:
                    Logger.error("WelcomPageView.update", f"Failed to play welcome music: {e}")
        except Exception as e:
            Logger.error("WelcomPageView.update", e)
        
        return None

    def render(self):
        """
        Render welcome page content.
        """
        try:
            self.draw()
            for button in self.buttons:
                button.draw(self.screen)
            
            # Draw logout button (simple rectangle with text)
            try:
                logout_color = (100, 100, 100)  # gray
                logout_hover_color = (150, 150, 150)  # lighter gray on hover
                
                # Check if mouse is over logout button
                mouse_pos = pygame.mouse.get_pos()
                if self.logout_button.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, logout_hover_color, self.logout_button, border_radius=5)
                else:
                    pygame.draw.rect(self.screen, logout_color, self.logout_button, border_radius=5)
                
                # Draw border
                pygame.draw.rect(self.screen, (255, 255, 255), self.logout_button, 2, border_radius=5)
                
                # Draw text
                font = pygame.font.SysFont("Arial", 20)
                text_surf = font.render(self.logout_button_text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.logout_button.center)
                self.screen.blit(text_surf, text_rect)
            except Exception as e:
                Logger.error("WelcomPageView.render - logout button", e)
            
            # Display health warning at the top
            try:
                small_font = pygame.font.SysFont("Arial", int(self.height * 0.02), italic=True)
                warning_text = "L'abus d'alcool est dangereux pour la santé"
                warning_surf = small_font.render(warning_text, True, (200, 100, 100))
                warning_x = self.width // 2 - warning_surf.get_width() // 2
                warning_y = 10
                self.screen.blit(warning_surf, (warning_x, warning_y))
            except Exception as e:
                Logger.error("WelcomPageView.render - warning text", e)
            
            # Display login info at the bottom (very small text)
            try:
                tiny_font = pygame.font.SysFont("Arial", int(self.height * 0.015))
                login_text = f"Connecté: {self.current_user}"
                if self.is_admin:
                    login_text += " (Admin - Cheats: 1-8, P)"
                login_surf = tiny_font.render(login_text, True, (150, 150, 150))
                login_x = 10
                login_y = self.height - 30
                self.screen.blit(login_surf, (login_x, login_y))
            except Exception as e:
                Logger.error("WelcomPageView.render - login info", e)
        except Exception as e:
            Logger.error("WelcomPageView.render", e)
    
    # === GAME TRANSITION ===
    
    
    # === PROGRESSION LOADING/SAVING METHODS ===
    
    def _load_player_from_progression(self, progression_data):
        """
        Load a player object from progression data.
        
        Args:
            progression_data: Dictionary containing saved progression data
            
        Returns:
            PlayerModel instance with loaded stats
        """
        try:
            from Models.PlayerModel import PlayerModel
            from Models.BottleModel import BottleModel
            from Models.GuitarModel import GuitarFactory
            
            # Create player with game name "Lola Coma" (not the login username)
            player = PlayerModel("Lola Coma", 
                               progression_data.get("position", {}).get("x", 60),
                               progression_data.get("position", {}).get("y", 60))
            
            # Restore player stats
            player.setHealth(progression_data.get("hp", 100))
            player.setDamage(progression_data.get("damage", 10))
            player.setDrunkenness(progression_data.get("drunkenness", 0))
            player.setComaRisk(progression_data.get("coma_risk", 0))
            player.setLevel(progression_data.get("level", 0))
            player.setCurrency(progression_data.get("currency", 0))
            player.setAccuracy(0.85)  # Default accuracy
            
            # Clear default inventory added by PlayerModel.__init__
            player.inventory.items = []
            player.inventory.selected_index = 0
            
            # Restore inventory from saved progression
            inventory_data = progression_data.get("inventory", [])
            if inventory_data:
                for bottle_data in inventory_data:
                    try:
                        bottle = BottleModel(
                            bottle_data.get("name", "Beer"),
                            alcohol_level=bottle_data.get("alcohol_level", 15),
                            bonus_damage=bottle_data.get("bonus_damage", 0),
                            accuracy_penalty=bottle_data.get("accuracy_penalty", 0)
                        )
                        player.inventory.add_item(bottle)
                    except Exception as e:
                        Logger.error("WelcomPageView._load_player_from_progression", f"Failed to restore bottle: {e}")
            else:
                # Add default beer if no inventory was saved
                default_beer = BottleModel("Beer", 15, 3, 5)
                player.inventory.add_item(default_beer)
            
            # Set selected bottle from first item in inventory if available
            selected_item = player.inventory.get_selected_item()
            if selected_item:
                player.setSelectedBottle(selected_item)
            
            # Equip with starting guitar
            try:
                la_pelle = GuitarFactory.createLaPelle()
            except Exception as e:
                Logger.error("WelcomPageView._load_player_from_progression", f"Failed to load guitar: {e}")
            
            Logger.debug("WelcomPageView._load_player_from_progression", "Player loaded from progression", 
                        username=self.current_user)
            return player
        except Exception as e:
            Logger.error("WelcomPageView._load_player_from_progression", e)
            raise
    
    def _save_player_progression(self, player, sequence_controller):
        """
        Save player progression data to file.
        
        Args:
            player: PlayerModel instance with current stats
            sequence_controller: GameSequenceController with current stage
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            if not self.current_user:
                return False
            
            # Update progression data
            # Note: username is NOT stored here - it's associated via the progression filename
            # The game character is always "Lola Coma" regardless of login username
            
            # Serialize inventory bottles to JSON-compatible format
            inventory_list = []
            try:
                if hasattr(player, 'inventory') and player.inventory:
                    for bottle in player.inventory.get_all_items():
                        inventory_list.append({
                            "name": bottle.getName(),
                            "alcohol_level": bottle.getAlcoholLevel(),
                            "bonus_damage": bottle.getBonusDamage(),
                            "accuracy_penalty": bottle.getAccuracyPenalty()
                        })
            except Exception as e:
                Logger.error("WelcomPageView._save_player_progression", f"Failed to serialize inventory: {e}")
            
            progression = {
                "current_stage": sequence_controller.get_current_stage(),
                "level": player.getLevel(),
                "hp": player.getHealth(),
                "max_hp": 100,  # Default max HP
                "damage": player.getDamage(),
                "drunkenness": player.getDrunkenness(),
                "coma_risk": player.getComaRisk(),
                "currency": player.getCurrency(),
                "position": {
                    "x": player.getX(),
                    "y": player.getY()
                },
                "inventory": inventory_list,
                "completed_acts": [],
                "completed_rhythms": []
            }
            
            # Save to user's progression file
            from Utils.UserManager import UserManager
            user_manager = UserManager()
            success = user_manager.save_progression(self.current_user, progression)
            
            if success:
                Logger.debug("WelcomPageView._save_player_progression", "Player progression saved", 
                           username=self.current_user)
            else:
                Logger.debug("WelcomPageView._save_player_progression", "Failed to save player progression", 
                           username=self.current_user)
            
            return success
        except Exception as e:
            Logger.error("WelcomPageView._save_player_progression", e)
            return False
    
    def _startGameFlow(self, starting_stage=0):
        """
        Start the complete game flow with 8 stages:
        1. RhythmPageView
        2. Map (Act 1)
        3. Act1
        4. Map (Act 2)
        5. Act2
        6. RhythmPageView
        7. Map (Act 3)
        8. RhythmCombatView
        
        Args:
            starting_stage: Stage to start from (1-8). If 0 (default), load from player progression.
        """
        try:
            # Stop welcome music when game starts
            if self.music_playing:
                try:
                    pygame.mixer.music.stop()
                    self.music_playing = False
                    Logger.debug("WelcomPageView._startGameFlow", "Welcome music stopped")
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", f"Failed to stop welcome music: {e}")
            
            Logger.debug("WelcomPageView._startGameFlow", "Starting game flow with sequence controller")
            
            # Initialize sequence controller
            sequence_controller = GameSequenceController()
            
            # Set to the starting stage selected by user
            sequence_controller.set_stage(starting_stage)
            
            # Pass admin status to sequence controller (for cheat commands)
            sequence_controller.is_admin = self.is_admin
            
            Logger.debug("WelcomPageView._startGameFlow", "GameSequenceController created", starting_stage=starting_stage, is_admin=self.is_admin)
            
            # Save current menu size and attempt to switch to screen resolution for gameplay
            menu_size = None
            menu_resizable = getattr(self, "resizable", pygame.RESIZABLE)
            try:
                screen = self.screen
                menu_size = (screen.get_width(), screen.get_height())
                pygame.display.set_caption("Six-String Hangover")
                Logger.debug("WelcomPageView._startGameFlow", "Menu size saved", width=menu_size[0], height=menu_size[1])
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)

            try:
                screen_info = pygame.display.Info()
                full_size = (screen_info.current_w, screen_info.current_h)
                # If not already fullscreen, switch to fullscreen for gameplay
                try:
                    pre_fullscreen = bool(self.screen.get_flags() & pygame.FULLSCREEN)
                except Exception:
                    pre_fullscreen = False

                if not pre_fullscreen:
                    try:
                        # Switch to exclusive fullscreen mode
                        pygame.display.set_mode(full_size, pygame.FULLSCREEN)
                        screen = pygame.display.get_surface()
                        self.screen = screen
                        Logger.debug("WelcomPageView._startGameFlow", "Switched to FULLSCREEN for gameplay", width=full_size[0], height=full_size[1])
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", e)
                else:
                    Logger.debug("WelcomPageView._startGameFlow", "Already in fullscreen", width=full_size[0], height=full_size[1])
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
            
            # Create player once - will be passed through all views to preserve state
            try:
                from Models.PlayerModel import PlayerModel
                from Models.BottleModel import BottleModel
                from Models.GuitarModel import GuitarFactory
                from Models.BossModel import BossModel
                
                # Initialize AssetManager for loading boss configurations
                asset_manager = AssetManager("Game")
                
                # Load player from progression data if available
                if self.current_user and self.user_progression:
                    # Load player from saved progression
                    player = self._load_player_from_progression(self.user_progression)
                    # If starting_stage is 0 (default), use the saved stage from progression
                    # Otherwise, force the requested stage (admin cheat)
                    if starting_stage == 0:
                        current_stage = self.user_progression.get("current_stage", 1)
                        sequence_controller.set_stage(current_stage)
                        Logger.debug("WelcomPageView._startGameFlow", "Player loaded from progression with saved stage", username=self.current_user, saved_stage=current_stage)
                    else:
                        Logger.debug("WelcomPageView._startGameFlow", "Player loaded from progression with FORCED stage (admin cheat)", username=self.current_user, forced_stage=starting_stage)
                else:
                    # Create new player with default stats
                    player = PlayerModel("Lola Coma", 60, 60)
                    player.setHealth(100)
                    player.setDamage(10)
                    player.setAccuracy(0.85)
                    player.setDrunkenness(0)
                    player.setComaRisk(10)
                    player.setLevel(0)  # Start at level 0
                    
                    # Stats only increase after defeating final boss (Manager Corrompu)
                    
                    # Equip with starting guitar
                    la_pelle = GuitarFactory.createLaPelle()
                    
                    # Give starting bottle
                    beer = BottleModel("Beer", 15, 3, 5)
                    player.setSelectedBottle(beer)
                
                # Load bosses from asset configuration
                try:
                    # Load boss configurations
                    manager_corrompu_config = asset_manager.get_boss_by_name("Manager Corrompu")
                    gros_bill_config = asset_manager.get_boss_by_name("Gros Bill")
                    chef_securite_config = asset_manager.get_boss_by_name("Chef de la Sécurité")
                    
                    # Create boss instances from configurations
                    if manager_corrompu_config:
                        manager_corrompu = BossModel.from_config(manager_corrompu_config, 80, 80)
                    else:
                        # Fallback if config not found
                        manager_corrompu = BossModel("Manager Corrompu", 80, 80)
                        manager_corrompu.setHealth(3000)
                        manager_corrompu.setDamage(15)
                        Logger.warn("WelcomPageView._startGameFlow", "Manager Corrompu config not found, using fallback")
                    
                    if gros_bill_config:
                        gros_bill = BossModel.from_config(gros_bill_config, 80, 80)
                    else:
                        gros_bill = BossModel("Gros Bill", 80, 80)
                        gros_bill.setHealth(100)
                        gros_bill.setDamage(12)
                        gros_bill.setAccuracy(0.75)
                        Logger.warn("WelcomPageView._startGameFlow", "Gros Bill config not found, using fallback")
                    
                    if chef_securite_config:
                        chef_securite = BossModel.from_config(chef_securite_config, 80, 80)
                    else:
                        chef_securite = BossModel("Chef de la Sécurité", 80, 80)
                        chef_securite.setHealth(500)
                        chef_securite.setDamage(14)
                        chef_securite.setAccuracy(0.80)
                        Logger.warn("WelcomPageView._startGameFlow", "Chef de la Sécurité config not found, using fallback")
                    
                    Logger.debug("WelcomPageView._startGameFlow", "Bosses loaded from asset configurations")
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", f"Failed to load boss configs: {e}")
                    # Create fallback bosses
                    manager_corrompu = BossModel("Manager Corrompu", 80, 80)
                    manager_corrompu.setHealth(3000)
                    manager_corrompu.setDamage(15)

                    gros_bill = BossModel("Gros Bill", 80, 80)
                    gros_bill.setHealth(100)
                    gros_bill.setDamage(12)
                    gros_bill.setAccuracy(0.75)
                    
                    chef_securite = BossModel("Chef de la Sécurité", 80, 80)
                    chef_securite.setHealth(500)
                    chef_securite.setDamage(14)
                    chef_securite.setAccuracy(0.80)
                
                sequence_controller.set_player(player)
                
                Logger.debug("WelcomPageView._startGameFlow", "Player and bosses created successfully")
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
                raise
            
            # Main game loop - handle all 8 stages
            while True:
                try:
                    current_stage = sequence_controller.get_current_stage()
                    stage_name = sequence_controller.get_current_stage_name()
                    Logger.debug("WelcomPageView._startGameFlow", "Displaying stage", 
                               stage=current_stage, stage_name=stage_name)
                    
                    result = None
                    
                    # === STAGE 1: Rhythm Page (Act 1 Practice) ===
                    if current_stage == 1:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            rhythm_view = RhythmPageView(screen, player, sequence_controller)
                            result = rhythm_view.run()
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 2: Map (Before Act 1) ===
                    elif current_stage == 2:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            map_view = MapPageView(screen, 1, player, sequence_controller)
                            result = map_view.run()
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 3: Act 1 ===
                    elif current_stage == 3:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            sequence_controller.set_boss(gros_bill)
                            act1_view = Act1View(screen, player, sequence_controller)
                            result = act1_view.run()
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 4: Map (Before Act 2) ===
                    elif current_stage == 4:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            map_view = MapPageView(screen, 2, player, sequence_controller)
                            result = map_view.run()
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 5: Act 2 ===
                    elif current_stage == 5:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            sequence_controller.set_boss(chef_securite)
                            act2_view = Act2View(screen, player, sequence_controller)
                            result = act2_view.run()
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 6: Rhythm Page (Act 2 Practice) ===
                    elif current_stage == 6:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            rhythm_view = RhythmPageView(screen, player, sequence_controller, context="act2")
                            result = rhythm_view.run()
                            
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 7: Map (Final) ===
                    elif current_stage == 7:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            map_view = MapPageView(screen, 3, player, sequence_controller)
                            result = map_view.run()
                           
                           
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 8: Rhythm Combat (Boss Final) ===
                    elif current_stage == 8:
                        try:
                            # Views handle their own dimensioning (RESIZABLE)
                            sequence_controller.set_boss(manager_corrompu)
                            rhythm_combat_view = RhythmCombatPageView(screen, player, manager_corrompu, sequence_controller)
                            result = rhythm_combat_view.run()
                            
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === HANDLE RESULTS ===
                    if result is None:
                        # No result, something went wrong
                        Logger.debug("WelcomPageView._startGameFlow", "No result from stage", stage=current_stage)
                        break
                    
                    elif result == GameState.QUIT.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                        return GameState.QUIT.value
                    
                    elif result == GameState.LOGOUT.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Logout requested")
                        return GameState.LOGOUT.value
                    
                    elif result == GameState.MAIN_MENU.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Main menu requested")
                        break
                    
                    elif result == GameState.GAME_OVER.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Game over")
                        return
                    
                    elif result == GameState.COMPLETE.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Stage completed successfully, advancing to next stage")
                        # Advance to next stage instead of returning
                        if sequence_controller.advance_stage():
                            Logger.debug("WelcomPageView._startGameFlow", "Advanced to next stage",
                                       new_stage=sequence_controller.get_current_stage())
                        else:
                            Logger.debug("WelcomPageView._startGameFlow", "Already at final stage")
                            break
                        continue
                    
                    elif result.startswith("STAGE_"):
                        # Stage jump requested via numeric key (admin only)
                        if not self.is_admin:
                            Logger.debug("WelcomPageView._startGameFlow", "Stage jump blocked: admin only")
                            continue
                        
                        try:
                            stage_num = int(result.split("_")[1])
                            Logger.debug("WelcomPageView._startGameFlow", "Stage jump via numeric key (ADMIN)", target_stage=stage_num)
                            # Set the sequence controller to the requested stage
                            sequence_controller.set_stage(stage_num)
                            # Continue to next iteration which will display the requested stage
                            continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    else:
                        # Unknown result or normal completion of stage
                        # Advance to next stage
                        if sequence_controller.advance_stage():
                            Logger.debug("WelcomPageView._startGameFlow", "Advanced to next stage",
                                       new_stage=sequence_controller.get_current_stage())
                        else:
                            Logger.debug("WelcomPageView._startGameFlow", "Already at final stage")
                            break
                        
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", e)
                    break
            
        except Exception as e:
            Logger.error("WelcomPageView._startGameFlow", e)
            raise
        finally:
            # Save player progression before returning to menu
            try:
                if self.current_user:
                    self._save_player_progression(player, sequence_controller)
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", f"Failed to save progression: {e}")
            
            # Restart welcome music when returning to menu
            try:
                if not self.music_playing:
                    try:
                        pygame.mixer.music.play(-1)  # Resume looping music
                        self.music_playing = True
                        Logger.debug("WelcomPageView._startGameFlow", "Welcome music resumed on return to menu")
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", f"Failed to resume welcome music: {e}")
            except Exception:
                pass
            
            # Restore the menu window size if it was saved
            try:
                if menu_size:
                    try:
                        # Restore menu window centered
                        self.set_window_size(menu_size[0], menu_size[1], menu_resizable if menu_resizable else pygame.RESIZABLE)
                        Logger.debug("WelcomPageView._startGameFlow", "Restored menu window size", width=menu_size[0], height=menu_size[1])
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", e)
            except Exception:
                pass
