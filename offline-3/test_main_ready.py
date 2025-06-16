#!/usr/bin/env python3
"""
Final verification that main.py can be imported without errors
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_main_import():
    """Test that main.py imports work correctly"""
    try:
        print("Testing main.py import chain...")
        
        # This should import without any BASIC attribute errors
        from src.core.game_manager import Game
        print("✅ Game class imported successfully")
        
        # Create a game instance to test initialization
        game = Game()
        print("✅ Game instance created successfully")
        
        # Check the default heuristic
        default_heuristic = game.state_manager.menu_screen.selected_heuristic
        print(f"✅ Default menu heuristic: {default_heuristic.display_name}")
        
        print("\n🎉 Main game is ready to run!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_main_import()
    if success:
        print("\n✅ You can now run: python main.py")
    else:
        print("\n❌ There are still issues to fix.")
