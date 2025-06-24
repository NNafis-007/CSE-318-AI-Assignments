"""
Board class for Chain Reaction game following console version structure.
Compatible with the existing heuristics and minimax implementation.
"""

from typing import Callable, List, Tuple, Dict, Optional
from enum import Enum
import time
import math
import random

class Player(Enum):
    EMPTY = "Empty"
    RED = "Red"
    BLUE = "Blue"

class Cell:
    def __init__(self):
        self.orbs = 0
        self.player = Player.EMPTY
    
    def __str__(self):
        if self.player == Player.EMPTY:
            return "⚫"
        elif self.player == Player.RED:
            return f"🔴{self.orbs}" if self.orbs > 0 else "⚫"
        else:  # BLUE
            return f"🔵{self.orbs}" if self.orbs > 0 else "⚫"

# Game Class - main game logic following console version structure
class ChainReactionGame:
    def __init__(self, rows: int = 9, cols: int = 6):
        self.rows = rows
        self.cols = cols
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.current_player = Player.RED
        self.game_over = False
        self.winner = None
        self.move_count = 0
        self._initialize_critical_mass_cache()
    
    def _initialize_critical_mass_cache(self):
        """Pre-calculate critical mass for each position"""
        self.critical_mass_cache = {}
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                        neighbors += 1
                self.critical_mass_cache[(row, col)] = neighbors
    
    def get_critical_mass(self, row: int, col: int) -> int:
        """Get critical mass for a position (number of neighbors)"""
        return self.critical_mass_cache.get((row, col), 0)
    
    def is_valid_move(self, row: int, col: int, player: Player) -> bool:
        """Check if a move is valid"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
         
        cell = self.board[row][col]
        return cell.player == Player.EMPTY or cell.player == player
    
    def get_valid_moves(self, player: Player) -> List[Tuple[int, int]]:
        """Get all valid moves for a player"""
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves
    
    def make_move(self, row: int, col: int, player: Player) -> bool:
        """Make a move and handle explosions"""
        if not self.is_valid_move(row, col, player) or self.game_over:
            return False

        self.board[row][col].orbs += 1
        self.board[row][col].player = player
        self.move_count += 1
        
        self._handle_explosions()
        self._check_win_condition()
        # Switch player if game is not over
        if not self.game_over:
            self.current_player = Player.BLUE if self.current_player == Player.RED else Player.RED
        return True
    
    def _handle_explosions(self):
        """Handle chain explosions with game-over checking to prevent infinite loops"""
        explosion_occurred = True
        iteration_count = 0
        max_iterations = 1000000  # Safety limit
        
        while explosion_occurred and iteration_count < max_iterations:
            explosion_occurred = False
            iteration_count += 1
            
            # Find all cells that need to explode
            exploding_cells = []
            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.board[row][col]
                    if (cell.orbs >= self.get_critical_mass(row, col) and 
                        cell.player != Player.EMPTY):
                        exploding_cells.append((row, col))
            
            if exploding_cells:
                explosion_occurred = True  
                
                for row, col in exploding_cells:
                    self._explode_cell(row, col)
                    
                if self._is_game_over_during_explosions():
                    break
        
        if iteration_count >= max_iterations:
            print(f"⚠️  Explosion loop terminated after {max_iterations} iterations for safety")
    
    def _is_game_over_during_explosions(self) -> bool:
        """Check if game is over during explosion processing"""
        red_orbs = 0
        blue_orbs = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player == Player.RED:
                    red_orbs += cell.orbs
                elif cell.player == Player.BLUE:
                    blue_orbs += cell.orbs
        
        total_orbs = red_orbs + blue_orbs
        if total_orbs > 0 and self.move_count > 2:
            return (red_orbs == 0 and blue_orbs > 0) or (blue_orbs == 0 and red_orbs > 0)
        
        return False
    
    def _explode_cell(self, row: int, col: int):
        """Explode a single cell"""
        cell = self.board[row][col]
        exploding_player = cell.player
        critical_mass = self.get_critical_mass(row, col)
        orbs_to_distribute = critical_mass
        cell.orbs -= orbs_to_distribute
        if cell.orbs <= 0:
            cell.orbs = 0
            cell.player = Player.EMPTY
    
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in neighbors:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbor_cell = self.board[nr][nc]
                neighbor_cell.orbs += 1
                neighbor_cell.player = exploding_player
    
    def _check_win_condition(self):
        """Check if game is over and determine winner"""
        red_orbs = 0
        blue_orbs = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player == Player.RED:
                    red_orbs += cell.orbs
                elif cell.player == Player.BLUE:
                    blue_orbs += cell.orbs
        
        total_orbs = red_orbs + blue_orbs

        if total_orbs > 0 and self.move_count >= 2:
            if red_orbs > 0 and blue_orbs == 0:
                self.game_over = True
                self.winner = Player.RED
            elif blue_orbs > 0 and red_orbs == 0:
                self.game_over = True
                self.winner = Player.BLUE
    
    def get_score(self) -> Dict[Player, int]:
        """Get current score for each player"""
        scores = {Player.RED: 0, Player.BLUE: 0}
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player in scores:
                    scores[cell.player] += cell.orbs
        return scores
    
    def display_board(self):
        """Display the current board state"""
        print("\nCurrent Board:")
        for row in range(self.rows):
            print(' '.join(str(self.board[row][col]) for col in range(self.cols)))
        
        scores = self.get_score()
        print(f"\nScores - Red: {scores[Player.RED]}, Blue: {scores[Player.BLUE]}")
        print(f"Current Player: {self.current_player.value}")
    
    def copy(self):
        """Create a deep copy of the game state"""
        new_game = ChainReactionGame(self.rows, self.cols)
        new_game.current_player = self.current_player
        new_game.game_over = self.game_over
        new_game.winner = self.winner
        new_game.move_count = self.move_count
        
        for row in range(self.rows):
            for col in range(self.cols):
                new_game.board[row][col].orbs = self.board[row][col].orbs
                new_game.board[row][col].player = self.board[row][col].player
        
        return new_game

# Backward compatibility - Board class that wraps ChainReactionGame
class Board:# Backward compatibility - Board class that wraps ChainReactionGame
    """
    Wrapper around ChainReactionGame to maintain compatibility with existing code.
    Maps between the old grid-based interface and new console version structure.
    """
    def __init__(self, rows=9, cols=6):
        """Initialize the board with configurable dimensions."""
        self.rows = rows
        self.cols = cols
        self.game = ChainReactionGame(rows, cols)
        # Create a compatibility grid that maps to game board
        self._update_grid()
    
    def _update_grid(self):
        """Update the grid representation from game state"""
        self.grid = []
        for row in range(self.rows):
            grid_row = []
            for col in range(self.cols):
                # Create a simple cell wrapper
                cell_wrapper = SimpleCell(row, col, self.rows, self.cols)
                game_cell = self.game.board[row][col]
                # Map from Player enum to integer
                if game_cell.player == Player.RED:
                    cell_wrapper.player = 1
                elif game_cell.player == Player.BLUE:
                    cell_wrapper.player = 2
                else:
                    cell_wrapper.player = None
                cell_wrapper.orb_count = game_cell.orbs
                grid_row.append(cell_wrapper)
            self.grid.append(grid_row)
    
    def _sync_to_game(self):
        """Sync changes from grid back to game state"""
        for row in range(self.rows):
            for col in range(self.cols):
                grid_cell = self.grid[row][col]
                game_cell = self.game.board[row][col]
                # Map from integer to Player enum
                if grid_cell.player == 1:
                    game_cell.player = Player.RED
                elif grid_cell.player == 2:
                    game_cell.player = Player.BLUE
                else:
                    game_cell.player = Player.EMPTY
                game_cell.orbs = grid_cell.orb_count
    
    def make_move(self, player, row, col, undo_info=None):
        """Make a move on the board with optional undo information."""
        if undo_info is None:
            undo_info = []
        
        # Convert player number to Player enum
        player_enum = Player.RED if player == 1 else Player.BLUE
        
        # Store undo information
        if undo_info is not None:
            game_cell = self.game.board[row][col]
            old_player = 1 if game_cell.player == Player.RED else (2 if game_cell.player == Player.BLUE else None)
            undo_info.append([row, col, old_player, game_cell.orbs])
        
        # Make the move using game logic
        success = self.game.make_move(row, col, player_enum)
        
        # Update grid representation
        self._update_grid()
        
        return success
    
    def get_critical_mass(self, row, col):
        """Get the critical mass for a cell at given position."""
        return self.game.get_critical_mass(row, col)
    
    def is_terminal(self):
        """Check if the game is in a terminal state."""
        return self.game.game_over
    
    def print_board(self):
        """Print the current board state for debugging."""
        self.game.display_board()

# Simple cell wrapper for backward compatibility
class SimpleCell:
    """Simple cell class for AI compatibility"""
    def __init__(self, row, col, grid_rows=9, grid_cols=6):
        self.row = row
        self.col = col
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.player = None
        self.orb_count = 0
        self.critical_mass = self._calculate_critical_mass()
    
    def _calculate_critical_mass(self):
        """Calculate critical mass based on position"""
        # Corner cells (2 neighbors)
        if ((self.row == 0 or self.row == self.grid_rows - 1) and 
            (self.col == 0 or self.col == self.grid_cols - 1)):
            return 2
        # Edge cells (3 neighbors)
        elif (self.row == 0 or self.row == self.grid_rows - 1 or 
              self.col == 0 or self.col == self.grid_cols - 1):
            return 3
        # Center cells (4 neighbors)
        else:
            return 4

    def add_orb(self, player):
        """Add an orb to this cell"""
        if self.player is None or self.player == player:
            self.player = player
            self.orb_count += 1
            return True
        return False
