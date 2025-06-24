"""
Refactored Game Manager with clean separation of concerns.
Updated to work with the new UI/Logic separation.
"""

import pygame
import sys
from typing import Optional, Tuple

# Add parent directory to path for src package imports
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.config.enums import GameState, GameMode, AIDifficulty, AIHeuristic
from src.ui.ui_renderer import UIRenderer
from src.screens.menu_screen import MenuScreen
from src.screens.refactored_game_screen import RefactoredGameScreen
from src.config.config import *


class GameStateManager:
    """Manages different game states and transitions"""
    
    def __init__(self):
        self.current_state = GameState.MENU
        self.current_mode: Optional[GameMode] = None
        self.ui_renderer = UIRenderer()
        self.menu_screen = MenuScreen(self.ui_renderer)
        self.game_screen: Optional[RefactoredGameScreen] = None
    
    def transition_to_game(self, game_mode: GameMode, ai_difficulty: AIDifficulty = AIDifficulty.MEDIUM, ai_heuristic: AIHeuristic = AIHeuristic.WEIGHTED_COMBINED):
        """Transition to game state with specified mode and AI settings"""
        self.current_mode = game_mode
        self.current_state = GameState.GAME
        self.game_screen = RefactoredGameScreen(game_mode, ai_difficulty, ai_heuristic)
        
    def transition_to_menu(self):
        """Transition back to menu state"""
        self.current_state = GameState.MENU
        self.current_mode = None
        self.game_screen = None
    
    def handle_mouse_click(self, pos: tuple[int, int]):
        """Handle mouse click events based on current state"""
        if self.current_state == GameState.MENU:
            result = self.menu_screen.handle_mouse_click(pos)
            if result:
                game_mode, ai_difficulty, ai_heuristic = result
                self.transition_to_game(game_mode, ai_difficulty, ai_heuristic)
        elif self.current_state == GameState.GAME and self.game_screen:
            self.game_screen.handle_mouse_click(pos)
    
    def handle_mouse_motion(self, pos: tuple[int, int]):
        """Handle mouse motion events"""
        if self.current_state == GameState.GAME and self.game_screen:
            self.game_screen.handle_mouse_motion(pos)
    
    def handle_key_press(self, key: int) -> bool:
        """Handle key press events based on current state. Returns True if should quit"""
        if self.current_state == GameState.MENU:
            result = self.menu_screen.handle_key_press(key)
            if result == "quit":
                return True
        elif self.current_state == GameState.GAME and self.game_screen:
            result = self.game_screen.handle_key_press(key)
            if result == "back_to_menu":
                self.transition_to_menu()
        
        return False
    
    def update(self, dt: float):
        """Update the current screen"""
        if self.current_state == GameState.GAME and self.game_screen:
            self.game_screen.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Draw the current screen"""
        if self.current_state == GameState.MENU:
            self.menu_screen.draw(surface)
        elif self.current_state == GameState.GAME and self.game_screen:
            self.game_screen.draw(surface)


class Game:
    """Main game class following Single Responsibility Principle"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chain Reaction Game - Refactored")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_manager = GameStateManager()
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.state_manager.handle_mouse_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.state_manager.handle_mouse_motion(event.pos)
            elif event.type == pygame.KEYDOWN:
                should_quit = self.state_manager.handle_key_press(event.key)
                if should_quit:
                    self.running = False
            elif event.type == pygame.USEREVENT + 1:
                # Handle AI turn timer event
                if (self.state_manager.current_state == GameState.GAME and 
                    self.state_manager.game_screen):
                    self.state_manager.game_screen._process_ai_turn()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
    
    def update(self):
        """Update game logic"""
        # Get delta time for smooth animations
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        
        # Update the current screen
        self.state_manager.update(dt)
    
    def draw(self):
        """Draw everything to the screen"""
        self.state_manager.draw(self.screen)
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
