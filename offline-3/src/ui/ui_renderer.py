import pygame
import sys
import os

# Add parent directory to path for src package imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config.config import *

class UIRenderer:
    """Handles rendering of UI elements"""
    
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
    
    def draw_button(self, surface: pygame.Surface, text: str, x: int, y: int, 
                   width: int = BUTTON_WIDTH, height: int = BUTTON_HEIGHT,
                   bg_color: tuple = LIGHT_GRAY, text_color: tuple = BLACK,
                   border_color: tuple = BLACK, border_width: int = 2) -> pygame.Rect:
        """Draw a button and return its rect for collision detection"""
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, bg_color, button_rect)
        pygame.draw.rect(surface, border_color, button_rect, border_width)
        
        # Center text in button
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        
        return button_rect
    
    def draw_text(self, surface: pygame.Surface, text: str, x: int, y: int,
                 font_size: str = "normal", color: tuple = BLACK, center: bool = True):
        """Draw text on the surface"""
        if font_size == "title":
            font = self.title_font
        elif font_size == "small":
            font = self.small_font
        else:
            font = self.font
        
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
            surface.blit(text_surface, text_rect)
        else:
            surface.blit(text_surface, (x, y))
    
    def draw_grid(self, surface: pygame.Surface):
        """Draw the game grid"""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                x = GRID_X + col * CELL_SIZE
                y = GRID_Y + row * CELL_SIZE
                
                # Draw cell
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, WHITE, cell_rect)
                pygame.draw.rect(surface, BLACK, cell_rect, 1)
