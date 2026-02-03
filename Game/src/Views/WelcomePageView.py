import pygame
import sys
from Controllers.ButtonController import ButtonController
from Models.ButtonModel import ButtonModel

class WelcomPageView():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800)) 
        pygame.display.set_caption("Menu de mon Jeu")
        
        self.background = pygame.image.load('Game/Assets/welcomePage.png')
        self.background = pygame.transform.scale(self.background, (800, 800))
        
        
        # Créer les boutons avec leurs actions
        self.buttons = []
        
        # Bouton Jouer (au centre-haut)
        self.play_button = ButtonModel(
            image_path='Game/Assets/buttonPlay.png',  
            position=(400, 500),
            action=ButtonController.start_game
        )
        self.buttons.append(self.play_button)
        
        # Bouton Quitter (en bas)
        self.quit_button = ButtonModel(
            image_path='Game/Assets/buttonQuit.png',
            position=(400, 700),
            action=ButtonController.quit_game
        )
        self.buttons.append(self.quit_button)

        self.screen.blit(self.background, (0, 0))
    
    def run(self):
        """Boucle principale quand on lance WelcomePageView directement"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.blit(self.background, (0, 0))
            for button in self.buttons:
                ButtonModel.draw(self.screen)

            pygame.display.flip()

