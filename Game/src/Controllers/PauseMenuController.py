import pygame
from Utils.Logger import Logger
from Controllers import BaseController
from Controllers.GameState import GameState


class PauseMenuController(BaseController):

    def __init__(self, buttonControllers):
        try:
            self.button_controllers = buttonControllers or []
            self.selected_index = 0
            Logger.debug(
                "PauseMenuController.__init__",
                "Pause menu controller initialized",
                buttonCount=len(self.button_controllers),
            )
        except Exception as e:
            Logger.error("PauseMenuController.__init__", e)
            raise

    def handleEvents(self, events):
        try:
            result = None
            for event in events:
                action = self.handleInput(event)
                if action is not None:
                    result = action
            return result
        except Exception as e:
            Logger.error("PauseMenuController.handleEvents", e)
            return None

    def handleInput(self, event):
        try:
            if event.type == pygame.QUIT:
                Logger.debug("PauseMenuController.handleInput", "QUIT event received")
                return GameState.QUIT.value

            if event.type == pygame.KEYDOWN:
                if self.button_controllers:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.button_controllers)
                        Logger.debug(
                            "PauseMenuController.handleInput",
                            "Selection moved up",
                            index=self.selected_index,
                        )
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.button_controllers)
                        Logger.debug(
                            "PauseMenuController.handleInput",
                            "Selection moved down",
                            index=self.selected_index,
                        )

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if 0 <= self.selected_index < len(self.button_controllers):
                        buttonController = self.button_controllers[self.selected_index]
                        action = buttonController.action
                        Logger.debug(
                            "PauseMenuController.handleInput",
                            "Keyboard selection made",
                            action=action,
                        )
                        return self.mapButtonAction(action)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for buttonController in self.button_controllers:
                    try:
                        if buttonController.isClicked(mouse_pos):
                            action = buttonController.action
                            Logger.debug(
                                "PauseMenuController.handleInput",
                                "Mouse click on button",
                                action=action,
                            )
                            return self.mapButtonAction(action)
                    except Exception as e:
                        Logger.error("PauseMenuController.handleInput", e)
                        continue

            return None
        except Exception as e:
            Logger.error("PauseMenuController.handleInput", e)
            return None

    def mapButtonAction(self, action):
        if action == "continue_game":
            return GameState.CONTINUE.value
        if action == "main_menu":
            return GameState.MAIN_MENU.value
        if action == "quit_game":
            return GameState.QUIT.value
        if action == "logout":
            return GameState.LOGOUT.value
        return None


