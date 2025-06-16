#!/usr/bin/env python3
"""
Simple test script to demonstrate AI time limit functionality with lower difficulty
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.ai_player import AIPlayer
from Board import Board
import colors
import time

def test_ai_simple():
    """Test the AI player with time limits - simple version"""
    print("Testing AI Player with Time Limits (Simple)")
    print("=" * 50)
    
    # Create a board and AI player with lower difficulty
    board = Board()
    ai_player = AIPlayer(colors.RED, difficulty=2, heuristic_name='weighted_combined')
    
    print(f"AI Player Color: {colors.get_color_name(ai_player.color)}")
    print(f"AI Difficulty: {ai_player.difficulty}")
    print(f"Time Limit: {ai_player.time_limit} seconds")
    print()
    
    # Set up a simple board state
    print("Setting up board with one move...")
    board.grid[4][2].player = colors.BLUE
    board.grid[4][2].orb_count = 1
    
    print("Board state (showing only relevant area):")
    for i in range(3, 6):
        row_str = ""
        for j in range(6):
            cell = board.grid[i][j]
            if cell.player is None:
                row_str += "[ ] "
            else:
                color_symbol = "R" if cell.player == colors.RED else "B"
                row_str += f"[{color_symbol}{cell.orb_count}] "
        print(f"Row {i}: {row_str}")
    print()
    
    # Test AI move with time reporting
    print("Getting AI move with time limit...")
    
    try:
        best_move = ai_player.get_best_move(board)
        
        if best_move:
            print(f"AI selected move: Row {best_move[0]}, Col {best_move[1]}")
        else:
            print("No valid moves found")
            
    except Exception as e:
        print(f"Error during AI move: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_simple()
