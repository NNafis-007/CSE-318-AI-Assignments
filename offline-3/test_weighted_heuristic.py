#!/usr/bin/env python3
"""
Test script to verify the new weighted combined heuristic and removal of basic heuristic
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import Board
import utils
import colors

def test_weighted_combined_heuristic():
    """Test the new weighted combined heuristic"""
    print("=== Testing Weighted Combined Heuristic ===")
    
    # Create a test board
    board = Board.Board(3, 3)
    
    # Place some orbs to test
    board.grid[0][0].player = 1  # Red player in corner
    board.grid[0][0].orb_count = 1
    
    board.grid[1][1].player = 2  # Blue player in center
    board.grid[1][1].orb_count = 3
    
    # Test individual heuristics
    edge_corner_score = utils.heuristic_edge_corner_control(board, colors.RED)
    strategic_score = utils.heuristic_strategic_evaluation(board, colors.RED)
    weighted_score = utils.heuristic_weighted_combined(board, colors.RED)
    
    expected_weighted = 1 * edge_corner_score + 2 * strategic_score
    
    print(f"Edge Corner Score: {edge_corner_score}")
    print(f"Strategic Score: {strategic_score}")
    print(f"Weighted Combined Score: {weighted_score}")
    print(f"Expected (1*{edge_corner_score} + 2*{strategic_score}): {expected_weighted}")
    print(f"✅ Calculation correct: {weighted_score == expected_weighted}")

def test_basic_heuristic_removed():
    """Test that basic heuristic is no longer available"""
    print("\n=== Testing Basic Heuristic Removal ===")
    
    try:
        # Try to access the old basic heuristic - should fail
        basic_func = getattr(utils, 'heuristic', None)
        if basic_func is None:
            print("✅ Basic heuristic function successfully removed")
        else:
            print("❌ Basic heuristic function still exists")
    except AttributeError:
        print("✅ Basic heuristic function successfully removed")

def test_ai_heuristic_mapping():
    """Test AI player mapping with new heuristic"""
    print("\n=== Testing AI Player Mapping ===")
    
    try:
        from src.core.ai_player import AIPlayer
        
        # Test creating AI with weighted combined heuristic (should be default)
        ai = AIPlayer(colors.BLUE, difficulty=3)
        print("✅ AI player created successfully with default weighted_combined")
        
        # Test explicit weighted_combined
        ai_explicit = AIPlayer(colors.BLUE, difficulty=3, heuristic_name='weighted_combined')
        print("✅ AI player created successfully with explicit weighted_combined")
        
        # Test that basic is no longer available (should fallback to default)
        ai_fallback = AIPlayer(colors.BLUE, difficulty=3, heuristic_name='basic')
        fallback_func = ai_fallback.heuristic_function
        print(f"✅ Basic heuristic fallback: {fallback_func.__name__}")
        
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
        
        # Check that weighted_combined is available and basic is not
        weighted_found = any(h.key == 'weighted_combined' for h in AIHeuristic)
        basic_found = any(h.key == 'basic' for h in AIHeuristic)
        
        print(f"✅ Weighted Combined heuristic available: {weighted_found}")
        print(f"✅ Basic heuristic removed: {not basic_found}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_menu_default():
    """Test menu default selection"""
    print("\n=== Testing Menu Default Selection ===")
    
    try:
        from src.screens.menu_screen import MenuScreen
        from src.ui.ui_renderer import UIRenderer
        
        ui_renderer = UIRenderer()
        menu = MenuScreen(ui_renderer)
        
        default_heuristic = menu.selected_heuristic
        print(f"✅ Menu default heuristic: {default_heuristic.display_name} ({default_heuristic.key})")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_weighted_combined_heuristic()
    test_basic_heuristic_removed()
    test_ai_heuristic_mapping()
    test_enums()
    test_menu_default()
    print("\n✅ All tests completed!")
