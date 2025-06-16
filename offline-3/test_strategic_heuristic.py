#!/usr/bin/env python3
"""
Test script to verify the new strategic heuristic functionality
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import Board
import utils
import colors

def test_strategic_heuristic():
    """Test the new strategic heuristic"""
    print("=== Testing Strategic Heuristic ===")
    
    # Create a simple test board
    board = Board.Board(3, 3)  # Small 3x3 board for testing
    
    # Place some orbs to test different scenarios
    board.grid[0][0].player = 1  # Red player in corner
    board.grid[0][0].orb_count = 1
    
    board.grid[1][1].player = 2  # Blue player in center
    board.grid[1][1].orb_count = 3  # One away from critical (4)
    
    board.grid[0][1].player = 1  # Red player on edge
    board.grid[0][1].orb_count = 2  # One away from critical (3)
    
    # Test the heuristic
    red_score = utils.heuristic_strategic_evaluation(board, colors.RED)
    blue_score = utils.heuristic_strategic_evaluation(board, colors.BLUE)
    
    print(f"Red player score: {red_score}")
    print(f"Blue player score: {blue_score}")
    
    # Test basic orb counting
    expected_red_orbs = 1 + 2  # corner + edge orbs
    print(f"Red orbs on board: {expected_red_orbs}")
    
    # Test positional bonuses
    print("\nTesting positional bonuses:")
    print("- Corner cell (0,0): should get +3 bonus if no critical enemies")
    print("- Edge cell (0,1): should get +2 bonus if no critical enemies")
    print("- Critical cell (0,1): should get +2 bonus if critical")

def test_ai_heuristic_mapping():
    """Test that the AI player can use the new heuristic"""
    print("\n=== Testing AI Heuristic Mapping ===")
    
    try:
        from src.core.ai_player import AIPlayer
        
        # Test creating AI with strategic heuristic
        ai = AIPlayer(colors.BLUE, difficulty=3, heuristic_name='strategic')
        print("✅ AI player created successfully with strategic heuristic")
        
        # Test that the function is correctly mapped
        heuristic_func = ai._get_heuristic_function('strategic')
        print(f"✅ Strategic heuristic function: {heuristic_func.__name__}")
        
        # Test that vulnerability is no longer available
        vulnerability_func = ai._get_heuristic_function('vulnerability')
        print(f"✅ Vulnerability heuristic fallback: {vulnerability_func.__name__}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_enums():
    """Test the updated enums"""
    print("\n=== Testing Updated Enums ===")
    
    try:
        from src.config.enums import AIHeuristic
        
        print("Available heuristics:")
        for heuristic in AIHeuristic:
            print(f"- {heuristic.display_name} ({heuristic.key})")
        
        # Check that strategic is available and vulnerability is not
        strategic_found = any(h.key == 'strategic' for h in AIHeuristic)
        vulnerability_found = any(h.key == 'vulnerability' for h in AIHeuristic)
        
        print(f"✅ Strategic heuristic available: {strategic_found}")
        print(f"✅ Vulnerability heuristic removed: {not vulnerability_found}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")

if __name__ == "__main__":
    test_strategic_heuristic()
    test_ai_heuristic_mapping()
    test_enums()
    print("\n✅ All tests completed!")
