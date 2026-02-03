import pygame

from Models.CaracterModel import CaracterModel
from Controllers.PlayerController import PlayerController
from Views.CaracterView import CaracterView
from Views.MapView import MapView
from Views.PageView import PageView
from Models.BottleModel import BottleModel
from Models.PlayerModel import PlayerModel
from Models.BossModel import BossModel
from Models.MapModel import MapModel
from Models.TileModel import TileModel


class MainPageView(PageView):

    def __init__(self,name,width=800, height=800,RESIZABLE=0, background_image="Game/Assets/welcomePage.png"):
        super().__init__(name,width,height,RESIZABLE,background_image)


        self.johnny = PlayerModel("Johnny Fuzz",60,60)
        self.gros_bill=BossModel("Gros Bill",80,80)
        self.beer = BottleModel("Beer", 10, 2, 5)
        self.vodka = BottleModel("Vodka", 35, 8, 20)
        self.champagne = BottleModel("Champagne", 20, 4, 8)
        tile_kinds =[
            TileModel("road", "Game/Assets/road3_carre.png", False),
            TileModel("road2", "Game/Assets/road3_carre.png", False)

        ]
        self.map = MapModel("Game/Assets/maps/map.map", tile_kinds, 106)

        self.johnny.setSelectedBottle(self.beer)

        self.controller = PlayerController(self.screen, self.johnny)

        self.player_view = CaracterView("Game/Assets/guitare.png")
        self.boss_view=CaracterView("Game/Assets/boss.png")


    def run(self):
        clock = pygame.time.Clock()
        
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.controller.handleInput(event)
            
            self.draw()
            MapView(self.screen,self.map)

            self.player_view.drawCaracter(self.screen, self.johnny)
            self.boss_view.drawCaracter(self.screen, self.gros_bill)



            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


