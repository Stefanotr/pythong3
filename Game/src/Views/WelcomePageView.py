"""
WelcomePageView Module

Displays the welcome/main menu page with play and quit buttons.
Handles the transition to the main game view when play button is clicked.
"""

import pygame
from Utils.Logger import Logger
from Controllers.ButtonController import ButtonController
from Controllers.GameState import GameState
from Views.PageView import PageView
from Views.ButtonView import ButtonView
from Views.MapPageView import MapPageView
from Views.Act1View import Act1View
from Views.Act2View import Act2View
from Views.RhythmPageView import RhythmPageView


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
                        self.screen = pygame.display.set_mode((new_width, new_height), self.resizable)
                        self.rescaleBackground(new_width, new_height)
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

                # Delegate clicks/inputs to button controllers
                for button_controller in self.buttons_controllers:
                    action = button_controller.handleEvents(event)
                    if action == GameState.START_GAME.value:
                        Logger.debug(
                            "WelcomPageView.handle_events",
                            "Start game action received, starting game flow",
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
    
    def _startGameFlow(self):
        """
        Start the complete game flow: Map → Act1 → Map → Act2 → Map → Rhythm.
        Manages all transitions between game states.
        """
        try:
            Logger.debug("WelcomPageView._startGameFlow", "Starting game flow")
            
            # Reuse existing window from the welcome menu (do NOT quit/re-init pygame)
            try:
                screen = self.screen
                pygame.display.set_caption("Six-String Hangover")
                Logger.debug("WelcomPageView._startGameFlow", "Reusing existing screen", 
                           width=screen.get_width(), height=screen.get_height())
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
                raise
            
            # Create player once - will be passed through all views to preserve state
            try:
                from Models.PlayerModel import PlayerModel
                from Models.BottleModel import BottleModel
                from Models.GuitarModel import GuitarFactory
                
                player = PlayerModel("Johnny Fuzz", 60, 60)
                player.setHealth(100)
                player.setDamage(10)
                player.setAccuracy(0.85)
                player.setDrunkenness(0)  # Start at 0, but will persist after this
                player.setComaRisk(10)
                
                # Equip with starting guitar
                la_pelle = GuitarFactory.createLaPelle()
                
                # Give starting bottle
                beer = BottleModel("Beer", 15, 3, 5)
                player.setSelectedBottle(beer)
                
                Logger.debug("WelcomPageView._startGameFlow", "Player created and initialized")
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
                raise
            
            # Game flow: Map → Act1 → Map → Act2 → Map → Rhythm
            current_act = 1
            
            while True:
                try:
                    # === MAP PHASE ===
                    try:
                        map_view = MapPageView(screen, current_act, player)
                        result = map_view.run()
                        Logger.debug("WelcomPageView._startGameFlow", "Map completed", result=result, current_act=current_act)
                        
                        if result == GameState.QUIT.value:
                            Logger.debug("WelcomPageView._startGameFlow", "Quit requested from map")
                            return GameState.QUIT.value
                        elif result == GameState.MAIN_MENU.value:
                            Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from map")
                            # Return to main menu (exit game flow)
                            return
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", e)
                        break
                    
                    # === ACT 1 ===
                    if result == GameState.ACT1.value:
                        try:
                            act1_view = Act1View(screen, player)
                            act1_result = act1_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Act 1 completed", result=act1_result)
                            
                            if act1_result == GameState.MAIN_MENU.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from Act 1")
                                return
                            
                            if act1_result == GameState.GAME_OVER.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Game over")
                                return
                            elif act1_result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                                return GameState.QUIT.value
                            elif act1_result == GameState.MAP.value:
                                # Continue to next map phase
                                current_act = 2
                                continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    # === ACT 2 ===
                    elif result == GameState.ACT2.value:
                        try:
                            act2_view = Act2View(screen, player)
                            act2_result = act2_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Act 2 completed", result=act2_result)
                            
                            if act2_result == GameState.MAIN_MENU.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from Act 2")
                                return
                            
                            if act2_result == GameState.GAME_OVER.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Game over")
                                return
                            elif act2_result == GameState.QUIT.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                                return GameState.QUIT.value
                            elif act2_result == GameState.MAP.value:
                                # Continue to next map phase
                                current_act = 3
                                continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    # === RHYTHM (FINAL) ===
                    elif result == GameState.RHYTHM.value:
                        try:
                            rhythm_view = RhythmPageView(screen, player)
                            rhythm_result = rhythm_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Rhythm completed", result=rhythm_result)
                            
                            if rhythm_result == GameState.MAIN_MENU.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from Rhythm")
                                return
                            
                            # Game complete
                            if rhythm_result == GameState.COMPLETE.value:
                                Logger.debug("WelcomPageView._startGameFlow", "Game completed successfully!")
                                return
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    else:
                        # Unknown result, exit
                        Logger.debug("WelcomPageView._startGameFlow", "Unknown result, exiting", result=result)
                        break
                        
                except Exception as e:
                    Logger.error("WelcomPageView._startGameFlow", e)
                    break
            
        except Exception as e:
            Logger.error("WelcomPageView._startGameFlow", e)
            raise
