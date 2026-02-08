import pygame
import os
from Views.Act1View import ActView
from Utils.Logger import Logger

class Act2View:

    def __new__(cls, screen, player=None, sequence_controller =None):

        return ActView.createAct2(screen, player, sequence_controller)

if __name__ == "__main__":

    try:
        Logger.debug("Act2View.__main__", "Standalone test starting")
        
        try:
            pygame.init()
            Logger.debug("Act2View.__main__", "Pygame initialized")
        except Exception as e:
            Logger.error("Act2View.__main__", e)
            raise
        
        try:
            screen_info = pygame.display.Info()
            try:
                os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
            except Exception as e:
                Logger.error("Act2View.__main__", e)
            screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
            pygame.display.set_caption("Act 2 - Wood-Stock-Option")
            Logger.debug("Act2View.__main__", "Display created", 
                       width=screen_info.current_w, height=screen_info.current_h)
        except Exception as e:
            Logger.error("Act2View.__main__", e)
            raise
        
        try:
            act2 = Act2View(screen)
            result = act2.run()
            Logger.debug("Act2View.__main__", "Act 2 result", result=result)
        except Exception as e:
            Logger.error("Act2View.__main__", e)
            raise
            
    except Exception as e:
        Logger.error("Act2View.__main__", e)
    finally:
        try:
            pygame.quit()
        except Exception:
            pass
