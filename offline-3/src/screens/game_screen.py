import pygame
from typing import Optional, Tuple
from src.core.interfaces import EventHandler
from src.ui.ui_renderer import UIRenderer
from src.config.enums import GameMode
from src.config.config import *
from src.core.cell import Cell

class GameBoard:
    """Represents the game board state"""
    
    def __init__(self, rows: int = GRID_ROWS, cols: int = GRID_COLS):
        self.rows = rows
        self.cols = cols
        self.board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the given position is valid"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_cell_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional['Cell']:
        """Convert mouse position to board coordinates"""
        mouse_x, mouse_y = mouse_pos
        
        # Check if click is within the grid
        if (GRID_X <= mouse_x <= GRID_X + GRID_WIDTH and
            GRID_Y <= mouse_y <= GRID_Y + GRID_HEIGHT):
            
            col = (mouse_x - GRID_X) // CELL_SIZE
            row = (mouse_y - GRID_Y) // CELL_SIZE
            
            if self.is_valid_position(row, col):
                return self.board[row][col]
        
        return None

class GameScreen(EventHandler):
    """Handles the game screen / main game loop"""
    
    def __init__(self, ui_renderer: UIRenderer, game_mode: GameMode):
        self.ui_renderer = ui_renderer
        self.game_mode = game_mode
        self.board = GameBoard()
    
    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[str]:
        """Handle mouse clicks on the game board"""
        cell = self.board.get_cell_from_mouse_pos(pos)
        if cell:
            print(cell)
            
        return None
    
    def handle_key_press(self, key: int) -> Optional[str]:
        """Handle key presses in game screen"""
        if key == pygame.K_ESCAPE:
            return "back_to_menu"
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the game screen"""
        surface.fill(WHITE)
        
        # Draw title with current game mode
        self.ui_renderer.draw_text(surface, f"Mode: {self.game_mode.value}", 
                                 WINDOW_WIDTH // 2, 50, "title")
        
        # Draw the grid
        self.ui_renderer.draw_grid(surface)
        
        # Draw instructions
        self.ui_renderer.draw_text(surface, "Click any cell to see coordinates in console", 
                                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30, "small", GRAY)
        
        self.ui_renderer.draw_text(surface, "Press ESC to go back to menu", 
                                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 15, "small", GRAY)
