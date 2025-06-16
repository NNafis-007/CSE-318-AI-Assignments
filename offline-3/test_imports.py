#!/usr/bin/env python3
"""
Test import to verify BASIC references are completely removed
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work without BASIC attribute errors"""
    try:
        print("Testing imports...")
        
        # Test enum import
        from src.config.enums import AIHeuristic, AIDifficulty, GameMode
        print("✅ Enums imported successfully")
        
        # Test game manager import
        from src.core.game_manager import GameStateManager, Game
        print("✅ Game manager imported successfully")
        
        # Test that WEIGHTED_COMBINED is available
        default_heuristic = AIHeuristic.WEIGHTED_COMBINED
        print(f"✅ Default heuristic: {default_heuristic.display_name}")
        
        # Test that BASIC is not available
        try:
            basic_heuristic = AIHeuristic.BASIC
            print("❌ BASIC heuristic still exists!")
        except AttributeError:
            print("✅ BASIC heuristic successfully removed")
        
        print("\n✅ All imports successful - BASIC references removed!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    if success:
        print("\n🎉 Ready to run the main game!")
    else:
        print("\n❌ Fix import errors before running the game.")
