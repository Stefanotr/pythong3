import pygame

class MapModel():

    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds


        file=open(map_file, "r")
        data =file.read()
        file.close()

        self.tiles=[]
        for line in data.split("\n"):
            row=[]
            for tile_number in line:
                row.append(int(tile_number))
            self.tiles.append(row)
        
        self.tile_size = tile_size