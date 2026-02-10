

import pygame
from Utils.Logger import Logger
from Controllers import BaseController
from Controllers.GameState import GameState


class PauseMenuController(BaseController):


    def __init__(self, button_controllers):

        try:
            self.button_controllers = button_controllers or []
            self.selected_index = 0
            Logger.debug(
                "PauseMenuController.__init__",
                "Pause menu controller initialized",
                button_count=len(self.button_controllers),
            )
        except Exception as e:
            Logger.error("PauseMenuController.__init__", e)
            raise



    def handle_events(self, events):

        try:
            result = None
            for event in events:
                action = self.handle_input(event)
                if action is not None:
                    result = action
            return result
        except Exception as e:
            Logger.error("PauseMenuController.handle_events", e)
            return None


    def handle_input(self, event):
        
        
        try:
            if event.type == pygame.QUIT:
                Logger.debug("PauseMenuController.handle_input", "QUIT event received")
                return GameState.QUIT.value


            if event.type == pygame.KEYDOWN:
                if self.button_controllers:
                    if event.key == pygame.K_UP:
                        self.selected_index = (self.selected_index - 1) % len(self.button_controllers)
                        Logger.debug(
                            "PauseMenuController.handle_input",
                            "Selection moved up",
                            index=self.selected_index,
                        )
                    elif event.key == pygame.K_DOWN:
                        self.selected_index = (self.selected_index + 1) % len(self.button_controllers)
                        Logger.debug(
                            "PauseMenuController.handle_input",
                            "Selection moved down",
                            index=self.selected_index,
                        )

                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if 0 <= self.selected_index < len(self.button_controllers):
                        button_controller = self.button_controllers[self.selected_index]
                        action = button_controller.action
                        Logger.debug(
                            "PauseMenuController.handle_input",
                            "Keyboard selection made",
                            action=action,
                        )
                        return self._map_button_action(action)


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button_controller in self.button_controllers:
                    try:
                        if button_controller.isClicked(mouse_pos):
                            action = button_controller.action
                            Logger.debug(
                                "PauseMenuController.handle_input",
                                "Mouse click on button",
                                action=action,
                            )
                            return self._map_button_action(action)
                    except Exception as e:
                        Logger.error("PauseMenuController.handle_input", e)
                        continue

            return None
        except Exception as e:
            Logger.error("PauseMenuController.handle_input", e)
            return None



    def _map_button_action(self, action):
        
        
        if action == "continue_game":
            return GameState.CONTINUE.value
        if action == "main_menu":
            return GameState.MAIN_MENU.value
        if action == "quit_game":
            return GameState.QUIT.value
        if action == "logout":
            return GameState.LOGOUT.value
        return None


