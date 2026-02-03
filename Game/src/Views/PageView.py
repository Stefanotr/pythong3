import pygame

class PageView():

   
    def __init__(self,name, width, height , backgroud_image):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN) 
        pygame.display.set_caption(name)
        
        self.background = pygame.image.load(backgroud_image)
        self.background = pygame.transform.scale(self.background, (width, height))

    def draw(self):
        """Affiche le fond du shop"""
        self.screen.blit(self.background, (0, 0))