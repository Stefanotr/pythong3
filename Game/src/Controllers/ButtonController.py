import pygame
import sys
from Views.MainPageView import MainPageView
from Utils.Logger import Logger


class ButtonController:
    """Classe réutilisable pour créer des boutons cliquables"""
    
    def __init__(self, button, action=None):
        self.action=action
        self.button=button
    
    def isClicked(self, mouse_pos ):
        """Vérifie si le bouton est cliqué"""
        Logger.debug("ButtonController.isClicked","Bouton gauche cliqué",clique=self.button.rect.collidepoint(mouse_pos))
        return self.button.rect.collidepoint(mouse_pos)
    
    def handleClick(self):
        """Exécute l'action associée au bouton"""

        Logger.debug("ButtonController.handleClick","entré dans la fonction")
        if self.action=="start_game":
            Logger.debug("ButtonController.handleClick","lancement de la page de jeux")
            self.startPage()
        if self.action=="quit_game":
            self.quitGame()
            
    
    
    def handleEvents(self, event):

        """Gère tous les événements du menu"""
        if event.type == pygame.QUIT:
            self.quitGame()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                
                if self.isClicked(mouse_pos):
                    Logger.debug("ButtonController.handleEvents","entré dans le if self.isClicked(mouse_pos):")
                    self.handleClick()

    def quitGame(self):
        """Quitte le jeu proprement"""
        pygame.quit()
        sys.exit()
    
    def startPage(self):
        """Démarre le jeu (fonction exemple)"""
        print("Lancement du jeu...")
        pygame.quit()
        pygame.init()
        game_page=MainPageView("Guitaroholic",1920,1080,pygame.RESIZABLE)
        game_page.draw()
        # Ici tu pourras changer d'état de jeu
    




    