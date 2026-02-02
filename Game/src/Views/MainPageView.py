import pygame

class MainPageView():

    def __init__(self):

        pygame.init()

        pygame.display.set_mode((800, 600))

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

biere = Bouteille("Bière", 10, 2, 5, 2)
vodka = Bouteille("Vodka", 35, 8, 20, 25)
hampagne = Bouteille("Champagne", 20, 4, 8, 5)
