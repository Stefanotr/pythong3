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
            
            # Play button (center-top)
            try:
                self.play_button = ButtonView(
                    image_path='Game/Assets/buttonPlay.png',
                    position=(400, 500),
                )
                self.buttons.append(self.play_button)
                
                play_button_controller = ButtonController(self.play_button, "start_game")
                self.buttons_controllers.append(play_button_controller)
                Logger.debug("WelcomPageView.__init__", "Play button created")
            except Exception as e:
                Logger.error("WelcomPageView.__init__", e)
                raise
            
            # Quit button (bottom)
            try:
                self.quit_button = ButtonView(
                    image_path='Game/Assets/buttonQuit.png',
                    position=(400, 700),
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
                
        except Exception as e:
            Logger.error("WelcomPageView.__init__", e)
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
        Currently no per-frame state to update.
        """
        return None

    def render(self):
        """
        Render welcome page content.
        """
        try:
            self.draw()
            for button in self.buttons:
                button.draw(self.screen)
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
                from Models.CaracterModel import CaracterModel
                
                player = PlayerModel("Johnny Fuzz", 60, 60)
                player.setHealth(100)
                player.setDamage(10)
                player.setAccuracy(0.85)
                player.setDrunkenness(0)
                player.setComaRisk(10)
                
                # Equip with starting guitar
                la_pelle = GuitarFactory.createLaPelle()
                
                # Give starting bottle
                beer = BottleModel("Beer", 15, 3, 5)
                player.setSelectedBottle(beer)
                
                # Create boss for rhythm combat
                boss = CaracterModel("Le Manager Corrompu", 80, 80)
                boss.setHealth(100)
                boss.setDamage(10)
                
                sequence_controller.set_player(player)
                Logger.debug("WelcomPageView._startGameFlow", "Player and boss created and initialized")
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
                            rhythm_view = RhythmPageView(screen, player, sequence_controller)
                            result = rhythm_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 2: Map (Before Act 1) ===
                    elif current_stage == 2:
                        try:
                            map_view = MapPageView(screen, 1, player, sequence_controller)
                            result = map_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 3: Act 1 ===
                    elif current_stage == 3:
                        try:
                            act1_view = Act1View(screen, player, sequence_controller)
                            result = act1_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 4: Map (Before Act 2) ===
                    elif current_stage == 4:
                        try:
                            map_view = MapPageView(screen, 2, player, sequence_controller)
                            result = map_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 5: Act 2 ===
                    elif current_stage == 5:
                        try:
                            act2_view = Act2View(screen, player, sequence_controller)
                            result = act2_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 6: Rhythm Page (Act 2 Practice) ===
                    elif current_stage == 6:
                        try:
                            rhythm_view = RhythmPageView(screen, player, sequence_controller)
                            result = rhythm_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 7: Map (Final) ===
                    elif current_stage == 7:
                        try:
                            map_view = MapPageView(screen, 3, player, sequence_controller)
                            result = map_view.run()
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                    
                    # === STAGE 8: Rhythm Combat (Boss Final) ===
                    elif current_stage == 8:
                        try:
                            rhythm_combat_view = RhythmCombatPageView(screen, player, boss, sequence_controller)
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
                        return
                    
                    elif result == GameState.GAME_OVER.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Game over")
                        return
                    
                    elif result == GameState.COMPLETE.value:
                        Logger.debug("WelcomPageView._startGameFlow", "Game completed successfully!")
                        return
                    
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
