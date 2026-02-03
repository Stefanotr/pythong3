import pygame
import sys


class ButtonController:
    """Classe réutilisable pour créer des boutons cliquables"""
    
    def __init__(self, action=None):
     self.action=action
    
    def is_clicked(self, mouse_pos):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos)
    
    def handle_click(self):
        """Exécute l'action associée au bouton"""
        if self.action:
            self.action()
    
    
    def handle_events(self):
        """Gère tous les événements du menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Vérifier chaque bouton
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            button.handle_click()
    
    def quit_game(self):
        """Quitte le jeu proprement"""
        pygame.quit()
        sys.exit()
    
    def start_game(self):
        """Démarre le jeu (fonction exemple)"""
        print("Lancement du jeu...")
        # Ici tu pourras changer d'état de jeu
    




    