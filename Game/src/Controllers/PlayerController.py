"""
PlayerController Module

Handles player input and movement.
Manages keyboard controls for player character movement and actions.
"""

import pygame
from Utils.Logger import Logger
from Controllers import BaseController


# === PLAYER CONTROLLER CLASS ===

class PlayerController(BaseController):
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

    # === INPUT HANDLING (EVENT-BASED) ===

    def handle_input(self, event):
        """
        Handle keyboard input events for player movement and actions.
        
        Args:
            event: Pygame event object
        """
        try:
            if event.type != pygame.KEYDOWN:
                return

            # === ACTION CONTROLS === (ponctuels)
            if event.key == pygame.K_b:
                try:
                    selected_bottle = self.player.getSelectedBottle()
                    if selected_bottle:
                        self.player.drink(selected_bottle)
                        Logger.debug(
                            "PlayerController.handle_input",
                            "Player drank",
                            bottle=selected_bottle.getName(),
                            drunkenness=self.player.getDrunkenness(),
                        )
                    else:
                        Logger.debug("PlayerController.handle_input", "No bottle selected")
                except Exception as e:
                    Logger.error("PlayerController.handle_input", e)
        except Exception as e:
            Logger.error("PlayerController.handle_input", e)

    # Backwards compatible alias
    def handleInput(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handle_input(event)

    # === INPUT HANDLING (FRAME-BASED) ===

    def handle_events(self, events):
        """
        Handle continuous input each frame (movement while keys are held).

        Args:
            events: iterable of pygame events (unused here but kept for API compatibility)
        """
        try:
            keys = pygame.key.get_pressed()

            dx = 0
            dy = 0

            # Support both arrows and WASD
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= self.SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += self.SPEED
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy -= self.SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy += self.SPEED

            if dx == 0 and dy == 0:
                return

            try:
                current_x = self.player.getX()
                current_y = self.player.getY()
            except Exception as e:
                Logger.error("PlayerController.handle_events", e)
                return

            new_x = current_x + dx
            new_y = current_y + dy

            # Simple boundary checks (no hard map limits for now)
            if new_x < 0:
                new_x = 0
            if new_y < 0:
                new_y = 0

            try:
                self.player.setX(new_x)
                self.player.setY(new_y)
                Logger.debug(
                    "PlayerController.handle_events",
                    "Player moved",
                    x=self.player.getX(),
                    y=self.player.getY(),
                )
            except Exception as e:
                Logger.error("PlayerController.handle_events", e)
        except Exception as e:
            Logger.error("PlayerController.handle_events", e)