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
    
    def __init__(self, screen, player, collision_rects=None):
        """
        Initialize the player controller.
        
        Args:
            screen: Pygame surface for rendering
            player: PlayerModel instance to control
            collision_rects: optional list of pygame.Rect in world coordinates to collide against
        """
        try:
            self.player = player
            # Collision rectangles in world coordinates
            self.collision_rects = collision_rects if collision_rects is not None else []

            # Get screen dimensions for boundary checking
            screen_width, screen_height = screen.get_size()
            self.SCREEN_SIZE = max(screen_width, screen_height)  # Use larger dimension
            self.PLAYER_SIZE = 50
            self.SPEED = 6  # reduced speed for better control
            self.screen_width = screen_width
            self.screen_height = screen_height
            Logger.debug("PlayerController.__init__", "Player controller initialized", player_name=player.getName(), collisions=len(self.collision_rects))
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

            # Support both arrows and ZQSD (French keyboard layout)
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                dx -= self.SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += self.SPEED
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                dy -= self.SPEED
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy += self.SPEED

            if dx == 0 and dy == 0:
                # No movement: return to idle action
                try:
                    self.player.setCurrentAction("idle")
                except Exception as e:
                    Logger.error("PlayerController.handle_events", e)
                return
            
            # Set directional moving action for animation
            try:
                if dx < 0:
                    self.player.setCurrentAction("moving_left", duration=10)
                elif dx > 0:
                    self.player.setCurrentAction("moving_right", duration=10)
                else:
                    # Movement vertical seulement: keep current action or default to moving_right
                    action = self.player.getCurrentAction()
                    if action not in ["moving_left", "moving_right"]:
                        self.player.setCurrentAction("moving_right", duration=10)
            except Exception as e:
                Logger.error("PlayerController.handle_events", e)

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

            # Prepare player rectangle for collision checks (player coords are center)
            half = self.PLAYER_SIZE // 2

            # Axis-separated collision handling to allow sliding along obstacles
            resolved_x = current_x
            resolved_y = current_y

            # Test X movement first
            try:
                rect_x = pygame.Rect(new_x - half, current_y - half, self.PLAYER_SIZE, self.PLAYER_SIZE)
                collided_x = any(rect_x.colliderect(r) for r in self.collision_rects)
                if not collided_x:
                    resolved_x = new_x
                else:
                    Logger.debug("PlayerController.handle_events", "Collision on X axis prevented movement")
            except Exception as e:
                Logger.error("PlayerController.collision_x", e)

            # Test Y movement with the (possibly) resolved x
            try:
                rect_y = pygame.Rect(resolved_x - half, new_y - half, self.PLAYER_SIZE, self.PLAYER_SIZE)
                collided_y = any(rect_y.colliderect(r) for r in self.collision_rects)
                if not collided_y:
                    resolved_y = new_y
                else:
                    Logger.debug("PlayerController.handle_events", "Collision on Y axis prevented movement")
            except Exception as e:
                Logger.error("PlayerController.collision_y", e)

            try:
                self.player.setX(resolved_x)
                self.player.setY(resolved_y)
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