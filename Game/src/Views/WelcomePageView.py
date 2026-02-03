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
from Views.Act1View import Act1View


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
                                    # Exit welcome page loop and start Act 1
                                    running = False
                                    Logger.debug("WelcomPageView.run", "Start game action received, transitioning to Act1View")
                                    self._startAct1()
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
    
    def _startAct1(self):
        """
        Transition to Act 1 view.
        Creates and runs the Act1View with proper screen initialization.
        """
        try:
            Logger.debug("WelcomPageView._startAct1", "Starting Act 1")
            
            # Close current window
            try:
                pygame.quit()
                Logger.debug("WelcomPageView._startAct1", "Previous window closed")
            except Exception as e:
                Logger.error("WelcomPageView._startAct1", e)
            
            # Initialize pygame for Act 1
            try:
                pygame.init()
                Logger.debug("WelcomPageView._startAct1", "Pygame reinitialized")
            except Exception as e:
                Logger.error("WelcomPageView._startAct1", e)
                raise
            
            # Get screen info and create resizable window
            try:
                screen_info = pygame.display.Info()
                screen = pygame.display.set_mode(
                    (screen_info.current_w, screen_info.current_h), 
                    pygame.RESIZABLE
                )
                pygame.display.set_caption("Guitaroholic - Act 1")
                Logger.debug("WelcomPageView._startAct1", "Screen created for Act 1", 
                           width=screen_info.current_w, height=screen_info.current_h)
            except Exception as e:
                Logger.error("WelcomPageView._startAct1", e)
                raise
            
            # Create and run Act 1 view
            try:
                act1_view = Act1View(screen)
                result = act1_view.run()
                Logger.debug("WelcomPageView._startAct1", "Act 1 completed", result=result)
                
                # Handle Act 1 result (for future expansion)
                if result == "ACT2":
                    Logger.debug("WelcomPageView._startAct1", "Act 2 should start (not yet implemented)")
                elif result == "GAME_OVER":
                    Logger.debug("WelcomPageView._startAct1", "Game over")
                elif result == "QUIT":
                    Logger.debug("WelcomPageView._startAct1", "Quit requested")
                    
            except Exception as e:
                Logger.error("WelcomPageView._startAct1", e)
                raise
            
        except Exception as e:
            Logger.error("WelcomPageView._startAct1", e)
            try:
                pygame.quit()
            except Exception:
                pass
            raise
