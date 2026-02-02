import pygame
from Models.PlayerModel import PlayerModel
from Controllers.PlayerController import PlayerController
from Views.PlayerView import PlayerView
from Models.BouteilleModel import BouteilleModel

class MainPageView():

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Johnny Fuzz - Integration Test")

        self.johnny = PlayerModel("Johnny Fuzz")
        self.controller = PlayerController(self.johnny)
        self.player_view = PlayerView()

        clock = pygame.time.Clock()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.controller.handle_input(event)
            
            self.screen.fill((30, 30, 30))
            self.player_view.draw(self.screen, self.johnny)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

biere = BouteilleModel("Bière", 10, 2, 5, 2)
vodka = BouteilleModel("Vodka", 35, 8, 20, 25)
hampagne = BouteilleModel("Champagne", 20, 4, 8, 5)
