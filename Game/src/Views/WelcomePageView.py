import pygame
from Utils.Logger import Logger
from Controllers.ButtonController import ButtonController
from Views.PageView import PageView
from Views.ButtonView import ButtonView
from Views.MainPageView import MainPageView

class WelcomPageView(PageView):
    def __init__(self,name,width=800, height=800,RESIZABLE=0, background_image="Game/Assets/welcomePage.png"):
        super().__init__(name,width,height,RESIZABLE,background_image)
        

        screen_width=1920
        screen_height=1080
        
        
        # Créer les boutons avec leurs actions
        self.buttons = []
        self.buttons_controllers=[]
        
        # Bouton Jouer (au centre-haut)
        self.play_button = ButtonView(
            image_path='Game/Assets/buttonPlay.png',  
            position=(400, 500),
            
        )
        self.buttons.append(self.play_button)
        
        
        play_button_controller=ButtonController(self.play_button,"start_game" )
        
        self.buttons_controllers.append(play_button_controller)
        
        # Bouton Quitter (en bas)
        self.quit_button = ButtonView(
            image_path='Game/Assets/buttonQuit.png',
            position=(400, 700),
        )
        self.buttons.append(self.quit_button)

        quit_button_controller=ButtonController(self.quit_button, "quit_game")
        self.buttons_controllers.append(quit_button_controller)


        


    def run(self):
        clock=pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button_controller in self.buttons_controllers:
                    button_controller.handleEvents(event)  

            self.draw()
            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
