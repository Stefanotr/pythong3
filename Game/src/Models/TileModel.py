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
            
            # Load tile image with alpha-support when possible
            try:
                surf = pygame.image.load(image)
                try:
                    self.image = surf.convert_alpha()
                    Logger.debug("TileModel.__init__", "Tile image loaded with alpha", name=name, image=image)
                except Exception:
                    try:
                        surf2 = surf.convert()
                        col = surf2.get_at((0, 0))
                        surf2.set_colorkey(col)
                        self.image = surf2
                        Logger.debug("TileModel.__init__", "Tile image loaded without alpha - colorkey set", name=name, image=image, colorkey=col)
                    except Exception:
                        # Fallback to original surface
                        self.image = surf
                        Logger.debug("TileModel.__init__", "Tile image loaded without conversion", name=name, image=image)
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
    
    # === GETTERS / SETTERS ===
    
    def getName(self):
        """
        Get the tile name.
        
        Returns:
            str: Tile name/identifier
        """
        try:
            return self.name
        except Exception as e:
            Logger.error("TileModel.getName", e)
            return ""
    
    def setName(self, name):
        """
        Set the tile name.
        
        Args:
            name: Tile name/identifier
        """
        try:
            self.name = str(name)
            Logger.debug("TileModel.setName", "Tile name set", name=self.name)
        except Exception as e:
            Logger.error("TileModel.setName", e)
    
    def getImage(self):
        """
        Get the tile image surface.
        
        Returns:
            pygame.Surface: Tile image surface
        """
        try:
            return self.image
        except Exception as e:
            Logger.error("TileModel.getImage", e)
            # Return default surface if error
            default = pygame.Surface((32, 32))
            default.fill((128, 128, 128))
            return default
    
    def setImage(self, image):
        """
        Set the tile image.
        
        Args:
            image: Either a path string to image file or a pygame.Surface
        """
        try:
            if isinstance(image, str):
                # Load from file path with alpha support when possible
                try:
                    surf = pygame.image.load(image)
                    try:
                        self.image = surf.convert_alpha()
                        Logger.debug("TileModel.setImage", "Tile image loaded with alpha", path=image)
                    except Exception:
                        try:
                            surf2 = surf.convert()
                            col = surf2.get_at((0, 0))
                            surf2.set_colorkey(col)
                            self.image = surf2
                            Logger.debug("TileModel.setImage", "Tile image loaded without alpha - colorkey set", path=image, colorkey=col)
                        except Exception:
                            self.image = surf
                            Logger.debug("TileModel.setImage", "Tile image loaded without conversion", path=image)
                except Exception as e:
                    Logger.error("TileModel.setImage", e)
            elif isinstance(image, pygame.Surface):
                # Use provided surface
                self.image = image
                Logger.debug("TileModel.setImage", "Tile image set from surface")
            else:
                Logger.error("TileModel.setImage", TypeError("Image must be a file path string or pygame.Surface"))
        except Exception as e:
            Logger.error("TileModel.setImage", e)
    
    def getIsSolid(self):
        """
        Get whether the tile is solid (collidable).
        
        Returns:
            bool: True if tile is solid, False otherwise
        """
        try:
            return self.is_solid
        except Exception as e:
            Logger.error("TileModel.getIsSolid", e)
            return False
    
    def setIsSolid(self, is_solid):
        """
        Set whether the tile is solid (collidable).
        
        Args:
            is_solid: True if tile is solid, False otherwise
        """
        try:
            self.is_solid = bool(is_solid)
            Logger.debug("TileModel.setIsSolid", "Tile solid status set", is_solid=self.is_solid)
        except Exception as e:
            Logger.error("TileModel.setIsSolid", e)