"""
WelcomePageView Module

Displays the welcome/main menu page with play and quit buttons.
Handles the transition to the main game view when play button is clicked.
"""

import pygame
from Utils.Logger import Logger
from Controllers.ButtonController import ButtonController
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

    # === MAIN LOOP ===
    
    def run(self):
        """
        Main game loop for the welcome page.
        Handles events, draws the page, and manages transition to main game.
        """
        try:
            clock = pygame.time.Clock()
            running = True
            Logger.debug("WelcomPageView.run", "Welcome page loop started")

            while running:
                try:
                    # === EVENT HANDLING ===
                    
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            Logger.debug("WelcomPageView.run", "QUIT event received")
                        elif event.type == pygame.VIDEORESIZE:
                            # Handle window resize
                            try:
                                new_width = event.w
                                new_height = event.h
                                self.screen = pygame.display.set_mode((new_width, new_height), self.resizable)
                                self.rescaleBackground(new_width, new_height)
                                Logger.debug("WelcomPageView.run", "Window resized", 
                                          width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("WelcomPageView.run", e)
                        else:
                            # Check button clicks
                            for button_controller in self.buttons_controllers:
                                action = button_controller.handleEvents(event)
                                if action == "start_game":
                                    # Start game flow - if it returns, we continue the welcome page loop
                                    Logger.debug("WelcomPageView.run", "Start game action received, transitioning to MapPageView")
                                    try:
                                        self._startGameFlow()
                                        # After game flow ends, continue welcome page loop (don't quit)
                                        Logger.debug("WelcomPageView.run", "Returned from game flow, showing menu again")
                                    except Exception as e:
                                        Logger.error("WelcomPageView.run", e)
                                    # Continue the loop to show menu again (don't set running = False)
                                elif action == "quit_game":
                                    # Quit game
                                    running = False
                                    Logger.debug("WelcomPageView.run", "Quit game action received")
                                    break

                    # === RENDERING ===
                    
                    self.draw()
                    for button in self.buttons:
                        button.draw(self.screen)

                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("WelcomPageView.run", e)
                    # Continue running even if one frame fails
                    continue

            Logger.debug("WelcomPageView.run", "Welcome page loop ended")
            # Don't quit here - let the caller handle it
            
        except Exception as e:
            Logger.error("WelcomPageView.run", e)
            pygame.quit()
            raise
    
    # === GAME TRANSITION ===
    
    def _startGameFlow(self):
        """
        Start the complete game flow: Map → Act1 → Map → Act2 → Map → Rhythm.
        Manages all transitions between game states.
        """
        try:
            Logger.debug("WelcomPageView._startGameFlow", "Starting game flow")
            
            # Close current window
            try:
                pygame.quit()
                Logger.debug("WelcomPageView._startGameFlow", "Previous window closed")
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
            
            # Initialize pygame for game
            try:
                pygame.init()
                Logger.debug("WelcomPageView._startGameFlow", "Pygame reinitialized")
            except Exception as e:
                Logger.error("WelcomPageView._startGameFlow", e)
                raise
            
            # Get screen info and create resizable window
            try:
                screen_info = pygame.display.Info()
                screen = pygame.display.set_mode(
                    (screen_info.current_w, screen_info.current_h), 
                    pygame.RESIZABLE
                )
                pygame.display.set_caption("Six-String Hangover")
                Logger.debug("WelcomPageView._startGameFlow", "Screen created", 
                           width=screen_info.current_w, height=screen_info.current_h)
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
                        
                        if result == "QUIT":
                            Logger.debug("WelcomPageView._startGameFlow", "Quit requested from map")
                            break
                        elif result == "MAIN_MENU":
                            Logger.debug("WelcomPageView._startGameFlow", "Main menu requested from map")
                            # Return to main menu (exit game flow)
                            return
                    except Exception as e:
                        Logger.error("WelcomPageView._startGameFlow", e)
                        break
                    
                    # === ACT 1 ===
                    if result == "ACT1":
                        try:
                            act1_view = Act1View(screen, player)
                            act1_result = act1_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Act 1 completed", result=act1_result)
                            
                            if act1_result == "GAME_OVER":
                                Logger.debug("WelcomPageView._startGameFlow", "Game over")
                                break
                            elif act1_result == "QUIT":
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                                break
                            elif act1_result == "MAP":
                                # Continue to next map phase
                                current_act = 2
                                continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    # === ACT 2 ===
                    elif result == "ACT2":
                        try:
                            act2_view = Act2View(screen, player)
                            act2_result = act2_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Act 2 completed", result=act2_result)
                            
                            if act2_result == "GAME_OVER":
                                Logger.debug("WelcomPageView._startGameFlow", "Game over")
                                break
                            elif act2_result == "QUIT":
                                Logger.debug("WelcomPageView._startGameFlow", "Quit requested")
                                break
                            elif act2_result == "MAP":
                                # Continue to next map phase
                                current_act = 3
                                continue
                        except Exception as e:
                            Logger.error("WelcomPageView._startGameFlow", e)
                            break
                    
                    # === RHYTHM (FINAL) ===
                    elif result == "RHYTHM":
                        try:
                            rhythm_view = RhythmPageView(screen, player)
                            rhythm_result = rhythm_view.run()
                            Logger.debug("WelcomPageView._startGameFlow", "Rhythm completed", result=rhythm_result)
                            
                            # Game complete
                            if rhythm_result == "COMPLETE":
                                Logger.debug("WelcomPageView._startGameFlow", "Game completed successfully!")
                            break
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
            try:
                pygame.quit()
            except Exception:
                pass
            raise
