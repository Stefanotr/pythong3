import pygame
from Models.BossModel import BossModel

class BossView:

    def __init__(self, screen):
        self.screen = screen
        self.boss_model = BossModel()

       
        self.image = pygame.image.load("Game/Assets/boss.png").convert_alpha()
        self.rect = self.image.get_rect()

        
        self.rect.topleft = (
            self.boss_model.position_x,
            self.boss_model.position_y
        )

    def afficherBoss(self):
        self.screen.blit(self.image, self.rect)