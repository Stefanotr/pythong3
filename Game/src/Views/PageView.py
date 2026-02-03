import pygame
import os
from Utils.Logger import Logger

class PageView():

   
    def __init__(self,name="none", width=800, height=800 ,RESIZABLE=0, backgroud_image="Game/Assets/welcomePage.png"):
        
        Logger.debug("PageView.__init__", "argument initialisation", self=self, name=name, width=width, height=height, RESIZABLE=RESIZABLE, backgroud_image=backgroud_image)
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
        pygame.init()
        
        self.name=name
        self.width=width
        self.height=height
        self.resizable=RESIZABLE
        self.backgroud_image=backgroud_image


        self.screen = pygame.display.set_mode((self.width, self.height),self.resizable) 
        pygame.display.set_caption(self.name)
        
        self.background = pygame.image.load(self.backgroud_image)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw(self):
        
        self.screen.blit(self.background, (0, 0))