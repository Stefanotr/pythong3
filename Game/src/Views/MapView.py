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
            # Cache for scaled tile images to avoid repeated scaling each frame
            self._scaled_tile_cache = {}
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
                # If the map model provides an ordered list of layers, render them in sequence
                # This preserves per-tile transparency and lets upper tiles composite over lower ones
                layers_to_draw = None
                if hasattr(self.map, 'layer_ordered') and isinstance(self.map.layer_ordered, list):
                    layers_to_draw = [layer_matrix for _name, layer_matrix in self.map.layer_ordered]
                elif hasattr(self.map, 'layers') and isinstance(self.map.layers, dict):
                    # fallback: draw merged tiles only
                    layers_to_draw = [self.map.tiles]
                else:
                    layers_to_draw = [self.map.tiles]

                # Draw each layer from bottom to top
                for layer in layers_to_draw:
                    for y, row in enumerate(layer):
                        for x, tile in enumerate(row):
                            try:
                                if not tile:
                                    continue
                                location = (x * self.map.tile_size + offset_x, y * self.map.tile_size + offset_y)
                                tile_size = self.map.tile_size  # Define tile_size early
                                if tile in self.map.tile_kinds:
                                    image = self.map.tile_kinds[tile].image
                                    try:
                                        if not isinstance(image, pygame.Surface):
                                            raise TypeError('tile image not a Surface')
                                        cache_key = (id(image), tile_size)
                                        scaled = self._scaled_tile_cache.get(cache_key)
                                        if scaled is None:
                                            try:
                                                w, h = image.get_size()
                                                if (w, h) != (tile_size, tile_size):
                                                    scaled = pygame.transform.scale(image, (tile_size, tile_size))
                                                else:
                                                    scaled = image
                                            except Exception:
                                                scaled = image
                                            self._scaled_tile_cache[cache_key] = scaled
                                        screen.blit(scaled, location)
                                    except Exception as e:
                                        Logger.error('MapView.draw.blit', e)
                                        rect = (location[0], location[1], tile_size, tile_size)
                                        pygame.draw.rect(screen, (120, 0, 120), rect)
                                else:
                                    try:
                                        if not hasattr(self, '_unknown_gids'):
                                            self._unknown_gids = set()
                                        if tile not in self._unknown_gids:
                                            self._unknown_gids.add(tile)
                                            Logger.debug("MapView.draw", "Unknown tile type, drawing placeholder", tile=tile, position=(x, y))
                                        color = ((tile * 37) % 256, (tile * 61) % 256, (tile * 97) % 256) if isinstance(tile, int) else (150, 0, 150)
                                        rect = (location[0], location[1], tile_size, tile_size)
                                        pygame.draw.rect(screen, color, rect)
                                    except Exception as e:
                                        Logger.error("MapView.draw.placeholder", e)
                            except Exception as e:
                                Logger.error("MapView.draw.tile", e)
                                continue
            except Exception as e:
                Logger.error("MapView.draw", e)

        except Exception as e:
            Logger.error("MapView.draw", e)