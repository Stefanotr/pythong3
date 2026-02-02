import pygame
class PlayerController:
    def __init__(self, player):
        self.player = player

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.player.alcohol_level += 5
                print(f"Ivre à {self.player.alcohol_level}%")
            if event.key == pygame.K_LEFT: self.player.x -= 10
            if event.key == pygame.K_RIGHT: self.player.x += 10