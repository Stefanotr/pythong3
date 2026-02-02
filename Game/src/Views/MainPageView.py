import pygame
from Models.CaracterModel import CaracterModel
from Controllers.PlayerController import PlayerController
from Views.CaracterView import CaracterView
from Models.BottleModel import BottleModel


class MainPageView():

    def __init__(self):

        pygame.init()

        pygame.display.get_desktop_sizes
        

        self.screen = pygame.display.set_mode((1600, 1400))
        pygame.display.set_caption("Johnny Fuzz - Integration Test")

        johnny = CaracterModel("Johnny Fuzz",60,60,"PLAYER")
        gros_bill=CaracterModel("Gros Bill",80,80,"BOSS")
        beer = BottleModel("Beer", 10, 2, 5, 2)
        vodka = BottleModel("Vodka", 35, 8, 20, 25)
        champagne = BottleModel("Champagne", 20, 4, 8, 5)

        controller = PlayerController(johnny)

        player_view = CaracterView("Game/Assets/guitare.png")
        boss_view=CaracterView("Game/Assets/boss.png")

        clock = pygame.time.Clock()
        
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                controller.handleInput(event)
            
            self.screen.fill((30, 30, 30))
            player_view.drawCaracter(self.screen, johnny)
            boss_view.drawCaracter(self.screen, gros_bill)


            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


