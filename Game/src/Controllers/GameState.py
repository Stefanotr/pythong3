from enum import Enum


class GameState(Enum):
    """Centralized game state identifiers.

    Values are strings for backward compatibility with existing return values.
    """

    QUIT = "QUIT"
    MAIN_MENU = "MAIN_MENU"
    ACT1 = "ACT1"
    ACT2 = "ACT2"
    RHYTHM = "RHYTHM"
    MAP = "MAP"
    GAME_OVER = "GAME_OVER"
    COMPLETE = "COMPLETE"
    START_GAME = "START_GAME"
    CONTINUE = "CONTINUE"
