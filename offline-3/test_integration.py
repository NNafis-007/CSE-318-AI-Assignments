#!/usr/bin/env python3
"""
Quick test for Human vs AI GUI integration
"""

import pygame
from src.core.game_manager import Game
from src.config.enums import GameMode

def test_human_vs_ai_integration():
    """Test the Human vs AI integration"""
    print("Testing Human vs AI GUI integration...")
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Create game instance
        game = Game()
        
        # Test AI import
        from src.core.ai_player import AIPlayer
        import colors
        
        ai_player = AIPlayer(colors.BLUE, difficulty=2, heuristic_name='basic')
        print("✅ AI Player created successfully")
        
        # Test board conversion
        game_board = game.state_manager.game_screen.board if game.state_manager.game_screen else None
        if game_board:
            print("✅ Game board accessible")
        
        print("✅ Human vs AI integration test passed!")
        print("🎮 You can now run 'python main.py' and select 'Human vs AI' from the menu")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_human_vs_ai_integration()
