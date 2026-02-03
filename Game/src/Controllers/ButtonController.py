import pygame
import sys
import os

# Ajouter le chemin racine au PYTHONPATH pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, root_dir)

from Game.src.Views.WelcomePageView import WelcomPageView


class Button:
    """Classe réutilisable pour créer des boutons cliquables"""
    
    def __init__(self, image_path, position, action=None):
        """
        Args:
            image_path: Chemin vers l'image du bouton
            position: Tuple (x, y) pour la position du bouton
            action: Fonction à exécuter quand le bouton est cliqué
        """
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 80))
        self.rect = self.image.get_rect(center=position)
        self.action = action
    
    def draw(self, screen):
        """Affiche le bouton à l'écran"""
        screen.blit(self.image, self.rect)
    
    def is_clicked(self, mouse_pos):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos)
    
    def handle_click(self):
        """Exécute l'action associée au bouton"""
        if self.action:
            self.action()


class MenuController:
    def __init__(self):
        self.view = WelcomPageView()
        self.running = True
        
        # Créer les boutons avec leurs actions
        self.buttons = []
        
        # Bouton Jouer (au centre-haut)
        self.play_button = Button(
            image_path='Game/Assets/buttonPlay.png',  
            position=(400, 500),
            action=self.start_game
        )
        self.buttons.append(self.play_button)
        
        # Bouton Quitter (en bas)
        self.quit_button = Button(
            image_path='Game/Assets/buttonQuit.png',
            position=(400, 700),
            action=self.quit_game
        )
        self.buttons.append(self.quit_button)
    
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
    
    def run(self):
        """Boucle principale du menu"""
        while self.running:
            self.handle_events()
            
            # Afficher le fond
            self.view.draw()
            
            # Afficher tous les boutons
            for button in self.buttons:
                button.draw(self.view.screen)
            
            pygame.display.flip()


if __name__ == "__main__":
    menu = MenuController()
    menu.run()