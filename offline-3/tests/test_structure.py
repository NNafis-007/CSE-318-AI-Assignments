"""
Test script to verify the modular structure works correctly
"""

import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_imports():
    """Test that all modules can be imported successfully"""
    try:
        from src.config import config
        print("✓ src.config.config imported successfully")
        
        from src.config import enums
        print("✓ src.config.enums imported successfully")
        
        from src.core import interfaces
        print("✓ src.core.interfaces imported successfully")
        
        from src.ui import ui_renderer
        print("✓ src.ui.ui_renderer imported successfully")
        
        from src.screens import menu_screen
        print("✓ src.screens.menu_screen imported successfully")
        
        from src.screens import game_screen
        print("✓ src.screens.game_screen imported successfully")
        
        from src.core import game_manager
        print("✓ src.core.game_manager imported successfully")

        from src.core.cell import Cell
        print("✓ src.core.cell imported successfully")
        
        print("\n✅ All modules imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"Current Python path: {sys.path}")
        print(f"Project root: {project_root}")
        return False

def test_enums():
    """Test enum values"""
    from src.config.enums import GameState, GameMode
    
    print("\nTesting enums:")
    print(f"GameState.MENU: {GameState.MENU}")
    print(f"GameState.GAME: {GameState.GAME}")
    print(f"GameMode.TWO_PLAYER: {GameMode.TWO_PLAYER}")
    print(f"GameMode.HUMAN_VS_AI: {GameMode.HUMAN_VS_AI}")
    print(f"GameMode.AI_VS_AI: {GameMode.AI_VS_AI}")

def test_config():
    """Test configuration values"""
    from src.config import config
    
    print("\nTesting configuration:")
    print(f"Window size: {config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    print(f"Grid size: {config.GRID_ROWS}x{config.GRID_COLS}")
    print(f"Cell col size: {config.CELL_SIZE}")
    print(f"Cell row size: {config.CELL_SIZE}")

if __name__ == "__main__":
    print("Running modular structure tests...\n")
    
    if test_imports():
        test_enums()
        test_config()
        print("\n🎉 All tests passed! The modular structure is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the imports.")
