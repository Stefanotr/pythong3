"""
MapModel Module

Represents the game map loaded from a file.
Manages tile data, tile types, and map dimensions.
"""

import pygame
from Utils.Logger import Logger


# === MAP MODEL CLASS ===

class MapModel:
    """
    Model for the game map.
    Loads map data from file and manages tile layout.
    """
    
    # === INITIALIZATION ===
    
    def __init__(self, map_file, tile_kinds, tile_size):
        """
        Initialize the map model by loading map data from file.
        
        Args:
            map_file: Path to the map file
            tile_kinds: List of TileModel instances representing tile types
            tile_size: Size of each tile in pixels
        """
        try:
            self.tile_kinds = tile_kinds
            self.tile_size = tile_size
            Logger.debug("MapModel.__init__", "Loading map", map_file=map_file, tile_size=tile_size)
            
            # Load map data from file
            try:
                with open(map_file, "r") as file:
                    data = file.read()
                Logger.debug("MapModel.__init__", "Map file read successfully", map_file=map_file)
            except FileNotFoundError as e:
                Logger.error("MapModel.__init__", e)
                self.tiles = []
                raise
            except Exception as e:
                Logger.error("MapModel.__init__", e)
                self.tiles = []
                raise
            
            # Parse map data
            try:
                self.tiles = []
                for line in data.split("\n"):
                    if line.strip():  # Skip empty lines
                        row = []
                        for tile_number in line:
                            try:
                                row.append(int(tile_number))
                            except ValueError:
                                Logger.debug("MapModel.__init__", "Invalid tile number, skipping", tile=tile_number)
                                continue
                        if row:  # Only add non-empty rows
                            self.tiles.append(row)
                Logger.debug("MapModel.__init__", "Map parsed successfully", 
                           rows=len(self.tiles), 
                           cols=len(self.tiles[0]) if self.tiles else 0)
            except Exception as e:
                Logger.error("MapModel.__init__", e)
                self.tiles = []
                raise
                
        except Exception as e:
            Logger.error("MapModel.__init__", e)
            raise