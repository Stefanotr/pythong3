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
    
    # === GETTERS / SETTERS ===
    
    def getTileKinds(self):
        """
        Get the list of tile types.
        
        Returns:
            list: List of TileModel instances
        """
        try:
            return self.tile_kinds.copy() if hasattr(self, 'tile_kinds') else []
        except Exception as e:
            Logger.error("MapModel.getTileKinds", e)
            return []
    
    def setTileKinds(self, tile_kinds):
        """
        Set the list of tile types.
        
        Args:
            tile_kinds: List of TileModel instances
        """
        try:
            if isinstance(tile_kinds, list):
                self.tile_kinds = tile_kinds.copy()  # Store a copy
                Logger.debug("MapModel.setTileKinds", "Tile kinds set", count=len(self.tile_kinds))
            else:
                Logger.error("MapModel.setTileKinds", ValueError("Tile kinds must be a list"))
        except Exception as e:
            Logger.error("MapModel.setTileKinds", e)
    
    def getTileSize(self):
        """
        Get the tile size in pixels.
        
        Returns:
            int: Tile size in pixels
        """
        try:
            return self.tile_size
        except Exception as e:
            Logger.error("MapModel.getTileSize", e)
            return 32
    
    def setTileSize(self, tile_size):
        """
        Set the tile size in pixels.
        
        Args:
            tile_size: Tile size in pixels
        """
        try:
            self.tile_size = max(1, int(tile_size))
            Logger.debug("MapModel.setTileSize", "Tile size set", tile_size=self.tile_size)
        except Exception as e:
            Logger.error("MapModel.setTileSize", e)
    
    def getTiles(self):
        """
        Get the tile map data.
        
        Returns:
            list: 2D list of tile IDs
        """
        try:
            # Return a deep copy to prevent external modification
            return [row.copy() for row in self.tiles] if hasattr(self, 'tiles') and self.tiles else []
        except Exception as e:
            Logger.error("MapModel.getTiles", e)
            return []
    
    def setTiles(self, tiles):
        """
        Set the tile map data.
        
        Args:
            tiles: 2D list of tile IDs
        """
        try:
            if isinstance(tiles, list):
                # Store a deep copy
                self.tiles = [row.copy() if isinstance(row, list) else row for row in tiles]
                Logger.debug("MapModel.setTiles", "Tiles set", rows=len(self.tiles))
            else:
                Logger.error("MapModel.setTiles", ValueError("Tiles must be a list"))
        except Exception as e:
            Logger.error("MapModel.setTiles", e)