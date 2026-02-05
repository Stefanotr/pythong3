"""
PauseMenuController Module

Handles input for the pause menu: navigation, selection, and quit/continue actions.
"""

import pygame
from Utils.Logger import Logger
from Controllers import BaseController
from Controllers.GameState import GameState


class PauseMenuController(BaseController):
    """
    Controller for managing pause menu interactions.

    It works with a list of ButtonController instances and exposes a simple
    action API:
      - \"continue\"
      - \"main_menu\"
      - \"quit\"
    """

    def __init__(self, button_controllers):
        """
        Initialize the pause menu controller.

        Args:
            button_controllers: list of ButtonController instances
        """
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

    def handleEvents(self, events):
        """
        Handle a batch of events and return a high-level action if any.

        Args:
            events: iterable of pygame events

        Returns:
            str | None: "continue", "main_menu", "quit" or None
        """
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
        """
        Handle a single input event.

        Returns:
            str | None: "continue", "main_menu", "quit" or None
        """
        try:
            # Window close
            if event.type == pygame.QUIT:
                Logger.debug("PauseMenuController.handleInput", "QUIT event received")
                return GameState.QUIT.value
                # ESC to continue
                if event.key == pygame.K_ESCAPE:
                    Logger.debug("PauseMenuController.handle_input", "ESC pressed -> continue")
                    return "continue"

                # Arrow keys for navigation
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

                # Enter/Space to select current button
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    if 0 <= self.selected_index < len(self.button_controllers):
                        button_controller = self.button_controllers[self.selected_index]
                        action = button_controller.action
                        Logger.debug(
                            "PauseMenuController.handleInput",
                            "Keyboard selection made",
                            action=action,
                        )
                        return self._map_button_action(action)

            # Mouse click on buttons
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for button_controller in self.button_controllers:
                    try:
                        if button_controller.isClicked(mouse_pos):
                            action = button_controller.action
                            Logger.debug(
                                "PauseMenuController.handleInput",
                                "Mouse click on button",
                                action=action,
                            )
                            return self._map_button_action(action)
                    except Exception as e:
                        Logger.error("PauseMenuController.handleInput", e)
                        continue

            return None
        except Exception as e:
            Logger.error("PauseMenuController.handleInput", e)
            return None

    def _map_button_action(self, action):
        """
        Map a ButtonController.action to a pause menu result (GameState values).
        """
        if action == "continue_game":
            return GameState.CONTINUE.value
        if action == "main_menu":
            return GameState.MAIN_MENU.value
        if action == "quit_game":
            return GameState.QUIT.value
        return None

    # Backward compatible aliases
    def handle_events(self, events):
        """Legacy alias."""
        return self.handleEvents(events)
    
    def handle_input(self, event):
        """Legacy alias."""
        return self.handleInput(event)


