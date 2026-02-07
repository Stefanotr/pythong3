"""
PauseMenuView Module

Displays the pause menu overlay with Continue, Main Menu, and Quit options.
Based on WelcomePageView design.
"""

import pygame
from Utils.Logger import Logger
from Controllers.ButtonController import ButtonController
from Controllers.PauseMenuController import PauseMenuController
from Controllers.GameState import GameState
from Views.ButtonView import ButtonView


# === PAUSE MENU VIEW CLASS ===

class PauseMenuView:
    """
    Pause menu view displaying pause options.
    Provides navigation to continue game, return to main menu, or quit.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen):
        """
        Initialize the pause menu view.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            self.screen = screen
            self.screen_width = screen.get_width()
            self.screen_height = screen.get_height()
            
            Logger.debug("PauseMenuView.__init__", "Pause menu initialized", 
                        width=self.screen_width, height=self.screen_height)
            
            # === BUTTON INITIALIZATION ===

            self.buttons = []
            self.buttons_controllers = []
            
            # Calculate button positions (centered vertically)
            button_y_start = self.screen_height // 2 - 120
            button_spacing = 100
            
            # Pre-calculate sizes and positions
            continue_size = (188, 75)
            menu_size = (188, 75)
            quit_size = (188, 75)
            logout_size = (188, 75)
            
            continue_y = button_y_start
            menu_y = button_y_start + button_spacing
            quit_y = button_y_start + button_spacing * 2
            logout_y = button_y_start + button_spacing * 3
            
            # Continue button
            try:
                self.continue_button = ButtonView(
                    image_path='Game/Assets/buttonPlay.png',  # Reuse play button image
                    position=(self.screen_width // 2, continue_y),
                    size=continue_size
                )
                self.buttons.append(self.continue_button)
                
                continue_button_controller = ButtonController(self.continue_button, "continue_game")
                self.buttons_controllers.append(continue_button_controller)
                Logger.debug("PauseMenuView.__init__", "Continue button created")
            except Exception as e:
                Logger.error("PauseMenuView.__init__", e)
                self.continue_button = None
            
            # Main Menu button (should return to WelcomeView)
            try:
                self.menu_button = ButtonView(
                    image_path='Game/Assets/buttonMainMenu.png',
                    position=(self.screen_width // 2, menu_y),
                    size=menu_size
                )
                self.buttons.append(self.menu_button)
                
                menu_button_controller = ButtonController(self.menu_button, "main_menu")
                self.buttons_controllers.append(menu_button_controller)
                Logger.debug("PauseMenuView.__init__", "Main Menu button created")
            except Exception as e:
                Logger.error("PauseMenuView.__init__", e)
                self.menu_button = None
            
            # Quit button - Quitter complètement le jeu
            try:
                self.quit_button = ButtonView(
                    image_path='Game/Assets/buttonQuit.png',
                    position=(self.screen_width // 2, quit_y),
                    size=quit_size
                )
                self.buttons.append(self.quit_button)
                
                quit_button_controller = ButtonController(self.quit_button, "quit_game")
                self.buttons_controllers.append(quit_button_controller)
                Logger.debug("PauseMenuView.__init__", "Quit button created")
            except Exception as e:
                Logger.error("PauseMenuView.__init__", e)
                self.quit_button = None
            
            # Logout button - simple rectangle with text (no image)
            try:
                logout_size = (225, 50)
                logout_x = self.screen_width // 2 - logout_size[0] // 2
                self.logout_button = pygame.Rect(
                    logout_x,
                    logout_y - logout_size[1] // 2,
                    logout_size[0],
                    logout_size[1]
                )
                self.logout_button_text = "Déconnexion"
                Logger.debug("PauseMenuView.__init__", "Logout button created as simple rectangle")
            except Exception as e:
                Logger.error("PauseMenuView.__init__", e)
                self.logout_button = None
            
            # Font setup
            try:
                self.title_font = pygame.font.SysFont("Arial", 72, bold=True)
                self.button_font = pygame.font.SysFont("Arial", 36, bold=True)
            except Exception as e:
                Logger.error("PauseMenuView.__init__", e)
                self.title_font = pygame.font.Font(None, 72)
                self.button_font = pygame.font.Font(None, 36)

            # === CONTROLLER INITIALIZATION ===
            try:
                self.controller = PauseMenuController(self.buttons_controllers)
            except Exception as e:
                Logger.error("PauseMenuView.__init__", e)
                self.controller = None
                
        except Exception as e:
            Logger.error("PauseMenuView.__init__", e)
            raise
    
    def handle_logout(self, events):
        """
        Handle logout button click for pause menu.
        
        Args:
            events: pygame events
            
        Returns:
            bool: True if logout button was clicked, False otherwise
        """
        try:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        if self.logout_button.collidepoint(event.pos):
                            Logger.debug("PauseMenuView.handle_logout", "Logout button clicked")
                            return True
            return False
        except Exception as e:
            Logger.error("PauseMenuView.handle_logout", e)
            return False

    # === MAIN LOOP ===
    
    def run(self):
        """
        Main loop for the pause menu.
        Handles events and returns the selected action.
        
        Returns:
            str: Selected action ("continue", "main_menu", or "quit")
        """
        try:
            clock = pygame.time.Clock()
            running = True
            result = None
            Logger.debug("PauseMenuView.run", "Pause menu loop started")
            
            while running:
                try:
                    events = pygame.event.get()
                    
                    # === CHECK LOGOUT BUTTON FIRST ===
                    if self.logout_button and self.handle_logout(events):
                        result = GameState.LOGOUT.value
                        running = False
                    # === INPUT HANDLING VIA CONTROLLER ===
                    elif self.controller is not None:
                        try:
                            action = self.controller.handle_events(events)
                        except Exception as e:
                            Logger.error("PauseMenuView.run", e)
                            action = None

                        if action is not None:
                            result = action
                            running = False
                    else:
                        # Fallback: basic quit handling
                        for event in events:
                            if event.type == pygame.QUIT:
                                result = GameState.QUIT.value
                                running = False

                    # === RENDERING ===
                    
                    try:
                        self.draw()
                    except Exception as e:
                        Logger.error("PauseMenuView.run", e)
                    
                    pygame.display.flip()
                    clock.tick(60)
                    
                except Exception as e:
                    Logger.error("PauseMenuView.run", e)
                    continue
            
            Logger.debug("PauseMenuView.run", "Pause menu closed", result=result)
            return result if result else GameState.CONTINUE.value
            
        except Exception as e:
            Logger.error("PauseMenuView.run", e)
            return GameState.CONTINUE.value
    
    # === RENDERING ===
    
    def draw(self):
        """
        Draw the pause menu overlay.
        Renders semi-transparent background, title, and buttons.
        """
        try:
            # Draw semi-transparent overlay
            try:
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))  # Black with 100 alpha (60% transparent, 40% opaque)
                self.screen.blit(overlay, (0, 0))
            except Exception as e:
                Logger.error("PauseMenuView.draw", e)
            
            # Draw title
            try:
                title_text = "PAUSED"
                title_surf = self.title_font.render(title_text, True, (255, 215, 0))  # Gold color
                title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
                
                title_x = self.screen_width // 2 - title_surf.get_width() // 2
                title_y = self.screen_height // 4
                
                self.screen.blit(title_shadow, (title_x + 3, title_y + 3))
                self.screen.blit(title_surf, (title_x, title_y))
            except Exception as e:
                Logger.error("PauseMenuView.draw", e)
            
            # Draw buttons (only images, no text overlay to avoid superposition)
            try:
                for button in self.buttons:
                    if button:
                        try:
                            button.draw(self.screen)
                        except Exception as e:
                            Logger.error("PauseMenuView.draw", e)
                            continue
            except Exception as e:
                Logger.error("PauseMenuView.draw", e)
            
            # Draw logout button (simple rectangle with text)
            try:
                if self.logout_button:
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
                    font = pygame.font.SysFont("Arial", 18)
                    text_surf = font.render(self.logout_button_text, True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=self.logout_button.center)
                    self.screen.blit(text_surf, text_rect)
            except Exception as e:
                Logger.error("PauseMenuView.draw - logout button", e)
                
        except Exception as e:
            Logger.error("PauseMenuView.draw", e)

