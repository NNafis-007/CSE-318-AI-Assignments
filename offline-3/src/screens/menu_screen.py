import pygame
from typing import Optional
from src.core.interfaces import EventHandler
from src.ui.ui_renderer import UIRenderer
from src.config.enums import GameMode
from src.config.config import *

class MenuScreen(EventHandler):
    """Handles the main menu screen"""
    
    def __init__(self, ui_renderer: UIRenderer):
        self.ui_renderer = ui_renderer
        self.button_rects = {}
        self.selected_mode: Optional[GameMode] = None
    
    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[GameMode]:
        """Handle mouse clicks on menu buttons"""
        for mode, rect in self.button_rects.items():
            if rect.collidepoint(pos):
                self.selected_mode = mode
                print(f"Selected: {mode.value}")
                return mode
        return None
    
    def handle_key_press(self, key: int) -> Optional[str]:
        """Handle key presses in menu"""
        if key == pygame.K_ESCAPE:
            return "quit"
        else:
            # Handle other key presses if needed
            print(f"Key pressed: {pygame.key.name(key)}")
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the menu screen"""
        surface.fill(WHITE)
        
        # Draw title
        self.ui_renderer.draw_text(surface, "Game Menu", WINDOW_WIDTH // 2, 100, "title")
        
        # Draw menu buttons
        button_x = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
        
        button_configs = [
            (GameMode.TWO_PLAYER, 200),
            (GameMode.HUMAN_VS_AI, 280),
            (GameMode.AI_VS_AI, 360)
        ]
        
        self.button_rects.clear() # Clear previous button rects
        
        # Draw buttons and store their rects
        for mode, y in button_configs:
            rect = self.ui_renderer.draw_button(surface, mode.value, button_x, y)
            self.button_rects[mode] = rect
        

        # Draw instructions
        instructions = [
            " --- Click any cell to place an orb and see cell info ---",
            " --- Reach critical mass to explode and spread orbs ---",
            " --- Eliminate all opponent orbs to win ---",
            " --- Press R to reset |  Press I for game info | ESC to menu ---"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = WINDOW_HEIGHT - 80 + (i * 15)
            self.ui_renderer.draw_text(surface, instruction, WINDOW_WIDTH // 2, y_pos, "small", GRAY)

        # Draw instructions
        self.ui_renderer.draw_text(surface, "Press ESC to quit", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 120, "normal", GRAY)
