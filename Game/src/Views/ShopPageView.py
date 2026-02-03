"""
ShopPageView Module

Handles the visual representation of the shop page.
Displays shop interface for purchasing items.
"""

import pygame
import sys
from Utils.Logger import Logger


# === SHOP PAGE VIEW CLASS ===

class ShopPageView:
    """
    View class for rendering the shop interface.
    Displays shop background and handles shop UI rendering.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self):
        """
        Initialize the shop page view.
        Sets up the display window and loads background image.
        """
        try:
            # Initialize pygame
            try:
                pygame.init()
                Logger.debug("ShopPageView.__init__", "Pygame initialized")
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                raise
            
            # Create display surface
            try:
                self.screen = pygame.display.set_mode((800, 800))
                pygame.display.set_caption("Shop du jeux")
                Logger.debug("ShopPageView.__init__", "Display surface created", size=(800, 800))
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                raise
            
            # Load background image
            try:
                self.background = pygame.image.load('Game/Assets/Shop.png')
                self.background = pygame.transform.scale(self.background, (800, 800))
                Logger.debug("ShopPageView.__init__", "Background image loaded")
            except FileNotFoundError as e:
                Logger.error("ShopPageView.__init__", e)
                # Create default background if image not found
                self.background = pygame.Surface((800, 800))
                self.background.fill((50, 50, 50))
                Logger.debug("ShopPageView.__init__", "Using default background")
            except Exception as e:
                Logger.error("ShopPageView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("ShopPageView.__init__", e)
            raise

    # === RENDERING ===
    
    def draw(self):
        """
        Draw the shop background to the screen.
        Should be called each frame to render the shop view.
        """
        try:
            self.screen.blit(self.background, (0, 0))
        except Exception as e:
            Logger.error("ShopPageView.draw", e)
