#!/usr/bin/env python3
"""
Test script to demonstrate AI time limit being exceeded
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.ai_player import AIPlayer
from Board import Board
import colors
import time

def test_ai_timeout():
    """Test the AI player with a very short time limit to trigger timeout"""
    print("Testing AI Player Time Limit (Timeout Scenario)")
    print("=" * 55)
    
    # Create a board and AI player with high difficulty and very short time limit
    board = Board()
    ai_player = AIPlayer(colors.RED, difficulty=6, heuristic_name='weighted_combined')
    
    # Override time limit to a very short duration for testing
    ai_player.time_limit = 0.1  # 100 milliseconds
    
    print(f"AI Player Color: {colors.get_color_name(ai_player.color)}")
    print(f"AI Difficulty: {ai_player.difficulty}")
    print(f"Time Limit: {ai_player.time_limit} seconds")
    print()
    
    # Set up a complex board state to force more computation
    print("Setting up board with multiple moves...")
    positions = [(4, 2), (4, 3), (5, 2), (5, 3), (3, 1), (6, 4)]
    players = [colors.BLUE, colors.RED, colors.BLUE, colors.RED, colors.BLUE, colors.RED]
    orbs = [1, 1, 2, 1, 1, 1]
    
    for i, ((row, col), player, orb_count) in enumerate(zip(positions, players, orbs)):
        board.grid[row][col].player = player
        board.grid[row][col].orb_count = orb_count
    
    print("Complex board state set up.")
    print()
    
    # Test AI move with very short time limit
    print("Getting AI move with very short time limit...")
    
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
    test_ai_timeout()
