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
    
    def draw(self, screen, offset=(0, 0)):
        """
        Draw the map to the screen with optional offset (camera).
        Should be called every frame.

        Args:
            screen: Pygame surface to draw on
            offset: Tuple (offset_x, offset_y) to offset the map rendering
        """
        try:
            offset_x, offset_y = offset
            # Render each tile
            try:
                for y, row in enumerate(self.map.tiles):
                    for x, tile in enumerate(row):
                        try:
                            location = (x * self.map.tile_size + offset_x, y * self.map.tile_size + offset_y)

                            # Get tile image
                            if tile in self.map.tile_kinds:
                                image = self.map.tile_kinds[tile].image
                                screen.blit(image, location)
                            else:
                                # Draw a placeholder rect so missing tiles are visible (avoid black holes)
                                try:
                                    if not hasattr(self, '_unknown_gids'):
                                        self._unknown_gids = set()
                                    if tile not in self._unknown_gids:
                                        self._unknown_gids.add(tile)
                                        Logger.debug("MapView.draw", "Unknown tile type, drawing placeholder", tile=tile, position=(x, y))
                                    color = ((tile * 37) % 256, (tile * 61) % 256, (tile * 97) % 256) if isinstance(tile, int) else (150, 0, 150)
                                    rect = (location[0], location[1], self.map.tile_size, self.map.tile_size)
                                    pygame.draw.rect(screen, color, rect)
                                except Exception as e:
                                    Logger.error("MapView.draw.placeholder", e)
                        except Exception as e:
                            Logger.error("MapView.draw.tile", e)
                            # Continue with next tile even if one tile draw failed
                            continue
            except Exception as e:
                Logger.error("MapView.draw", e)

        except Exception as e:
            Logger.error("MapView.draw", e)