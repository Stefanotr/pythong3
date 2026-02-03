"""
MapView Module

Handles the visual representation of the game map.
Renders tiles from the map model to the screen.
"""

import pygame
from Utils.Logger import Logger


# === MAP VIEW CLASS ===

class MapView:
    """
    View class for rendering the game map.
    Draws all tiles from the map model to the screen.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, map):
        """
        Initialize the map view.
        
        Args:
            map: MapModel instance containing tile data
        """
        try:
            self.map = map
            Logger.debug("MapView.__init__", "Map view initialized", 
                        tile_count=len(map.tiles) if hasattr(map, 'tiles') else 0)
        except Exception as e:
            Logger.error("MapView.__init__", e)
            raise
    
    # === RENDERING ===
    
    def draw(self, screen):
        """
        Draw the map to the screen.
        Should be called every frame.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            # Render each tile
            try:
                for y, row in enumerate(self.map.tiles):
                    for x, tile in enumerate(row):
                        try:
                            location = (x * self.map.tile_size, y * self.map.tile_size)
                            
                            # Get tile image
                            if tile in self.map.tile_kinds:
                                image = self.map.tile_kinds[tile].image
                                screen.blit(image, location)
                            else:
                                Logger.debug("MapView.draw", "Unknown tile type", tile=tile, position=(x, y))
                                
                        except Exception as e:
                            Logger.error("MapView.draw", e)
                            # Continue rendering other tiles even if one fails
                            continue
                            
            except AttributeError as e:
                Logger.error("MapView.draw", e)
                Logger.debug("MapView.draw", "Map model missing required attributes")
            except Exception as e:
                Logger.error("MapView.draw", e)
                
        except Exception as e:
            Logger.error("MapView.draw", e)