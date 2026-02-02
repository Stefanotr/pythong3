import pygame

class PlayerController:
    def __init__(self, player):
        self.player = player
        self.SCREEN_SIZE = 400
        self.PLAYER_SIZE = 50 
        self.SPEED = 10

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            
            current_x = self.player.get_x()
            current_y = self.player.get_y()
            current_alcool = self.player.get_alcohol_level()

            # GAUCHE
            if event.key == pygame.K_LEFT: 
                if current_x > 0: 
                    self.player.set_x(current_x - self.SPEED)

            # DROITE
            if event.key == pygame.K_RIGHT: 
                if current_x < (self.SCREEN_SIZE - self.PLAYER_SIZE): 
                    self.player.set_x(current_x + self.SPEED)
            
            # HAUT
            if event.key == pygame.K_UP:
                if current_y > 0:
                    self.player.set_y(current_y - self.SPEED)

            # BAS
            if event.key == pygame.K_DOWN:
                if current_y < (self.SCREEN_SIZE - self.PLAYER_SIZE):
                    self.player.set_y(current_y + self.SPEED)

            # BOIRE 
            if event.key == pygame.K_b:
                self.player.set_alcohol_level(current_alcool + 10)
                
                print(f"🍺 Glouglou ! Ivre à {self.player.get_alcohol_level()}%")