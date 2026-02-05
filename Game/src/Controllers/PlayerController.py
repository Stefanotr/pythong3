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
    
    def __init__(self, screen, player, collision_rects=None, map_width=None, map_height=None):
        """
        Initialize the player controller.
        
        Args:
            screen: Pygame surface for rendering
            player: PlayerModel instance to control
            collision_rects: optional list of pygame.Rect in world coordinates to collide against
            map_width: optional map width in pixels to enforce boundary limits
            map_height: optional map height in pixels to enforce boundary limits
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
            
            # Map boundaries to prevent player from leaving map
            self.map_width = map_width
            self.map_height = map_height
            
            Logger.debug("PlayerController.__init__", "Player controller initialized", player_name=player.getName(), collisions=len(self.collision_rects), map_bounds=(map_width, map_height))
        except Exception as e:
            Logger.error("PlayerController.__init__", e)
            raise

    # === INPUT HANDLING (EVENT-BASED) ===

    def handleInput(self, event):
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
                        Logger.debug("PlayerController.handleInput", "No bottle selected")
                except Exception as e:
                    Logger.error("PlayerController.handleInput", e)
        except Exception as e:
            Logger.error("PlayerController.handleInput", e)

    # Backward compatible alias
    def handle_input(self, event):
        """Legacy alias keeping existing calls working."""
        return self.handleInput(event)

    # === INPUT HANDLING (FRAME-BASED) ===

    def handleEvents(self, events):
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
                return

            try:
                current_x = self.player.getX()
                current_y = self.player.getY()
            except Exception as e:
                Logger.error("PlayerController.handleEvents", e)
                return

            new_x = current_x + dx
            new_y = current_y + dy

            # Boundary checks to keep player within map
            half = self.PLAYER_SIZE // 2
            if new_x < half:
                new_x = half
            if new_y < half:
                new_y = half
            
            # Apply map boundaries if provided
            if self.map_width is not None and new_x + half > self.map_width:
                new_x = self.map_width - half
            if self.map_height is not None and new_y + half > self.map_height:
                new_y = self.map_height - half

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
                    "PlayerController.handleEvents",
                    "Player moved",
                    x=self.player.getX(),
                    y=self.player.getY(),
                )
            except Exception as e:
                Logger.error("PlayerController.handleEvents", e)
        except Exception as e:
            Logger.error("PlayerController.handleEvents", e)

    # Backward compatible alias
    def handle_events(self, events):
        """Legacy alias keeping existing calls working."""
        return self.handleEvents(events)