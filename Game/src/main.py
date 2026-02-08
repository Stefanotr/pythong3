

import pygame
from Views.LoginPageView import LoginPageView
from Views.WelcomePageView import WelcomPageView
from Utils.Logger import Logger
from Controllers.GameState import GameState




def main():
   
    try:
        Logger.debug("main.main", "Game application starting")
        
        
        try:
            if not pygame.get_init():
                pygame.init()
                Logger.debug("main.main", "Pygame initialized")
        except Exception as e:
            Logger.error("main.main", e)
            raise
        
        
        while True:
            
            try:
                login_page = LoginPageView(
                    "Connexion",
                    800,
                    800,
                    pygame.RESIZABLE,
                    "Game/Assets/welcomePage.png"
                )
                Logger.debug("main.main", "Login page created, starting run loop")
                login_result = login_page.run()
                
                if login_result and login_result.get("success"):
                    Logger.debug("main.main", "Login successful, transitioning to welcome page")
                    
                    
                    try:
                        welcome_page = WelcomPageView(
                            "Menu",
                            login_result.get("width", 800),
                            login_result.get("height", 800),
                            pygame.RESIZABLE,
                            "Game/Assets/welcomePage.png"
                        )
                        
                        
                        welcome_page.current_user = login_result.get("user")
                        welcome_page.user_progression = login_result.get("progression")
                        welcome_page.is_admin = login_result.get("is_admin", False)
                        
                        Logger.debug("main.main", "Welcome page created, starting run loop")
                        welcome_result = welcome_page.run()
                        
                       
                        if welcome_result == GameState.LOGOUT.value or welcome_result == "LOGOUT":
                            
                            Logger.debug("main.main", "User logged out, showing login again")
                            continue
                        elif welcome_result == False or welcome_result == GameState.QUIT.value:
                            
                            Logger.debug("main.main", "User quit the game, exiting application")
                            break
                        else:
                            
                            Logger.debug("main.main", "Returned from welcome page, showing login again")
                            continue
                    except Exception as e:
                        Logger.error("main.main", e)
                        raise
                else:
                    
                    Logger.debug("main.main", "Login cancelled or failed, exiting application")
                    break
            except Exception as e:
                Logger.error("main.main", e)
                break
        
        Logger.debug("main.main", "Game application ended normally")
        
    except KeyboardInterrupt:
        Logger.debug("main.main", "Game interrupted by user (KeyboardInterrupt)")
        try:
            pygame.quit()
        except Exception:
            pass
    except Exception as e:
        Logger.error("main.main", e)
        try:
            pygame.quit()
        except Exception:
            pass
        raise




if __name__ == "__main__":
    main()



