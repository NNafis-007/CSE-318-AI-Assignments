from typing import Optional, List, Tuple
from src.config.config import GRID_ROWS, GRID_COLS


class Cell:
    """
    Represents a single cell in the Chain Reaction game board.
    Handles orb placement, critical mass calculation, and explosion logic.
    """
    
    def __init__(self, row: int, col: int):
        """
        Initialize a cell with its position.
        
        Args:
            row: Row position of the cell
            col: Column position of the cell  
        """
        self.row = row
        self.col = col
        
        # Game state
        self.orb_count = 0              # Number of orbs in this cell
        self.player = None               # Player who owns this cell (1 or 2)
        self.is_exploding = False       # Whether cell is currently exploding
        
        # Calculate critical mass based on position
        self.critical_mass = self._calculate_critical_mass()
    
    def _calculate_critical_mass(self) -> int:
        """
        Calculate the critical mass for this cell based on its position.
        
        Returns:
            int: Critical mass (2 for corners, 3 for edges, 4 for center)
        """
        # Corner cells (2 neighbor)
        if ((self.row == 0 or self.row == GRID_ROWS - 1) and 
            (self.col == 0 or self.col == GRID_COLS - 1)):
            return 2
        
        # Edge cells (3 neighbors)
        elif (self.row == 0 or self.row == GRID_ROWS - 1 or 
              self.col == 0 or self.col == GRID_COLS - 1):
            return 3
        
        # Center cells (4 neighbors in Chain Reaction - only 4 directions)
        else:
            return 4
    
    def add_orb(self, player: int) -> bool:
        """
        Add an orb to this cell for the specified player.
        
        Args:
            player: Player number (1 or 2)
            
        Returns:
            bool: True if can add orb, False otherwise
        """
        # If cell is empty or owned by the same player
        if self.player is None or self.player == player:
            self.player = player
            self.orb_count += 1
            
            # Check if cell reaches critical mass
            if self.orb_count >= self.critical_mass:
                self.is_exploding = True
            return True
        
        else:
            print(f"Cannot add orb for player {self.player}: in cell ({self.row}, {self.col})")

        # Cannot add orb to opponent's cell
        return False
    
    def can_place_orb(self, player: int) -> bool:
        """
        Check if a player can place an orb in this cell.
        
        Args:
            player: Player number to check
            
        Returns:
            bool: True if player can place orb, False otherwise
        """
        return self.player is None or self.player == player
    
    def explode(self) -> List[Tuple[int, int]]:
        """
        Explode this cell and return coordinates of neighboring cells.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) coordinates of neighbors
        """
        if self.orb_count < self.critical_mass:
            print(f"Cell ({self.row}, {self.col}) cannot explode: not enough orbs")
            return []
        
        # Mark as exploding
        self.is_exploding = True
        
        # Calculate orbs to distribute (all current orbs)
        orbs_to_distribute = self.orb_count
        
        # Reset this cell
        self.orb_count = 0
        self.player = None
        
        # Get valid neighbors
        neighbors = self._get_neighbors()
        
        # Each neighbor gets 1 orb
        return neighbors[:orbs_to_distribute]
    
    def _get_neighbors(self) -> List[Tuple[int, int]]:
        """
        Get coordinates of all valid neighboring cells.
        
        Returns:
            List[Tuple[int, int]]: List of valid neighbor coordinates
        """
        neighbors = []
        
        # Check all 4 directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            
            # Check if neighbor is within board bounds
            if (0 <= new_row < GRID_ROWS and 
                0 <= new_col < GRID_COLS):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def reset_explosion_state(self):
        """Reset the explosion state of this cell."""
        self.is_exploding = False
    
    def is_empty(self) -> bool:
        """Check if the cell is empty."""
        return self.orb_count == 0
    
    def get_display_info(self) -> dict:
        """
        Get information needed for UI display.
        
        Returns:
            dict: Display information including orb count, player, state
        """
        return {
            'orb_count': self.orb_count,
            'player': self.player,
            'critical_mass': self.critical_mass,
            'is_exploding': self.is_exploding,
            'can_explode': self.orb_count >= self.critical_mass
        }
    
    def __str__(self) -> str:
        """String representation for debugging."""
        if self.is_empty():
            return f"Cell({self.row},{self.col}): Empty"
        return f"Cell({self.row},{self.col}): {self.orb_count} orbs, Player {self.player}"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return (f"Cell(row={self.row}, col={self.col}, "
                f"orbs={self.orb_count}, player={self.player}, "
                f"critical_mass={self.critical_mass})")