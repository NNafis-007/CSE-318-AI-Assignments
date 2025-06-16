#!/usr/bin/env python3
"""
Human vs AI Chain Reaction game with file-based communication.
All game states are saved to and can be loaded from gamestate.txt.
"""

import Board
import colors
import utils
import minmax
from gamestate_manager import GameStateManager

class HumanVsAIGame:
    def __init__(self, human_color=colors.RED, ai_difficulty=3, ai_heuristic='basic'):
        self.board = Board.Board()
        self.human_color = human_color
        self.ai_color = colors.BLUE if human_color == colors.RED else colors.RED
        self.ai_difficulty = ai_difficulty
        self.ai_heuristic = ai_heuristic
        self.current_player = colors.RED  # Red always starts
        self.game_over = False
        self.move_count = 0
        self.gsm = GameStateManager()
        
        # Map heuristic names to functions
        self.heuristic_map = {
            'basic': utils.heuristic,
            'orb_count': utils.heuristic_orb_count_diff,
            'edge_corner': utils.heuristic_edge_corner_control,
            'vulnerability': utils.heuristic_vulnerability,
            'chain_reaction': utils.heuristic_chain_reaction_opportunity
        }
        
        # Save initial empty board state
        self.gsm.save_game_state(self.board, self.current_player, "Game Start")
    
    def print_board(self):
        """Print the current board state."""
        print("\nCurrent Board:")
        print("   ", end="")
        for j in range(6):
            print(f"{j:3}", end="")
        print()
        
        for i in range(9):
            print(f"{i}: ", end="")
            for j in range(6):
                cell = self.board.grid[i][j]
                if cell.orb_count == 0:
                    print("[ ]", end=" ")
                else:
                    player_char = "R" if cell.player == 1 else "B"
                    print(f"[{cell.orb_count}{player_char}]", end=" ")
            print()
        print()
    
    def is_human_turn(self):
        return self.current_player == self.human_color
    
    def get_human_move(self):
        """Get a move from the human player."""
        valid_moves_list = utils.valid_moves(self.board, self.human_color)
        
        while True:
            try:
                print(f"\nYour turn ({'Red' if self.human_color == colors.RED else 'Blue'})!")
                move_input = input("Enter your move (row col) or 'quit' to exit: ").strip()
                
                if move_input.lower() == 'quit':
                    return None
                    
                row, col = map(int, move_input.split())
                
                if (row, col) in valid_moves_list:
                    return (row, col)
                else:
                    print("Invalid move! You can only place orbs in empty cells or your own cells.")
                    
            except (ValueError, IndexError):
                print("Invalid input format! Use 'row col' (e.g., '3 2')")
    
    def get_ai_move(self):
        """Get a move from the AI player using minimax."""
        print(f"\nAI ({'Red' if self.ai_color == colors.RED else 'Blue'}) is thinking...")
        
        heuristic_func = self.heuristic_map.get(self.ai_heuristic, utils.heuristic)
        best_move = utils.get_best_move(self.board, self.ai_color, 
                                      depth=self.ai_difficulty, 
                                      heuristic_func=heuristic_func)
        
        print(f"AI chooses: {best_move}")
        return best_move
    
    def make_move(self, row, col):
        """Make a move and update the game state file."""
        try:
            # Make the move
            self.board.make_move(self.current_player, row, col)
            self.move_count += 1
            
            # Save game state to file
            move_type = "Human Move" if self.is_human_turn() else "AI Move"
            self.gsm.save_game_state(self.board, self.current_player, move_type)
            
            print(f"Move made: ({row}, {col}) - Saved to gamestate.txt")
            
            # Check for game over
            if self.board.is_terminal() and self.move_count > 0:
                self.game_over = True
                return True
            
            # Switch players
            self.current_player = colors.BLUE if self.current_player == colors.RED else colors.RED
            return True
            
        except Exception as e:
            print(f"Error making move: {e}")
            return False
    
    def get_winner(self):
        """Get the winner of the game."""
        if not self.game_over:
            return None
        
        winner_value = utils.who_won(self.board)
        if winner_value > 0:
            return "Red"
        elif winner_value < 0:
            return "Blue"
        else:
            return "Draw"
    
    def load_game_from_file(self):
        """Load game state from gamestate.txt."""
        move_type, success = self.gsm.load_game_state(self.board)
        if success:
            print(f"Game state loaded from file. Last move: {move_type}")
            # Determine current player based on last move
            if move_type == "Human":
                self.current_player = self.ai_color
            else:
                self.current_player = self.human_color
            return True
        return False
    
    def play(self):
        """Main game loop."""
        print("=== Chain Reaction: Human vs AI ===")
        print("All moves are saved to gamestate.txt")
        print()
        
        while not self.game_over:
            self.print_board()
            
            # Get move
            if self.is_human_turn():
                move = self.get_human_move()
                if move is None:  # Player quit
                    print("Game ended by player.")
                    break
            else:
                move = self.get_ai_move()
                if move is None:  # AI couldn't find a move
                    print("AI couldn't make a move!")
                    break
            
            # Make the move
            row, col = move
            if not self.make_move(row, col):
                continue
        
        # Game over
        if self.game_over:
            self.print_board()
            winner = self.get_winner()
            print(f"Game Over! Winner: {winner}")
            
            # Save final state
            self.gsm.save_game_state(self.board, self.current_player, f"Game Over - {winner} wins")
        
        print("Game state has been saved to gamestate.txt")

def main():
    print("=== Chain Reaction: Human vs AI with File Communication ===")
    print()
    
    # Check if user wants to load existing game
    load_choice = input("Load existing game from gamestate.txt? (y/n): ").strip().lower()
    
    if load_choice == 'y':
        # Try to load existing game
        gsm = GameStateManager()
        temp_board = Board.Board()
        move_type, success = gsm.load_game_state(temp_board)
        
        if success:
            print("Existing game loaded!")
            temp_board.print_board()
            
            # Continue with loaded game setup
            print("Choose your color for the loaded game:")
            print("1. Red")
            print("2. Blue")
            choice = input("Enter your choice (1 or 2): ").strip()
            human_color = colors.RED if choice == "1" else colors.BLUE
            
            print("\nChoose AI difficulty:")
            print("1. Easy (depth 2)")
            print("2. Medium (depth 3)")
            print("3. Hard (depth 4)")
            diff_choice = input("Enter difficulty (1-3): ").strip()
            difficulty_map = {"1": 2, "2": 3, "3": 4}
            ai_difficulty = difficulty_map.get(diff_choice, 3)
            
            print("\nChoose AI heuristic:")
            print("1. Basic")
            print("2. Orb Count Difference")
            print("3. Edge/Corner Control")
            print("4. Vulnerability Analysis")
            print("5. Chain Reaction Opportunity")
            heur_choice = input("Enter heuristic (1-5): ").strip()
            heuristic_map = {
                "1": "basic",
                "2": "orb_count", 
                "3": "edge_corner",
                "4": "vulnerability",
                "5": "chain_reaction"
            }
            ai_heuristic = heuristic_map.get(heur_choice, "basic")
            
            # Create game and load state
            game = HumanVsAIGame(human_color, ai_difficulty, ai_heuristic)
            game.load_game_from_file()
            game.play()
        else:
            print("Could not load existing game. Starting new game...")
            load_choice = 'n'
    
    if load_choice != 'y':
        # Start new game
        print("Choose your color:")
        print("1. Red (you go first)")
        print("2. Blue (AI goes first)")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        human_color = colors.RED if choice == "1" else colors.BLUE
        
        print("\nChoose AI difficulty:")
        print("1. Easy (depth 2)")
        print("2. Medium (depth 3)")
        print("3. Hard (depth 4)")
        
        diff_choice = input("Enter difficulty (1-3): ").strip()
        difficulty_map = {"1": 2, "2": 3, "3": 4}
        ai_difficulty = difficulty_map.get(diff_choice, 3)
        
        print("\nChoose AI heuristic:")
        print("1. Basic")
        print("2. Orb Count Difference")
        print("3. Edge/Corner Control")
        print("4. Vulnerability Analysis")
        print("5. Chain Reaction Opportunity")
        
        heur_choice = input("Enter heuristic (1-5): ").strip()
        heuristic_map = {
            "1": "basic",
            "2": "orb_count", 
            "3": "edge_corner",
            "4": "vulnerability",
            "5": "chain_reaction"
        }
        ai_heuristic = heuristic_map.get(heur_choice, "basic")
        
        # Create and start game
        game = HumanVsAIGame(human_color, ai_difficulty, ai_heuristic)
        
        print(f"\nGame started! You are {'Red' if human_color == colors.RED else 'Blue'}")
        print("All game states will be saved to gamestate.txt")
        print("Enter moves as: row col (e.g., '3 2')")
        
        game.play()
    
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
