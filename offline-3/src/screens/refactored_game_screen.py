"""
Refactored Game Screen - Clean separation between UI and game logic.
This module only handles user input, coordinates between game logic and rendering.
"""

import pygame
import sys
import os
from typing import Optional, Tuple, List

# Add parent directory to path for src package imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.core.interfaces import EventHandler
from src.ui.game_renderer import GameRenderer
from src.ui.enhanced_animation import AnimationManager
from src.core.game_logic import ChainReactionGame
from src.config.enums import GameMode, AIDifficulty, AIHeuristic
from src.config.config import *


class RefactoredGameScreen(EventHandler):
    """
    Handles the game screen with clean separation of concerns.
    Coordinates between game logic, UI rendering, and user input.
    """
    
    def __init__(self, game_mode: GameMode, ai_difficulty: AIDifficulty = AIDifficulty.MEDIUM, 
                 ai_heuristic: AIHeuristic = AIHeuristic.WEIGHTED_COMBINED):
        # Game mode and AI settings
        self.game_mode = game_mode
        self.ai_difficulty = ai_difficulty.depth if ai_difficulty else 3
        self.ai_heuristic = ai_heuristic.key if ai_heuristic else "weighted_combined"
        
        # Core game logic (separated from UI)
        self.game = ChainReactionGame(GRID_ROWS, GRID_COLS)
        
        # UI and rendering (separated from game logic)
        self.renderer = GameRenderer()
        self.animation_manager = AnimationManager()
        
        # UI state (only for presentation, not game logic)
        self.hover_cell: Optional[Tuple[int, int]] = None
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.is_processing_turn = False  # Prevent input during animations
        
        # AI player setup
        self.ai_player = None
        self.human_player = 1  # Default: Human is player 1
        
        if self.game_mode == GameMode.HUMAN_VS_AI:
            self._setup_ai_mode()    
    def _setup_ai_mode(self):
        """Setup AI player for Human vs AI mode"""
        try:
            from src.core.ai_player import AIPlayer
            from src import colors
            
            print("\n=== Human vs AI Setup ===")
            print("You are Player 1 (Red), AI is Player 2 (Blue)")
            
            self.human_player = 1  # Human is always player 1 (Red)
            ai_color = colors.BLUE  # AI is player 2 (Blue)
            
            # Create AI player
            self.ai_player = AIPlayer(
                color=ai_color,
                difficulty=self.ai_difficulty,
                heuristic_name=self.ai_heuristic
            )
            
            print(f"AI configured: Difficulty={self.ai_difficulty}, Heuristic={self.ai_heuristic}")
            
        except ImportError as e:
            print(f"Warning: Could not import AI player: {e}")
            print("AI mode will not be available.")
            self.ai_player = None
    
    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[str]:
        """Handle mouse clicks on the game board"""
        # Don't process clicks during animations
        if self.is_processing_turn:
            return None
        
        # Convert mouse position to cell coordinates
        cell_coords = self.renderer.get_cell_from_mouse_pos(pos)
        if not cell_coords:
            return None  # Click outside grid
        
        row, col = cell_coords
        self.selected_cell = cell_coords
        
        # Handle different game modes
        if self.game_mode == GameMode.TWO_PLAYER:
            return self._handle_two_player_move(row, col)
        elif self.game_mode == GameMode.HUMAN_VS_AI:
            return self._handle_human_vs_ai_move(row, col)
        elif self.game_mode == GameMode.AI_VS_AI:
            print("AI vs AI mode - no manual moves allowed!")
            return None
        
        return None
    
    def _handle_two_player_move(self, row: int, col: int) -> Optional[str]:
        """Handle move in two-player mode"""
        game_state = self.game.get_game_state()
        
        if game_state.game_over:
            print(f"🎮 Game is over! Player {game_state.winner} has won!")
            return None
        
        # Try to make the move
        result = self.game.make_move(row, col)
        
        if result['success']:
            # Set processing flag to prevent input during animations
            self.is_processing_turn = True
            
            # Add animations for explosions
            for explosion in result['explosions']:
                if explosion['exploded']:
                    self.animation_manager.add_explosion_effect(explosion['position'])
                    
                    # Add moving orb animations for affected neighbors
                    for neighbor_pos in explosion['affected_neighbors']:
                        self.animation_manager.add_moving_orb(
                            explosion['position'], neighbor_pos,
                            game_state.current_player, duration=0.3
                        )
            
            # Print game state
            self._print_move_result(result)
            
        else:
            print(f"❌ {result['error']} at ({row}, {col})")        
        return None
    
    def _handle_human_vs_ai_move(self, row: int, col: int) -> Optional[str]:
        """Handle move in Human vs AI mode"""
        if self._is_ai_turn():
            print("It's AI's turn. Please wait...")
            return None
        
        game_state = self.game.get_game_state()
        
        if game_state.game_over:
            print(f"🎮 Game is over! Player {game_state.winner} has won!")
            return None
        
        # Human player's turn
        result = self.game.make_move(row, col)
        
        if result['success']:
            self.is_processing_turn = True
            
            # Add animations
            self._add_move_animations(result)
            
            # Save game state to file after human move
            self._save_game_state_to_file("Human Move")
            
            # Print move result
            print(f"\n🎮 Human played at ({row}, {col})")
            self._print_move_result(result)
            
            # Schedule AI turn if game continues
            if not result['game_state']['game_over']:
                pygame.time.set_timer(pygame.USEREVENT + 1, 500)  # 500ms delay
            
        else:
            print(f"❌ {result['error']} at ({row}, {col})")
        
        return None
    
    def _add_move_animations(self, move_result: dict):
        """Add appropriate animations for a move result"""
        for explosion in move_result['explosions']:
            if explosion['exploded']:
                # Add explosion effect
                self.animation_manager.add_explosion_effect(explosion['position'])
                
                # Add moving orb animations
                for neighbor_pos in explosion['affected_neighbors']:
                    self.animation_manager.add_moving_orb(
                        explosion['position'], neighbor_pos, move_result['game_state']['current_player'], duration=0.3
                    )
    
    def _print_move_result(self, result: dict):
        """Print detailed information about a move result"""
        state = result['game_state']
        print("="*50)
        print(f"📊 GAME STATE:")
        print(f"Current Player: {state['current_player']}")
        print(f"Total Moves: {state['total_moves']}")
        print(f"Player 1 Cells: {state['player1_cells']}")
        print(f"Player 2 Cells: {state['player2_cells']}")
        print(f"Total Orbs: {state['total_orbs']}")
        
        if state['last_chain_length'] > 1:
            print(f"💥 Chain Reaction Length: {state['last_chain_length']}")
        
        if state['game_over']:
            print(f"🎉 GAME OVER! Player {state['winner']} wins!")
        print("="*50)
    
    def _save_game_state_to_file(self, move_type: str):
        """Save current game state to gamestate.txt file"""
        try:
            with open("gamestate.txt", 'w') as f:
                # Header line: Who made the current move
                f.write(f"{move_type}:\n")
                
                # Board state: rows x cols cells
                game_state = self.game.get_game_state()
                for row in range(game_state.rows):
                    row_data = []
                    for col in range(game_state.cols):
                        cell = game_state.get_cell(row, col)
                        if cell and cell.player:  # Cell has orbs
                            # Format: <n><C> where n is orb count, C is R(Red)/B(Blue)
                            color = "R" if cell.player == 1 else "B"
                            row_data.append(f"{cell.orb_count}{color}")
                        else:  # Empty cell
                            row_data.append("0")
                    f.write(" ".join(row_data) + "\n")
                
                # Add empty line at the end to match format
                f.write("\n")
            
            print(f"Game state saved to gamestate.txt ({move_type})")        
        except Exception as e:
            print(f"Error saving game state: {e}")

    def _is_ai_turn(self) -> bool:
        """Check if it's the AI's turn"""
        return (self.game_mode == GameMode.HUMAN_VS_AI and 
                self.ai_player is not None and 
                self.game.get_game_state().current_player != self.human_player)
    
    def _process_ai_turn(self):
        """Process the AI's turn"""
        # Check if it's AI's turn and game is not over
        if not self._is_ai_turn():
            return
        
        # Check game over before calculating AI move
        game_state = self.game.get_game_state()
        if game_state.game_over:
            print(f"🎮 Game is over! Player {game_state.winner} has won!")
            return
        
        print(f"\nAI (Player {game_state.current_player}) is thinking...")
        
        # Get AI board representation
        ai_board = self._get_board_copy_for_ai()
        
        # Get best move from AI (only if AI player is available)
        if self.ai_player is None:
            print("AI player not available!")
            self.is_processing_turn = False
            return
        
        best_move = self.ai_player.get_best_move(ai_board)
        
        if best_move:
            row, col = best_move
            result = self.game.make_move(row, col)
            
            if result['success']:
                # Add animations
                self._add_move_animations(result)
                
                # Save game state to file after AI move
                self._save_game_state_to_file("AI Move")
                
                print(f"AI moved to ({row}, {col})")
                self._print_move_result(result)
            else:
                print(f"AI move failed: {result['error']}")
        else:
            print("AI couldn't find a valid move!")        
        # Reset processing flag        self.is_processing_turn = False
    
    def _get_board_copy_for_ai(self):
        """Get a copy of the board in the format expected by AI"""
        from src import Board
        
        game_state = self.game.get_game_state()
        ai_board = Board.Board(game_state.rows, game_state.cols)
        
        # Copy current game state to AI board format
        for i in range(game_state.rows):
            for j in range(game_state.cols):
                cell = game_state.get_cell(i, j)
                ai_cell = ai_board.grid[i][j]
                ai_cell.player = cell.player
                ai_cell.orb_count = cell.orb_count
        
        return ai_board
    
    def handle_mouse_motion(self, pos: tuple[int, int]):
        """Handle mouse movement for hover effects"""
        self.hover_cell = self.renderer.get_cell_from_mouse_pos(pos)
    
    def handle_key_press(self, key: int) -> Optional[str]:
        """Handle key presses in game screen"""
        if key == pygame.K_ESCAPE:
            return "back_to_menu"
        elif key == pygame.K_r:  # Reset game with 'R' key
            self.game.reset_game()
            self.animation_manager.clear_all()
            self.selected_cell = None
            self.is_processing_turn = False
            print("🔄 Game reset! Press R again anytime to reset.")
        elif key == pygame.K_i:  # Info key - show game state
            state = self.game.get_game_state()
            info = state.get_game_info()
            print("\n" + "="*40)
            print("📊 COMPLETE GAME STATE:")
            for key, value in info.items():
                if key != 'valid_moves':  # Don't print all valid moves
                    print(f"{key.replace('_', ' ').title()}: {value}")
            print("="*40)
        
        return None
    
    def update(self, dt: float):
        """Update game screen (animations, AI processing, etc.)"""
        # Update animation timer
        self.renderer.update_animation_time(dt)
        
        # Update animations
        self.animation_manager.update(dt)
        
        # Check if animations are complete to allow next input
        if (self.is_processing_turn and 
            self.animation_manager.wait_for_completion()):
            self.is_processing_turn = False
    
    def draw(self, surface: pygame.Surface):
        """Draw the game screen"""
        # Get current game state
        game_state = self.game.get_game_state()
        
        # Draw the main game using the renderer
        self.renderer.draw_game_screen(
            surface, game_state, 
            hover_cell=self.hover_cell,
            selected_cell=self.selected_cell
        )
        
        # Draw animations on top
        self.animation_manager.draw(surface, self.renderer)
    
    def get_game_state(self):
        """Get the current game state for external use"""
        return self.game.get_game_state()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.game.reset_game()
        self.animation_manager.clear_all()
        self.selected_cell = None
        self.hover_cell = None
        self.is_processing_turn = False
