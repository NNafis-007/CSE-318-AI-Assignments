import pygame
import sys
from typing import Optional
from src.config.enums import GameState, GameMode
from src.ui.ui_renderer import UIRenderer
from src.screens.menu_screen import MenuScreen
from src.screens.game_screen import GameScreen
from src.config.config import *

class GameStateManager:
    """Manages different game states and transitions"""
    
    def __init__(self):
        self.current_state = GameState.MENU
        self.current_mode: Optional[GameMode] = None
        self.ui_renderer = UIRenderer()
        self.menu_screen = MenuScreen(self.ui_renderer)
        self.game_screen: Optional[GameScreen] = None
    
    def transition_to_game(self, game_mode: GameMode):
        """Transition to game state with specified mode"""
        self.current_mode = game_mode
        self.current_state = GameState.GAME
        self.game_screen = GameScreen(self.ui_renderer, game_mode)
    
    def transition_to_menu(self):
        """Transition back to menu state"""
        self.current_state = GameState.MENU
        self.current_mode = None
        self.game_screen = None
    
    def handle_mouse_click(self, pos: tuple[int, int]):
        """Handle mouse click events based on current state"""
        if self.current_state == GameState.MENU:
            selected_mode = self.menu_screen.handle_mouse_click(pos)
            if selected_mode:
                self.transition_to_game(selected_mode)
        elif self.current_state == GameState.GAME and self.game_screen:
            self.game_screen.handle_mouse_click(pos)
    
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
        pygame.display.set_caption("Chain Reaction Game")
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
        
        # Update animations if we're in game state
        if (self.state_manager.current_state == GameState.GAME and 
            self.state_manager.game_screen):
            game_screen = self.state_manager.game_screen
            
            # Update board animations
            game_screen.board.animation_manager.update(dt)
            
            # Check if animations are complete to allow next input
            if (game_screen.is_processing_turn and 
                game_screen.board.animation_manager.wait_for_completion()):
                game_screen.is_processing_turn = False
    
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
