import pygame

class CaracterView:
    def __init__(self,image_path):
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.sprite = pygame.transform.scale(original_image, (50, 50))
            print(f"✅ Image loaded : {image_path}")
        except FileNotFoundError:
            print(f"❌ ERROR : Image not found {image_path}")
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 255))

        self.font = pygame.font.SysFont(None, 36)

    def drawCaracter(self, screen, caracter):
        x = caracter.getX()
        y = caracter.getY()
        
        screen.blit(self.sprite, (x, y))

    
        if caracter.getType() == "PLAYER":
            
            alcohol = caracter.getAlcoholLevel()
            text_content = f"Alcohol: {alcohol}%"
            text_surface = self.font.render(text_content, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10))

        

        
    
