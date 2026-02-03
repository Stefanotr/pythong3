"""
PlayerController Module

Handles player input and movement.
Manages keyboard controls for player character movement and actions.
"""

import pygame
from Utils.Logger import Logger


# === PLAYER CONTROLLER CLASS ===

class PlayerController:
    """
    Controller class for handling player input and movement.
    Processes keyboard events and updates player position and state.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, screen, player):
        """
        Initialize the player controller.
        
        Args:
            screen: Pygame surface for rendering
            player: PlayerModel instance to control
        """
        try:
            self.player = player
            # Get screen dimensions for boundary checking
            screen_width, screen_height = screen.get_size()
            self.SCREEN_SIZE = max(screen_width, screen_height)  # Use larger dimension
            self.PLAYER_SIZE = 50
            self.SPEED = 10
            self.screen_width = screen_width
            self.screen_height = screen_height
            Logger.debug("PlayerController.__init__", "Player controller initialized", player_name=player.getName())
        except Exception as e:
            Logger.error("PlayerController.__init__", e)
            raise

    # === INPUT HANDLING ===
    
    def handleInput(self, event):
        """
        Handle keyboard input events for player movement and actions.
        
        Args:
            event: Pygame event object
        """
        try:
            if event.type == pygame.KEYDOWN:
                try:
                    current_x = self.player.getX()
                    current_y = self.player.getY()
                except Exception as e:
                    Logger.error("PlayerController.handleInput", e)
                    return

                # === MOVEMENT CONTROLS ===
                
                # LEFT
                if event.key == pygame.K_LEFT:
                    try:
                        if current_x > 0:
                            self.player.setX(current_x - self.SPEED)
                            Logger.debug("PlayerController.handleInput", "Player moved left", x=self.player.getX())
                    except Exception as e:
                        Logger.error("PlayerController.handleInput", e)

                # RIGHT
                elif event.key == pygame.K_RIGHT:
                    try:
                        # Allow movement within map bounds (no hard limit for now)
                        self.player.setX(current_x + self.SPEED)
                        Logger.debug("PlayerController.handleInput", "Player moved right", x=self.player.getX())
                    except Exception as e:
                        Logger.error("PlayerController.handleInput", e)

                # UP
                elif event.key == pygame.K_UP:
                    try:
                        if current_y > 0:
                            self.player.setY(current_y - self.SPEED)
                            Logger.debug("PlayerController.handleInput", "Player moved up", y=self.player.getY())
                    except Exception as e:
                        Logger.error("PlayerController.handleInput", e)

                # DOWN
                elif event.key == pygame.K_DOWN:
                    try:
                        # Allow movement within map bounds (no hard limit for now)
                        self.player.setY(current_y + self.SPEED)
                        Logger.debug("PlayerController.handleInput", "Player moved down", y=self.player.getY())
                    except Exception as e:
                        Logger.error("PlayerController.handleInput", e)

                # === ACTION CONTROLS ===
                
                # DRINK (B)
                if event.key == pygame.K_b:
                    try:
                        selected_bottle = self.player.getSelectedBottle()
                        if selected_bottle:
                            self.player.drink(selected_bottle)
                            Logger.debug("PlayerController.handleInput", "Player drank", 
                                       bottle=selected_bottle.getName(), 
                                       drunkenness=self.player.getDrunkenness())
                        else:
                            Logger.debug("PlayerController.handleInput", "No bottle selected")
                    except Exception as e:
                        Logger.error("PlayerController.handleInput", e)
                        
        except Exception as e:
            Logger.error("PlayerController.handleInput", e)