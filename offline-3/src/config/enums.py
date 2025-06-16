from enum import Enum

class GameState(Enum):
    MENU = "menu"
    GAME = "game"
    AI_CONFIG = "ai_config"  # New state for AI configuration

class GameMode(Enum):
    TWO_PLAYER = "2 Player"
    HUMAN_VS_AI = "Human vs AI"
    AI_VS_AI = "AI vs AI"

class AIDifficulty(Enum):
    EASY = ("Easy", 3)
    MEDIUM = ("Medium", 4)
    HARD = ("Hard", 6)
    
    def __init__(self, display_name, depth):
        self.display_name = display_name
        self.depth = depth

class AIHeuristic(Enum):
    WEIGHTED_COMBINED = ("Weighted Combined", "weighted_combined")
    ORB_COUNT = ("Orb Count", "orb_count")
    EDGE_CORNER = ("Edge Corner", "edge_corner")
    STRATEGIC = ("Strategic", "strategic")
    CHAIN_REACTION = ("Chain Reaction", "chain_reaction")
    
    def __init__(self, display_name, key):
        self.display_name = display_name
        self.key = key
