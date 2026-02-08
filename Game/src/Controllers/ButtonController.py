import pygame
import sys
from Utils.Logger import Logger
from Controllers import BaseController
from Controllers.GameState import GameState


class ButtonController(BaseController):

    def __init__(self, button, action=None):
        try:
            self.action = action
            self.button = button
            Logger.debug("ButtonController.__init__", "Button controller initialized", action=action)
        except Exception as e:
            Logger.error("ButtonController.__init__", e)
            raise


    def isClicked(self, mouse_pos):
        try:
            is_clicked = self.button.rect.collidepoint(mouse_pos)
            Logger.debug("ButtonController.isClicked", "Button click checked", clicked=is_clicked)
            return is_clicked
        except Exception as e:
            Logger.error("ButtonController.isClicked", e)
            return False


    def handleClick(self):
        try:
            Logger.debug("ButtonController.handleClick", "Button click handled", action=self.action)
            
            if self.action == "start_game":
                Logger.debug("ButtonController.handleClick", "Start game action triggered")
                return GameState.START_GAME.value
            elif self.action == "quit_game":
                Logger.debug("ButtonController.handleClick", "Quit game action triggered")
                self.quitGame()
                return GameState.QUIT.value
            elif self.action == "logout":
                Logger.debug("ButtonController.handleClick", "Logout action triggered")
                return GameState.LOGOUT.value
            
            return None
        except Exception as e:
            Logger.error("ButtonController.handleClick", e)
            return None


    def handleInput(self, event):
        try:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                if self.isClicked(mouse_pos):
                    Logger.debug("ButtonController.handleInput", "Button clicked, handling action")
                    return self.handleClick()

            return None
        except Exception as e:
            Logger.error("ButtonController.handleInput", e)
            return None

    def handleEvents(self, event):
        return self.handleInput(event)


    def quitGame(self):
        try:
            Logger.debug("ButtonController.quitGame", "Quitting game")
            pygame.quit()
            sys.exit()
        except Exception as e:
            Logger.error("ButtonController.quitGame", e)
            sys.exit(1)