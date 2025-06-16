import pygame
from typing import Optional, Tuple
from src.core.interfaces import EventHandler
from src.ui.ui_renderer import UIRenderer
from src.config.enums import GameMode, AIDifficulty, AIHeuristic
from src.config.config import *

class MenuScreen(EventHandler):
    """Handles the main menu screen"""
    
    def __init__(self, ui_renderer: UIRenderer):
        self.ui_renderer = ui_renderer
        self.button_rects = {}
        self.selected_mode: Optional[GameMode] = None
        self.show_ai_config = False
        self.selected_difficulty: AIDifficulty = AIDifficulty.MEDIUM
        self.selected_heuristic: AIHeuristic = AIHeuristic.WEIGHTED_COMBINED
        self.difficulty_rects = {}
        self.heuristic_rects = {}
        self.back_button_rect = None
        self.start_game_rect = None
    
    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[Tuple[GameMode, AIDifficulty, AIHeuristic]]:
        """Handle mouse clicks on menu buttons"""
        if self.show_ai_config:
            # Handle AI configuration screen clicks
            
            # Back button
            if self.back_button_rect and self.back_button_rect.collidepoint(pos):
                self.show_ai_config = False
                return None
                
            # Start game button
            if self.start_game_rect and self.start_game_rect.collidepoint(pos):
                return (GameMode.HUMAN_VS_AI, self.selected_difficulty, self.selected_heuristic)
            
            # Difficulty selection
            for difficulty, rect in self.difficulty_rects.items():
                if rect.collidepoint(pos):
                    self.selected_difficulty = difficulty
                    print(f"Selected difficulty: {difficulty.display_name}")
                    return None
            
            # Heuristic selection
            for heuristic, rect in self.heuristic_rects.items():
                if rect.collidepoint(pos):
                    self.selected_heuristic = heuristic
                    print(f"Selected heuristic: {heuristic.display_name}")
                    return None
        else:
            # Handle main menu clicks
            for mode, rect in self.button_rects.items():
                if rect.collidepoint(pos):
                    self.selected_mode = mode
                    print(f"Selected: {mode.value}")
                    
                    if mode == GameMode.HUMAN_VS_AI:
                        self.show_ai_config = True
                        return None
                    else:
                        # For other modes, return with default AI settings
                        return (mode, self.selected_difficulty, self.selected_heuristic)
        return None
    
    def handle_key_press(self, key: int) -> Optional[str]:
        """Handle key presses in menu"""
        if key == pygame.K_ESCAPE:
            return "quit"
        else:            # Handle other key presses if needed
            print(f"Key pressed: {pygame.key.name(key)}")
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the menu screen"""
        surface.fill(WHITE)
        
        if self.show_ai_config:
            self._draw_ai_config_screen(surface)
        else:
            self._draw_main_menu(surface)
    
    def _draw_main_menu(self, surface: pygame.Surface):
        """Draw the main menu"""
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
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = WINDOW_HEIGHT - 80 + (i * 15)
            self.ui_renderer.draw_text(surface, instruction, WINDOW_WIDTH // 2, y_pos, "small", GRAY)

        # Draw instructions
        self.ui_renderer.draw_text(surface, "Press ESC to quit", WINDOW_WIDTH // 2, WINDOW_HEIGHT - 120, "normal", GRAY)
    
    def _draw_ai_config_screen(self, surface: pygame.Surface):
        """Draw the AI configuration screen"""
        # Draw title
        self.ui_renderer.draw_text(surface, "AI Configuration", WINDOW_WIDTH // 2, 80, "title")
        
        # Clear previous rects
        self.difficulty_rects.clear()
        self.heuristic_rects.clear()
          # Draw difficulty selection
        self.ui_renderer.draw_text(surface, "Select Difficulty:", WINDOW_WIDTH // 4, 150, "normal")
        
        difficulty_y = 180
        for difficulty in AIDifficulty:
            bg_color = BLUE if difficulty == self.selected_difficulty else LIGHT_GRAY
            rect = self.ui_renderer.draw_button(
                surface, 
                f"{difficulty.display_name} (Depth {difficulty.depth})",
                50,
                difficulty_y,
                bg_color=bg_color
            )
            self.difficulty_rects[difficulty] = rect
            difficulty_y += 60
        
        # Draw heuristic selection
        self.ui_renderer.draw_text(surface, "Select Heuristic:", 3 * WINDOW_WIDTH // 4, 150, "normal")
        
        heuristic_y = 180
        for heuristic in AIHeuristic:
            bg_color = BLUE if heuristic == self.selected_heuristic else LIGHT_GRAY
            rect = self.ui_renderer.draw_button(
                surface,
                heuristic.display_name,
                WINDOW_WIDTH // 2 + 50,
                heuristic_y,
                bg_color=bg_color
            )
            self.heuristic_rects[heuristic] = rect
            heuristic_y += 60
        
        # Draw control buttons
        button_x = (WINDOW_WIDTH - BUTTON_WIDTH) // 2
        
        # Back button
        self.back_button_rect = self.ui_renderer.draw_button(
            surface, "Back", button_x - 120, WINDOW_HEIGHT - 120
        )
          # Start game button
        self.start_game_rect = self.ui_renderer.draw_button(
            surface, "Start Game", button_x + 120, WINDOW_HEIGHT - 120, bg_color=BLUE
        )
        
        # Draw current selection info
        info_text = f"Selected: {self.selected_difficulty.display_name} + {self.selected_heuristic.display_name}"
        self.ui_renderer.draw_text(surface, info_text, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 160, "normal", GRAY)
