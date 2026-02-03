import pygame
import sys
from Views.PageView import PageView


class ButtonController:
    """Classe réutilisable pour créer des boutons cliquables"""
    
    def __init__(self, button, action=None):
        self.action=action
        self.button=button
    
    def is_clicked(self, mouse_pos ):
        """Vérifie si le bouton est cliqué"""
        return self.button.rect.collidepoint(mouse_pos)
    
    def handle_click(self):
        """Exécute l'action associée au bouton"""
        if isinstance(self.action, PageView()):
            self.start_page(self.action)
        if self.action=="quit_game":
            self.quit_game()
            
    
    
    def handle_events(self, event):

        """Gère tous les événements du menu"""
        if event.type == pygame.QUIT:
            self.quit_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                
                if self.is_clicked(mouse_pos):
                    self.handle_click()

    def quit_game(self):
        """Quitte le jeu proprement"""
        pygame.quit()
        sys.exit()
    
    def start_page(self,action):
        """Démarre le jeu (fonction exemple)"""
        print("Lancement du jeu...")
        action=action
        # Ici tu pourras changer d'état de jeu
    




    