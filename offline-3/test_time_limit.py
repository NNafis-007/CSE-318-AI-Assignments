#!/usr/bin/env python3
"""
Test script to demonstrate AI time limit functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.ai_player import AIPlayer
from Board import Board
import colors
import time

def test_ai_time_limit():
    """Test the AI player with time limits"""
    print("Testing AI Player with Time Limits")
    print("=" * 40)
    
    # Create a board and AI player
    board = Board()
    ai_player = AIPlayer(colors.RED, difficulty=4, heuristic_name='weighted_combined')
    
    print(f"AI Player Color: {colors.get_color_name(ai_player.color)}")
    print(f"AI Difficulty: {ai_player.difficulty}")
    print(f"Time Limit: {ai_player.time_limit} seconds")
    print()
      # Make a few moves to populate the board
    print("Setting up board with some initial moves...")
    board.grid[0][0].player = colors.RED
    board.grid[0][0].orb_count = 1
    board.grid[1][1].player = colors.BLUE
    board.grid[1][1].orb_count = 1
    board.grid[2][2].player = colors.RED
    board.grid[2][2].orb_count = 2
    board.grid[3][3].player = colors.BLUE
    board.grid[3][3].orb_count = 1
    
    print("Board state:")
    for i in range(4):
        row_str = ""
        for j in range(4):
            cell = board.grid[i][j]
            if cell.player is None:
                row_str += "[ ] "
            else:
                color_symbol = "R" if cell.player == colors.RED else "B"
                row_str += f"[{color_symbol}{cell.orb_count}] "
        print(row_str)
    print()
    
    # Test AI move with time reporting
    print("Getting AI move with time limit...")
    start_time = time.time()
    
    try:
        best_move = ai_player.get_best_move(board)
        total_time = time.time() - start_time
        
        if best_move:
            print(f"AI selected move: {best_move}")
        else:
            print("No valid moves found")
            
        print(f"Total execution time: {total_time:.3f} seconds")
        
    except Exception as e:
        print(f"Error during AI move: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_time_limit()
