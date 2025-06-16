"""
Game State Manager for file-based communication in Chain Reaction.
Handles saving and loading game state to/from gamestate.txt.
"""

import Board
import colors

class GameStateManager:
    def __init__(self, filename="gamestate.txt"):
        self.filename = filename
    
    def save_game_state(self, board, current_player, move_type="Human Move"):
        """
        Save the current game state to file in the specified format.
        
        Args:
            board: The game board
            current_player: Current player (colors.RED or colors.BLUE)
            move_type: Type of move ("Human Move" or "AI Move")
        """
        with open(self.filename, 'w') as f:
            # Header line
            f.write(f"{move_type}:\n")
            
            # Board state: Nine rows of six cells each
            for i in range(9):
                row_data = []
                for j in range(6):
                    cell = board.grid[i][j]
                    if cell.orb_count == 0:
                        row_data.append("0")
                    else:
                        color_char = "R" if cell.player == 1 else "B"
                        row_data.append(f"{cell.orb_count}{color_char}")
                f.write(" ".join(row_data) + "\n")
    
    def load_game_state(self, board):
        """
        Load game state from file.
        
        Args:
            board: The board to load state into
            
        Returns:
            tuple: (move_type, success) where move_type is "Human" or "AI"
        """
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                
                if len(lines) < 10:
                    return None, False
                
                # Parse header
                header = lines[0].strip()
                move_type = "Human" if "Human Move" in header else "AI"
                
                # Parse board state
                for i in range(9):
                    row_line = lines[i + 1].strip()
                    cells = row_line.split()
                    
                    for j in range(6):
                        if j < len(cells):
                            cell_data = cells[j]
                            if cell_data == "0":
                                board.grid[i][j].player = None
                                board.grid[i][j].orb_count = 0
                            else:
                                count = int(cell_data[:-1])
                                player = 1 if cell_data[-1] == "R" else 2
                                board.grid[i][j].player = player
                                board.grid[i][j].orb_count = count
                
                return move_type, True
        except FileNotFoundError:
            return None, False
        except Exception as e:
            print(f"Error loading game state: {e}")
            return None, False
    
    def get_last_move_type(self):
        """Get the type of the last move from file."""
        try:
            with open(self.filename, 'r') as f:
                header = f.readline().strip()
                return "Human" if "Human Move" in header else "AI"
        except FileNotFoundError:
            return None

def test_gamestate_manager():
    """Test the GameStateManager functionality."""
    print("Testing GameStateManager...")
    
    # Create a test board
    board = Board.Board()
    board.make_move(colors.RED, 0, 0)  # Red places orb at (0,0)
    board.make_move(colors.BLUE, 1, 1)  # Blue places orb at (1,1)
    
    # Save state
    gsm = GameStateManager()
    gsm.save_game_state(board, colors.RED, "Human Move")
    print("Game state saved to gamestate.txt")
    
    # Load state into new board
    new_board = Board.Board()
    move_type, success = gsm.load_game_state(new_board)
    
    if success:
        print(f"Game state loaded successfully. Last move type: {move_type}")
        print("Original board:")
        board.print_board()
        print("Loaded board:")
        new_board.print_board()
    else:
        print("Failed to load game state")

if __name__ == "__main__":
    test_gamestate_manager()
