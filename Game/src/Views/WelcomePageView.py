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
from Views.MainPageView import MainPageView


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
                                self._rescale_background(new_width, new_height)
                                Logger.debug("WelcomPageView.run", "Window resized", 
                                          width=new_width, height=new_height)
                            except Exception as e:
                                Logger.error("WelcomPageView.run", e)
                        else:
                            # Check button clicks
                            for button_controller in self.buttons_controllers:
                                action = button_controller.handleEvents(event)
                                if action == "start_game":
                                    # Exit welcome page loop and start main game
                                    running = False
                                    Logger.debug("WelcomPageView.run", "Start game action received, transitioning to MainPageView")
                                    self._startMainGame()
                                    return
                                elif action == "quit_game":
                                    # Quit game (handled in ButtonController)
                                    return

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
            pygame.quit()
            
        except Exception as e:
            Logger.error("WelcomPageView.run", e)
            pygame.quit()
            raise
    
    # === GAME TRANSITION ===
    
    def _startMainGame(self):
        """
        Transition to the main game view.
        Creates and runs the MainPageView.
        """
        try:
            Logger.debug("WelcomPageView._startMainGame", "Starting main game")
            
            # Close current window
            pygame.quit()
            
            # Initialize pygame for main game
            pygame.init()
            
            # Create and run main game view
            game_page = MainPageView("Guitaroholic", 1920, 1080, pygame.RESIZABLE)
            game_page.run()
            
        except Exception as e:
            Logger.error("WelcomPageView._startMainGame", e)
            pygame.quit()
            raise
