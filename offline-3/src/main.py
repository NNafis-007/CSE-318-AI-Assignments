"""
Main entry point for the Chain Reaction game.
This file follows the Single Responsibility Principle by only handling application startup.
Updated to use the refactored UI/Logic separation.
"""

import sys
import os

# Add parent directory to path for src package imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.core.refactored_game_manager import Game

def main():
    """Entry point of the application"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
