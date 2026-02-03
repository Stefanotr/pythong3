import pygame
from Utils.Logger import Logger
from Models.PlayerModel import PlayerModel

class CaracterView:
    def __init__(self,image_path):
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.sprite = pygame.transform.scale(original_image, (50, 50))
            Logger.debug("CaracterView.__init__",f"✅ Image loaded ",image_path=image_path)
        except FileNotFoundError as e:
            Logger.error("CaracterView.__init__",e)
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 255))

        self.font = pygame.font.SysFont(None, 36)

    def drawCaracter(self, screen, caracter):
        x = caracter.getX()
        y = caracter.getY()
        
        screen.blit(self.sprite, (x, y))

    
        if isinstance(caracter, PlayerModel):
            
            alcohol = caracter.getDrunkenness()
            text_content = f"Alcohol: {alcohol}%"
            text_surface = self.font.render(text_content, True, (255, 255, 255))
            screen.blit(text_surface, (10, 10))

        

        
    
