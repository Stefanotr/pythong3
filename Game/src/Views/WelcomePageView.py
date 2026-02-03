import pygame
import sys

class WelcomPageView():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800)) 
        pygame.display.set_caption("Menu de mon Jeu")
        
        self.background = pygame.image.load('Game/Assets/welcomePage.png')
        self.background = pygame.transform.scale(self.background, (800, 800))

    def draw(self):
        """Affiche le fond du menu"""
        self.screen.blit(self.background, (0, 0))
    
    def run(self):
        """Boucle principale quand on lance WelcomePageView directement"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()


if __name__ == "__main__":
    menu = WelcomPageView()
    menu.run()