import pygame

class PlayerView:
    def __init__(self):
        image_path = "Game/Assets/image.png"
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.sprite = pygame.transform.scale(original_image, (50, 50))
            print(f"✅ Image chargée : {image_path}")
        except FileNotFoundError:
            print(f"❌ ERREUR : Image introuvable {image_path}")
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 255))

        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen, player):
        x = player.get_x()
        y = player.get_y()
        alcool = player.get_alcohol_level()

        screen.blit(self.sprite, (x, y))

        text_content = f"Alcool: {alcool}%"
        text_surface = self.font.render(text_content, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))