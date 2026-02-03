import pygame
from Utils.Logger import Logger

class PlayerController:
    def __init__(self, screen, player):
        self.player = player
        self.SCREEN_SIZE = 400
        self.PLAYER_SIZE = 50 
        self.SPEED = 10

    def handleInput(self, event):
        if event.type == pygame.KEYDOWN:
            
            current_x = self.player.getX()
            current_y = self.player.getY()
            

            # GAUCHE
            if event.key == pygame.K_LEFT: 
                if current_x > 0: 
                    self.player.setX(current_x - self.SPEED)

            # DROITE
            if event.key == pygame.K_RIGHT: 
                if current_x < (self.SCREEN_SIZE - self.PLAYER_SIZE): 
                    self.player.setX(current_x + self.SPEED)
            
            # HAUT
            if event.key == pygame.K_UP:
                if current_y > 0:
                    self.player.setY(current_y - self.SPEED)

            # BAS
            if event.key == pygame.K_DOWN:
                if current_y < (self.SCREEN_SIZE - self.PLAYER_SIZE):
                    self.player.setY(current_y + self.SPEED)

            # BOIRE 
            if event.key == pygame.K_b:
                
                self.player.drink(self.player.getSelectedBottle)
                
                Logger.debug("PlayerController.handleInput",f"🍺 Glouglou ! Ivre à {self.player.getDrunkenness()}%")