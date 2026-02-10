

import pygame
from Utils.Logger import Logger



class ButtonView:
   
    
    
    
    def __init__(self, image_path, position, size=(200, 80)):
   

        try:
           
            try:
                self.image = pygame.image.load(image_path)
               
                self.image = pygame.transform.scale(self.image, size)
                Logger.debug("ButtonView.__init__", "Button image loaded", path=image_path, size=size)
            except FileNotFoundError as e:
                Logger.error("ButtonView.__init__", e)
               
                self.image = pygame.Surface(size)
                self.image.fill((128, 128, 128))
                Logger.debug("ButtonView.__init__", "Using default button surface")
            except Exception as e:
                Logger.error("ButtonView.__init__", e)
                raise
            
            
            

            try:
                self.rect = self.image.get_rect(center=position)
                Logger.debug("ButtonView.__init__", "Button rectangle created", position=position)
            except Exception as e:
                Logger.error("ButtonView.__init__", e)
                raise
                
        except Exception as e:
            Logger.error("ButtonView.__init__", e)
            raise
    
  
  

    
    def draw(self, screen):
       
        try:
          
            if not pygame.get_init() or pygame.display.get_surface() is None:
                return

            screen.blit(self.image, self.rect)
        except Exception as e:
            Logger.error("ButtonView.draw", e)
    

    
    def set_position(self, position):
       
        try:
            self.rect.center = position
            Logger.debug("ButtonView.set_position", "Button position updated", position=position)
        except Exception as e:
            Logger.error("ButtonView.set_position", e)