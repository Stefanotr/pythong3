"""
PageView Module

Base class for all page views in the game.
Provides common functionality for window creation, background loading, and rendering.
"""

import pygame
import os
from Utils.Logger import Logger


# === PAGE VIEW BASE CLASS ===

class PageView:
    """
    Base class for all page views.
    Handles window initialization, background image loading, and basic drawing functionality.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name="none", width=800, height=800, RESIZABLE=0, backgroud_image="Game/Assets/welcomePage.png"):
        """
        Initialize the page view with window settings and background image.
        
        Args:
            name: Window title/caption
            width: Window width in pixels
            height: Window height in pixels
            RESIZABLE: Pygame flag for window resizability (0 or pygame.RESIZABLE)
            backgroud_image: Path to background image file
        """
        try:
            Logger.debug("PageView.__init__", "Initializing page view", name=name, width=width, height=height)
            
            # Set window position to center
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except Exception as e:
                Logger.error("PageView.__init__", e)
            
            # Initialize pygame
            try:
                pygame.init()
                Logger.debug("PageView.__init__", "Pygame initialized")
            except Exception as e:
                Logger.error("PageView.__init__", e)
                raise
            
            # Store properties
            self.name = name
            self.width = width
            self.height = height
            self.resizable = RESIZABLE
            self.backgroud_image = backgroud_image

            # Create display surface
            try:
                self.screen = pygame.display.set_mode((self.width, self.height), self.resizable)
                pygame.display.set_caption(self.name)
                Logger.debug("PageView.__init__", "Display surface created", size=(width, height))
            except Exception as e:
                Logger.error("PageView.__init__", e)
                raise
            
            # Load original background image (store for rescaling)
            try:
                self._original_background = pygame.image.load(self.backgroud_image)
                # Scale to initial window size
                self.background = pygame.transform.scale(self._original_background, (self.width, self.height))
                Logger.debug("PageView.__init__", "Background image loaded", path=backgroud_image)
            except FileNotFoundError as e:
                Logger.error("PageView.__init__", e)
                # Create a default black background if image not found
                self._original_background = None
                self.background = pygame.Surface((self.width, self.height))
                self.background.fill((0, 0, 0))
                Logger.debug("PageView.__init__", "Using default black background")
            except Exception as e:
                Logger.error("PageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("PageView.__init__", e)
            raise

    # === BACKGROUND RESCALING ===
    
    def rescaleBackground(self, new_width, new_height):
        """
        Rescale the background image to match new window dimensions.
        
        Args:
            new_width: New window width in pixels
            new_height: New window height in pixels
        """
        try:
            # Update stored dimensions
            self.width = new_width
            self.height = new_height
            
            # Rescale background if original image exists
            if self._original_background is not None:
                self.background = pygame.transform.scale(self._original_background, (new_width, new_height))
                Logger.debug("PageView.rescaleBackground", "Background rescaled", 
                           width=new_width, height=new_height)
            else:
                # Create new default background if no original image
                self.background = pygame.Surface((new_width, new_height))
                self.background.fill((0, 0, 0))
                Logger.debug("PageView.rescaleBackground", "Default background resized", 
                           width=new_width, height=new_height)
        except Exception as e:
            Logger.error("PageView.rescaleBackground", e)

    # === RENDERING ===
    
    def draw(self):
        """
        Draw the background image to the screen.
        Should be called at the start of each frame's rendering.
        """
        try:
            # Get current screen size to ensure background matches
            current_width, current_height = self.screen.get_size()
            
            # Rescale if dimensions don't match
            if current_width != self.width or current_height != self.height:
                self.rescaleBackground(current_width, current_height)
            
            # Draw background, scaling to fit if needed
            try:
                self.screen.blit(self.background, (0, 0))
            except Exception as e:
                # If blit fails, try rescaling and blitting again
                Logger.debug("PageView.draw", "Blit failed, rescaling background", error=str(e))
                self.rescaleBackground(current_width, current_height)
                self.screen.blit(self.background, (0, 0))
        except Exception as e:
            Logger.error("PageView.draw", e)