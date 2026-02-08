from enum import Enum


class GameState(Enum):

    QUIT = "QUIT"
    LOGOUT = "LOGOUT"
    MAP = "MAP"
    GAME_OVER = "GAME_OVER"
    COMPLETE = "COMPLETE"
    START_GAME = "START_GAME"
    CONTINUE = "CONTINUE"
