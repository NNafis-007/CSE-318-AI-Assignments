"""
Development run script for the Chain Reaction game
Handles pygame initialization and provides better error reporting
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def run_game():
    """Run the game with proper error handling"""
    try:
        # Test imports first
        print("🔄 Testing imports...")
        from src.core.game_manager import Game
        print("✅ All imports successful!")
        
        # Initialize and run game
        print("🎮 Starting Chain Reaction Game...")
        game = Game()
        game.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure pygame is installed: pip install pygame")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Game Error: {e}")
        print(f"Error type: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    run_game()
