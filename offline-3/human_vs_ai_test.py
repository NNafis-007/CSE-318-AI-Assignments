#!/usr/bin/env python3
"""
Simple console-based Human vs AI game for testing the minimax implementation.
"""

import Board
import colors
import utils
import minmax

def print_board(board):
    """Print the current board state in a readable format."""
    print("\nCurrent Board:")
    print("   ", end="")
    for j in range(6):
        print(f"{j:3}", end="")
    print()
    
    for i in range(9):
        print(f"{i}: ", end="")
        for j in range(6):
            cell = board.grid[i][j]
            if cell.orb_count == 0:
                print("[ ]", end=" ")
            else:
                player_char = "R" if cell.player == 1 else "B"
                print(f"[{cell.orb_count}{player_char}]", end=" ")
        print()
    print()

def get_human_move(board, player):
    """Get a move from the human player."""
    valid_moves_list = utils.valid_moves(board, player)
    
    while True:
        try:
            print(f"\nYour turn ({'Red' if player == colors.RED else 'Blue'})!")
            move_input = input("Enter your move (row col) or 'quit' to exit: ").strip()
            
            if move_input.lower() == 'quit':
                return None
                
            row, col = map(int, move_input.split())
            
            if (row, col) in valid_moves_list:
                return (row, col)
            else:
                print("Invalid move! You can only place orbs in empty cells or your own cells.")
                print(f"Valid moves: {valid_moves_list[:10]}...")  # Show first 10 for brevity
                
        except (ValueError, IndexError):
            print("Invalid input format! Use 'row col' (e.g., '3 2')")

def get_ai_move(board, player, difficulty=3):
    """Get a move from the AI player."""
    print(f"\nAI ({'Red' if player == colors.RED else 'Blue'}) is thinking...")
    best_move = utils.get_best_move(board, player, depth=difficulty)
    print(f"AI chooses: {best_move}")
    return best_move

def play_game():
    """Main game loop for Human vs AI."""
    print("=== Chain Reaction: Human vs AI ===")
    print("Choose your color:")
    print("1. Red (you go first)")
    print("2. Blue (AI goes first)")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    human_color = colors.RED if choice == "1" else colors.BLUE
    ai_color = colors.BLUE if human_color == colors.RED else colors.RED
    
    print("\nChoose AI difficulty:")
    print("1. Easy (depth 2)")
    print("2. Medium (depth 3)")
    print("3. Hard (depth 4)")
    
    diff_choice = input("Enter difficulty (1-3): ").strip()
    difficulty_map = {"1": 2, "2": 3, "3": 4}
    ai_difficulty = difficulty_map.get(diff_choice, 3)
    
    # Initialize game
    board = Board.Board()
    current_player = colors.RED  # Red always starts
    game_over = False
    move_count = 0
    
    print(f"\nGame started! You are {'Red' if human_color == colors.RED else 'Blue'}")
    print("Enter moves as: row col (e.g., '3 2')")
    
    while not game_over:
        print_board(board)
        
        # Check for game over
        if board.is_terminal() and move_count > 0:
            winner = utils.who_won(board)
            if winner > 0:
                winner_name = "Red"
            elif winner < 0:
                winner_name = "Blue"
            else:
                winner_name = "Draw"
            
            print(f"Game Over! Winner: {winner_name}")
            break
        
        # Get move
        if current_player == human_color:
            move = get_human_move(board, current_player)
            if move is None:  # Player quit
                print("Game ended by player.")
                break
        else:
            move = get_ai_move(board, current_player, ai_difficulty)
            if move is None:  # AI couldn't find a move
                print("AI couldn't make a move!")
                break
        
        # Make the move
        row, col = move
        try:
            board.make_move(current_player, row, col)
            move_count += 1
            print(f"Move made: ({row}, {col})")
        except Exception as e:
            print(f"Error making move: {e}")
            continue
        
        # Switch players
        current_player = colors.BLUE if current_player == colors.RED else colors.RED
    
    print("Thanks for playing!")

if __name__ == "__main__":
    play_game()
