"""
Pure game logic for Chain Reaction - completely separated from UI code.
This module contains only the core game rules, state management, and business logic.
"""

import sys
import os
from typing import Optional, Tuple, List, Dict

# Add parent directory to path for src package imports
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.core.cell import Cell


class GameState:
    """Represents the complete state of a Chain Reaction game"""
    
    def __init__(self, rows: int = 9, cols: int = 6):
        self.rows = rows
        self.cols = cols
        self.current_player = 1  # Start with player 1
        self.game_over = False
        self.winner: Optional[int] = None
        self.player_cells = {1: 0, 2: 0}  # Track cells owned by each player
        
        # Create a 2D grid of Cell objects
        self.board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        
        # Game statistics
        self.total_moves = 0
        self.explosion_chain_length = 0
        self.last_move_player = None  # Track who made the last move
        
        # Game history for undo functionality (if needed later)
        self.move_history: List[Dict] = []

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the given position is valid"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get the cell at the specified position"""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def can_place_orb(self, row: int, col: int) -> bool:
        """Check if current player can place an orb at the given position"""
        if self.game_over:
            return False
            
        cell = self.get_cell(row, col)
        if cell:
            return cell.can_place_orb(self.current_player)
        return False

    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Get all valid moves for the current player"""
        valid_moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.can_place_orb(row, col):
                    valid_moves.append((row, col))
        return valid_moves

    def get_game_info(self) -> Dict:
        """Get current game state information"""
        player1_cells = self.player_cells[1]
        player2_cells = self.player_cells[2]
        total_orbs = sum(cell.orb_count for row in self.board for cell in row if not cell.is_empty())
                
        return {
            'current_player': self.current_player,
            'total_moves': self.total_moves,
            'player1_cells': player1_cells,
            'player2_cells': player2_cells,
            'total_orbs': total_orbs,
            'game_over': self.game_over,
            'winner': self.winner,
            'last_chain_length': self.explosion_chain_length,
            'valid_moves': self.get_valid_moves()
        }

    def reset_game(self):
        """Reset the game to initial state"""
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.player_cells = {1: 0, 2: 0}
        self.total_moves = 0
        self.explosion_chain_length = 0
        self.last_move_player = None
        self.move_history.clear()
        
        # Reset all cells
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col].reset()


class ChainReactionGame:
    """
    Core game engine for Chain Reaction.
    Handles all game logic without any UI dependencies.
    """
    
    def __init__(self, rows: int = 9, cols: int = 6):
        self.state = GameState(rows, cols)
        
    def make_move(self, row: int, col: int) -> Dict:
        """
        Make a move at the specified position.
        
        Args:
            row: Row position
            col: Column position
            
        Returns:
            dict: Move result containing success status, explosions, and game state changes
        """
        if not self.state.can_place_orb(row, col):
            return {
                'success': False,
                'error': 'Invalid move',
                'explosions': [],
                'game_state': self.state.get_game_info()
            }
        
        cell = self.state.get_cell(row, col)
        if not cell:
            return {
                'success': False,
                'error': 'Invalid position',
                'explosions': [],
                'game_state': self.state.get_game_info()
            }
        
        # Store move in history
        move_data = {
            'player': self.state.current_player,
            'position': (row, col),
            'move_number': self.state.total_moves + 1
        }
        
        # Place the orb
        success = cell.add_orb(self.state.current_player)
        if not success:
            return {
                'success': False,
                'error': 'Failed to place orb',
                'explosions': [],
                'game_state': self.state.get_game_info()
            }
            
        self.state.total_moves += 1
        self.state.player_cells[self.state.current_player] += 1
        
        # Handle explosions if necessary
        explosions = []
        if cell.orb_count >= cell.critical_mass:
            explosions = self._handle_explosions((row, col))
        
        # Check for game over
        self._check_game_over()
        
        # Switch to next player if game continues
        if not self.state.game_over:
            self._switch_player()
        
        # Add to history
        move_data['explosions'] = explosions
        move_data['result_state'] = self.state.get_game_info()
        self.state.move_history.append(move_data)
        
        return {
            'success': True,
            'explosions': explosions,
            'game_state': self.state.get_game_info(),
            'move_data': move_data
        }
    
    def _handle_explosions(self, initial_explosion: Tuple[int, int]) -> List[Dict]:
        """
        Handle chain explosions starting from initial explosion points.
        
        Args:
            initial_explosion: Cell (row, col) coordinates to explode
            
        Returns:
            List of explosion events for animation purposes
        """
        explosion_queue: List[Tuple[int, int]] = []
        explosion_queue.append(initial_explosion)
        explosion_events = []
        chain_length = 0
        
        while len(explosion_queue) > 0:
            self._check_game_over()
            if self.state.game_over:
                break
                
            chain_length += 1
            row, col = explosion_queue.pop(0)
            
            # Process explosion
            cell = self.state.get_cell(row, col)
            if cell and cell.orb_count >= cell.critical_mass:
                
                # Get neighbors that will receive orbs
                neighbors = cell._get_neighbors()
                have_exploded = cell.explode()
                
                # Record explosion event
                explosion_event = {
                    'position': (row, col),
                    'chain_number': chain_length,
                    'affected_neighbors': neighbors,
                    'exploded': have_exploded
                }
                explosion_events.append(explosion_event)
                
                # Distribute orbs to neighbors
                if have_exploded:
                    for neighbor_row, neighbor_col in neighbors:
                        neighbor_cell = self.state.get_cell(neighbor_row, neighbor_col)
                        if neighbor_cell:
                            # Update player cell counts if ownership changes
                            if neighbor_cell.player is not None and neighbor_cell.player != self.state.current_player:
                                self.state.player_cells[neighbor_cell.player] -= neighbor_cell.orb_count
                                self.state.player_cells[self.state.current_player] += neighbor_cell.orb_count
                            
                            neighbor_cell.player = self.state.current_player
                            neighbor_cell.add_orb(self.state.current_player)
                            
                            # If neighbor will explode, add to next round
                            if neighbor_cell.orb_count >= neighbor_cell.critical_mass:
                                explosion_queue.append((neighbor_row, neighbor_col))
        
        self.state.explosion_chain_length = chain_length
        return explosion_events
    
    def _switch_player(self):
        """Switch to the next player"""
        self.state.current_player = 2 if self.state.current_player == 1 else 1
    
    def _check_game_over(self):
        """Check if the game is over and determine winner"""
        if self.state.total_moves < 2:  # Game can't end in first move
            return
        
        player1_cells = self.state.player_cells[1]
        player2_cells = self.state.player_cells[2]
                
        # Determine if game is over
        if player1_cells == 0 and player2_cells > 0:
            self.state.game_over = True
            self.state.winner = 2
        elif player2_cells == 0 and player1_cells > 0:
            self.state.game_over = True
            self.state.winner = 1
    
    def get_game_state(self) -> GameState:
        """Get the current game state"""
        return self.state
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.state.reset_game()
    
    def get_cell_from_mouse_pos(self, mouse_pos: Tuple[int, int], 
                               grid_x: int, grid_y: int, cell_size: int) -> Optional[Cell]:
        """
        Convert mouse position to cell coordinates.
        This is a utility method but kept here for convenience.
        """
        x, y = mouse_pos
        
        # Check if click is within grid bounds
        if x < grid_x or y < grid_y:
            return None
            
        # Calculate grid position
        col = (x - grid_x) // cell_size
        row = (y - grid_y) // cell_size
        
        return self.state.get_cell(row, col)
