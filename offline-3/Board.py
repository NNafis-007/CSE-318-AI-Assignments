"""
Board class for Chain Reaction game.
Compatible with the existing Cell structure in src/core/cell.py
"""

class SimpleCell:
    """Simple cell class for AI compatibility"""
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.player = None
        self.orb_count = 0
        self.critical_mass = self._calculate_critical_mass()
    
    def _calculate_critical_mass(self):
        """Calculate critical mass based on position"""
        # Corner cells (2 neighbors)
        if ((self.row == 0 or self.row == 8) and 
            (self.col == 0 or self.col == 5)):
            return 2
        # Edge cells (3 neighbors)
        elif (self.row == 0 or self.row == 8 or 
              self.col == 0 or self.col == 5):
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

class Board:
    """
    Represents the game board for Chain Reaction.
    """
    
    def __init__(self):
        """Initialize the board with empty cells."""
        self.grid = [[SimpleCell(i, j) for j in range(6)] for i in range(9)]
        self.rows = 9
        self.cols = 6
    
    def make_move(self, player, row, col, logged=None, undo_info=None):
        """
        Make a move on the board with optional undo information.
        
        Args:
            player: Player making the move (1 or 2)
            row: Row to place orb
            col: Column to place orb
            logged: 2D array to track visited cells during explosion
            undo_info: List to store undo information
        """
        if logged is None:
            logged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        if undo_info is None:
            undo_info = []
        
        # Store undo information
        if undo_info is not None:
            undo_info.append([row, col, self.grid[row][col].player, self.grid[row][col].orb_count])
        
        # Add orb to the cell
        self.grid[row][col].add_orb(player)
        
        # Check if explosion is needed
        if self.grid[row][col].orb_count >= self.grid[row][col].critical_mass:
            self._explode_cell(row, col, player, logged, undo_info)
    
    def _explode_cell(self, row, col, player, logged, undo_info):
        """Handle cell explosion and chain reactions."""
        if logged[row][col]:
            return
            
        logged[row][col] = True
        cell = self.grid[row][col]
        
        # Store current state for undo
        if undo_info is not None:
            undo_info.append([row, col, cell.player, cell.orb_count])
        
        # Calculate orbs to distribute
        orbs_to_distribute = cell.orb_count
        cell.orb_count = 0
        cell.player = None
        
        # Get neighbor directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Distribute orbs to neighbors
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                # Store neighbor state for undo
                neighbor = self.grid[new_row][new_col]
                if undo_info is not None:
                    undo_info.append([new_row, new_col, neighbor.player, neighbor.orb_count])
                
                # Add orb to neighbor
                neighbor.add_orb(player)
                
                # Check for chain reaction
                if neighbor.orb_count >= neighbor.critical_mass:
                    self._explode_cell(new_row, new_col, player, logged, undo_info)
    
    def get_critical_mass(self, row, col):
        """Get the critical mass for a cell at given position."""
        return self.grid[row][col].critical_mass
    
    def is_terminal(self):
        """
        Check if the game is in a terminal state.
        Game ends when only one player has orbs on the board.
        """
        players_with_orbs = set()
        
        for row in self.grid:
            for cell in row:
                if cell.orb_count > 0 and cell.player is not None:
                    players_with_orbs.add(cell.player)
        
        # Game is terminal if 0 or 1 player has orbs (and at least one move was made)
        return len(players_with_orbs) <= 1 and any(
            cell.orb_count > 0 for row in self.grid for cell in row
        )
    
    def print_board(self):
        """Print the current board state for debugging."""
        print("Current Board:")
        print("   ", end="")
        for j in range(self.cols):
            print(f"{j:3}", end="")
        print()
        
        for i in range(self.rows):
            print(f"{i}: ", end="")
            for j in range(self.cols):
                cell = self.grid[i][j]
                if cell.orb_count == 0:
                    print("[ ]", end=" ")
                else:
                    player_char = "R" if cell.player == 1 else "B"
                    print(f"[{cell.orb_count}{player_char}]", end=" ")
            print()
        print()
