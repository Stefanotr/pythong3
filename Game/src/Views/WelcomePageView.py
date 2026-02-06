"""
WelcomePageView Module

Displays the welcome/main menu page with play and quit buttons.
Handles the transition to the main game view when play button is clicked.
"""

import pygame
from Utils.Logger import Logger
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

            super().__init__(name, width, height, RESIZABLE, background_image)
            Logger.debug("WelcomPageView.__init__", "Welcome page initialized", name=name, width=width, height=height)
            
            # === BUTTON INITIALIZATION ===
            
            self.buttons = []
            self.buttons_controllers = []
            
            # Play button (far right, vertically centered)
            try:
                # Compute dynamic position: far right of window
                play_size = (225, 82)  # reduced by 1/4
                play_x = int(self.width * 0.82)
                play_y = int(self.height * 0.45)
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
                quit_size = (225, 82)  # same reduced size
                quit_x = int(self.width * 0.82)
                # place below play button with small gap
                quit_y = play_y + play_size[1] // 2 + 5 + quit_size[1] // 2
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
            
            Logger.debug("WelcomPageView._update_button_positions", "Button positions updated")
        except Exception as e:
            Logger.error("WelcomPageView._update_button_positions", e)
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

                # Handle numeric keys 1-8 for stage selection
                if event.type == pygame.KEYDOWN:
                    if pygame.K_1 <= event.key <= pygame.K_8:
                        stage_num = event.key - pygame.K_1 + 1
                        self.selected_stage = stage_num
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Stage selected",
                            stage=self.selected_stage
                        )
                        continue
                
                # Delegate clicks/inputs to button controllers
                for button_controller in self.buttons_controllers:
                    action = button_controller.handleEvents(event)
                    if action == GameState.START_GAME.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Start game action received, starting game flow",
                            starting_stage=self.selected_stage
                        )
                        try:
                            result = self._startGameFlow(self.selected_stage)
                            Logger.debug(
                                "WelcomPageView.handle_events",
                                "Returned from game flow, showing menu again",
                                result=result,
                            )
                            if result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView.handle_events", "Quit requested during game flow, exiting menu")
                                return False
                        except Exception as e:
                            Logger.error("WelcomPageView.handle_events", e)
                    elif action == GameState.QUIT.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Quit game action received",
                        )
                        return False

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
        except Exception as e:
            Logger.error("WelcomPageView.render", e)
    
    # === GAME TRANSITION ===
    
    def _startGameFlow(self, starting_stage=1):
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
        
        Players can press keys 1-8 to jump to specific stages during gameplay.
        
        Args:
            starting_stage: The stage to start from (1-8, default 1)
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
            Logger.debug("WelcomPageView._startGameFlow", "GameSequenceController created", starting_stage=starting_stage)
            
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
                
                # Create final boss for rhythm combat - Manager Corrompu
                manager_corrompu = BossModel("Manager Corrompu", 80, 80)
                manager_corrompu.setHealth(3000)
                manager_corrompu.setDamage(15)

                # Act 1: Gros Bill
                gros_bill = BossModel("Gros Bill", 80, 80)
                gros_bill.setHealth(100)
                gros_bill.setDamage(12)
                gros_bill.setAccuracy(0.75)
                self.boss = gros_bill
                    
                # Act 2: Chef de la Sécurité
                chef_securite = BossModel("Chef de la Sécurité", 80, 80)
                chef_securite.setHealth(500)
                chef_securite.setDamage(14)
                chef_securite.setAccuracy(0.80)
                self.boss = chef_securite
                
                sequence_controller.set_player(player)
                
                Logger.debug("WelcomPageView._startGameFlow", "Player and Manager Corrompu created for rhythm combat")
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
                        # Stage jump requested via numeric key
                        try:
                            stage_num = int(result.split("_")[1])
                            Logger.debug("WelcomPageView._startGameFlow", "Stage jump via numeric key", target_stage=stage_num)
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
