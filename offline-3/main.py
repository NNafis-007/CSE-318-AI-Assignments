"""
Main entry point for the Chain Reaction game.
This file follows the Single Responsibility Principle by only handling application startup.
"""

from src.core.game_manager import Game

def main():
    """Entry point of the application"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
