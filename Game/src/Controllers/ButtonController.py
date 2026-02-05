"""
ButtonController Module

Handles button click events and actions for UI buttons.
Manages transitions between game states and user interactions.
"""

import pygame
import sys
from Utils.Logger import Logger
from Controllers import BaseController
from Controllers.GameState import GameState


# === BUTTON CONTROLLER CLASS ===

class ButtonController(BaseController):
    """
    Reusable controller class for creating clickable buttons.
    Handles button click detection and executes associated actions.
    """
    
    def __init__(self, button, action=None):
        """
        Initialize the button controller.
        
        Args:
            button: ButtonView instance to control
            action: String identifier for the action (e.g., "start_game", "quit_game")
        """
        try:
            self.action = action
            self.button = button
            Logger.debug("ButtonController.__init__", "Button controller initialized", action=action)
        except Exception as e:
            Logger.error("ButtonController.__init__", e)
            raise
    
    # === CLICK DETECTION ===
    
    def isClicked(self, mouse_pos):
        """
        Check if the button is clicked at the given mouse position.
        
        Args:
            mouse_pos: Tuple (x, y) representing mouse position
            
        Returns:
            bool: True if button is clicked, False otherwise
        """
        try:
            is_clicked = self.button.rect.collidepoint(mouse_pos)
            Logger.debug("ButtonController.isClicked", "Button click checked", clicked=is_clicked)
            return is_clicked
        except Exception as e:
            Logger.error("ButtonController.isClicked", e)
            return False
    
    # === ACTION HANDLING ===
    
    def handleClick(self):
        """
        Execute the action associated with the button.
        
        Returns:
            str: Action identifier ("start_game", "quit_game", or None)
        """
        try:
            Logger.debug("ButtonController.handleClick", "Button click handled", action=self.action)
            
            if self.action == "start_game":
                Logger.debug("ButtonController.handleClick", "Start game action triggered")
                return GameState.START_GAME.value
            elif self.action == "quit_game":
                Logger.debug("ButtonController.handleClick", "Quit game action triggered")
                self.quitGame()
                return GameState.QUIT.value
            
            return None
        except Exception as e:
            Logger.error("ButtonController.handleClick", e)
            return None
    
    # === EVENT HANDLING ===

    def handleInput(self, event):
        """
        Handle all menu events, including button clicks.
        
        Args:
            event: Pygame event object
            
        Returns:
            str: Action identifier if button was clicked, None otherwise
        """
        try:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.isClicked(mouse_pos):
                    Logger.debug("ButtonController.handleInput", "Button clicked, handling action")
                    return self.handleClick()

            return None
        except Exception as e:
            Logger.error("ButtonController.handleInput", e)
            return None

    # Backward compatible alias
    def handle_input(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handleInput(event)

    # Backwards compatible alias
    def handleEvents(self, event):
        """
        Legacy alias used by existing views.
        """
        return self.handleInput(event)

    # === GAME STATE ACTIONS ===
    
    def quitGame(self):
        """
        Quit the game properly.
        Closes pygame and exits the application.
        """
        try:
            Logger.debug("ButtonController.quitGame", "Quitting game")
            pygame.quit()
            sys.exit()
        except Exception as e:
            Logger.error("ButtonController.quitGame", e)
            sys.exit(1)
    




    