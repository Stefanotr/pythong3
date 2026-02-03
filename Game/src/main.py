from Views.WelcomePageView import WelcomPageView
import pygame

def main():
    
    welcome_page=WelcomPageView("Menu",800,800,pygame.RESIZABLE,"Game/Assets/welcomePage.png")
    welcome_page.run()


if __name__ == "__main__":
    
    main()



