"""
ButtonView Module

Handles the visual representation of buttons.
Manages button image loading, scaling, and rendering.
"""

import pygame
from Utils.Logger import Logger


# === BUTTON VIEW CLASS ===

class ButtonView:
    """
    Reusable class for creating clickable button views.
    Handles button image loading, positioning, and rendering.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, image_path, position, size=(200, 80)):
        """
        Initialize the button view with an image and position.
        
        Args:
            image_path: Path to the button image file
            position: Tuple (x, y) representing the button center position
        """
        try:
            # Load and scale button image
            try:
                self.image = pygame.image.load(image_path)
                # Scale to requested size
                self.image = pygame.transform.scale(self.image, size)
                Logger.debug("ButtonView.__init__", "Button image loaded", path=image_path, size=size)
            except FileNotFoundError as e:
                Logger.error("ButtonView.__init__", e)
                # Create a default button surface if image not found
                self.image = pygame.Surface(size)
                self.image.fill((128, 128, 128))
                Logger.debug("ButtonView.__init__", "Using default button surface")
            except Exception as e:
                Logger.error("ButtonView.__init__", e)
                raise
            
            # Create rectangle for collision detection
            try:
                self.rect = self.image.get_rect(center=position)
                Logger.debug("ButtonView.__init__", "Button rectangle created", position=position)
            except Exception as e:
                Logger.error("ButtonView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("ButtonView.__init__", e)
            raise
    
    # === RENDERING ===
    
    def draw(self, screen):
        """
        Draw the button to the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            # Avoid errors when display has been closed
            if not pygame.get_init() or pygame.display.get_surface() is None:
                return

            screen.blit(self.image, self.rect)
        except Exception as e:
            Logger.error("ButtonView.draw", e)