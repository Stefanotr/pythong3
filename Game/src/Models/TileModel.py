import pygame

class TileModel():

    def __init__(self, name, image, is_solid):
        
        self.name=name
        self.image= pygame.image.load(image)
        self.is_solid=is_solid