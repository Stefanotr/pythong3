import pygame

class ButtonView:
    """Classe réutilisable pour créer des boutons cliquables"""
    
    def __init__(self, image_path, position):
        """
        Args:
            image_path: Chemin vers l'image du bouton
            position: Tuple (x, y) pour la position du bouton
            action: Fonction à exécuter quand le bouton est cliqué
        """
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (200, 80))
        self.rect = self.image.get_rect(center=position)
        
    
    def draw(self, screen):
        """Affiche le bouton à l'écran"""
        screen.blit(self.image, self.rect)