"""
TileModel Module

Represents individual tiles used in the game map.
Manages tile properties like name, image, and collision (solid) status.
"""

import pygame
from Utils.Logger import Logger


# === TILE MODEL CLASS ===

class TileModel:
    """
    Model for map tiles.
    Stores tile name, image, and whether the tile is solid (collidable).
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, name, image, is_solid):
        """
        Initialize the tile model.
        
        Args:
            name: Tile name/identifier
            image: Path to tile image file
            is_solid: Whether the tile is solid (collidable)
        """
        try:
            self.name = name
            self.is_solid = is_solid
            
            # Load tile image
            try:
                self.image = pygame.image.load(image)
                Logger.debug("TileModel.__init__", "Tile image loaded", name=name, image=image)
            except FileNotFoundError as e:
                Logger.error("TileModel.__init__", e)
                # Create a default surface if image not found
                self.image = pygame.Surface((32, 32))
                self.image.fill((128, 128, 128))
                Logger.debug("TileModel.__init__", "Using default tile surface")
            except Exception as e:
                Logger.error("TileModel.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("TileModel.__init__", e)
            raise