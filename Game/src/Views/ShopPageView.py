import pygame
import sys

class ShopPageView():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800)) 
        pygame.display.set_caption("Shop du jeux")
        
        self.background = pygame.image.load('Game/Assets/Shop.png')
        self.background = pygame.transform.scale(self.background, (800, 800))

    def draw(self):
        """Affiche le fond du shop"""
        self.screen.blit(self.background, (0, 0))
    
