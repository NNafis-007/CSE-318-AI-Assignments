"""
Simple test for Human vs AI functionality
"""
import Board
import colors
import utils

def test_basic_functionality():
    """Test basic board operations and AI move generation."""
    print("Testing basic functionality...")
    
    # Create a new board
    board = Board.Board()
    
    # Make a few moves
    print("Making initial moves...")
    board.make_move(colors.RED, 4, 2)  # Center
    board.make_move(colors.BLUE, 0, 0)  # Corner
    board.make_move(colors.RED, 4, 3)  # Next to center
    
    # Print board
    board.print_board()
    
    # Test valid moves
    red_moves = utils.valid_moves(board, colors.RED)
    blue_moves = utils.valid_moves(board, colors.BLUE)
    print(f"Red valid moves: {len(red_moves)}")
    print(f"Blue valid moves: {len(blue_moves)}")
    
    # Test AI move generation
    print("\nTesting AI move generation...")
    ai_move = utils.get_best_move(board, colors.BLUE, depth=2)
    print(f"AI suggests move: {ai_move}")
    
    # Test different heuristics
    print("\nTesting heuristics...")
    h1 = utils.heuristic(board, colors.RED)
    h2 = utils.heuristic_orb_count_diff(board, colors.RED)
    h3 = utils.heuristic_edge_corner_control(board, colors.RED)
    
    print(f"Basic heuristic (RED): {h1}")
    print(f"Orb count diff (RED): {h2}")
    print(f"Edge/corner control (RED): {h3}")
    
    print("Test completed successfully!")

def interactive_test():
    """Interactive test where human can play against AI."""
    print("\n=== Interactive Human vs AI Test ===")
    print("You are RED, AI is BLUE")
    print("Enter moves as 'row col' (e.g., '4 2')")
    print("Enter 'quit' to exit")
    
    board = Board.Board()
    current_player = colors.RED
    
    while not board.is_terminal():
        board.print_board()
        
        if current_player == colors.RED:
            # Human turn
            try:
                move_input = input("Your move (row col): ").strip()
                if move_input.lower() == 'quit':
                    break
                
                row, col = map(int, move_input.split())
                valid_moves_list = utils.valid_moves(board, colors.RED)
                
                if (row, col) in valid_moves_list:
                    board.make_move(colors.RED, row, col)
                    current_player = colors.BLUE
                else:
                    print("Invalid move! Try again.")
            except (ValueError, IndexError):
                print("Invalid input! Use format 'row col'")
        
        else:
            # AI turn
            print("AI is thinking...")
            ai_move = utils.get_best_move(board, colors.BLUE, depth=3)
            
            if ai_move:
                row, col = ai_move
                board.make_move(colors.BLUE, row, col)
                print(f"AI played: {row} {col}")
                current_player = colors.RED
            else:
                print("AI has no valid moves!")
                break
    
    # Game over
    board.print_board()
    winner = utils.who_won(board)
    if winner > 0:
        print("You won!")
    elif winner < 0:
        print("AI won!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    test_basic_functionality()
    
    play_interactive = input("\nWould you like to play against the AI? (y/n): ").strip().lower()
    if play_interactive == 'y':
        interactive_test()
