from enum import Enum

class GameState(Enum):
    MENU = "menu"
    GAME = "game"

class GameMode(Enum):
    TWO_PLAYER = "2 Player"
    HUMAN_VS_AI = "Human vs AI"
    AI_VS_AI = "AI vs AI"
