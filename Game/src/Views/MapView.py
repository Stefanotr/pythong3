import pygame


class MapView():

    def __init__(self, screen, map):
        for y, row in enumerate(map.tiles):
            for x, tile in enumerate(row):
                location = (x * map.tile_size, y * map.tile_size)
                image = map.tile_kinds[tile].image
                screen.blit(image, location)