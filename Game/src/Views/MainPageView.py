import pygame
from Models.CaracterModel import CaracterModel
from Controllers.PlayerController import PlayerController
from Views.CaracterView import CaracterView
from Views.MapView import MapView
from Models.BottleModel import BottleModel
from Models.PlayerModel import PlayerModel
from Models.BossModel import BossModel
from Models.MapModel import MapModel
from Models.TileModel import TileModel


class MainPageView():

    def __init__(self):

        pygame.init()

        

        screen_width=1920
        screen_height=1072
        

        self.screen = pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)
        pygame.display.set_caption("Guitaroholic - Integration Test")

        johnny = PlayerModel("Johnny Fuzz",60,60)
        gros_bill=BossModel("Gros Bill",80,80)
        beer = BottleModel("Beer", 10, 2, 5)
        vodka = BottleModel("Vodka", 35, 8, 20)
        champagne = BottleModel("Champagne", 20, 4, 8)
        tile_kinds =[
            TileModel("road", "Game/Assets/road3_carre.png", False),
            TileModel("road2", "Game/Assets/road3_carre.png", False)

        ]
        map = MapModel("Game/Assets/maps/map.map", tile_kinds, 106)

        johnny.setSelectedBottle(beer)

        controller = PlayerController(self.screen, johnny)

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
            MapView(self.screen,map)

            player_view.drawCaracter(self.screen, johnny)
            boss_view.drawCaracter(self.screen, gros_bill)



            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


