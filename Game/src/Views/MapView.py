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
    
    # === INITIALIZATION AND RENDERING ===
    
    def __init__(self, screen, map):
        """
        Initialize and render the map view.
        Draws all tiles from the map model to the screen.
        
        Args:
            screen: Pygame surface to draw on
            map: MapModel instance containing tile data
        """
        try:
            Logger.debug("MapView.__init__", "Rendering map", tile_count=len(map.tiles) if hasattr(map, 'tiles') else 0)
            
            # Render each tile
            try:
                for y, row in enumerate(map.tiles):
                    for x, tile in enumerate(row):
                        try:
                            location = (x * map.tile_size, y * map.tile_size)
                            
                            # Get tile image
                            if tile in map.tile_kinds:
                                image = map.tile_kinds[tile].image
                                screen.blit(image, location)
                            else:
                                Logger.debug("MapView.__init__", "Unknown tile type", tile=tile, position=(x, y))
                                
                        except Exception as e:
                            Logger.error("MapView.__init__", e)
                            # Continue rendering other tiles even if one fails
                            continue
                            
                Logger.debug("MapView.__init__", "Map rendering completed")
                
            except AttributeError as e:
                Logger.error("MapView.__init__", e)
                Logger.debug("MapView.__init__", "Map model missing required attributes")
            except Exception as e:
                Logger.error("MapView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("MapView.__init__", e)
            raise