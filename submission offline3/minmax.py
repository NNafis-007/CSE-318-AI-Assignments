import colors
from utils import *

def minmax(state, depth, alpha, beta, maximizing_player, f_heuristic, ai_player=None):
    """Minimax algorithm with alpha-beta pruning and optional time limit."""
    # Check time limit if ai_player is provided
    if ai_player is not None and ai_player.is_time_up():
        return f_heuristic(state, maximizing_player)
    
    if state.is_terminal():
        return who_won(state)
    if depth == 0:
        return f_heuristic(state, maximizing_player)
    
    if maximizing_player == colors.RED:
        max_eval = -int(1e9)
        valid_movess = valid_moves(state, maximizing_player)
        for action in valid_movess:
            # Check time limit before each move evaluation
            if ai_player is not None and ai_player.is_time_up():
                break
                
            undo_info = make_move_with_undo_information(state, action, maximizing_player)
            eval = minmax(state, depth - 1, alpha, beta, colors.BLUE, f_heuristic, ai_player)
            undo_move(state, undo_info)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = int(1e9)
        valid_movess = valid_moves(state, maximizing_player)
        for action in valid_movess:
            # Check time limit before each move evaluation
            if ai_player is not None and ai_player.is_time_up():
                break
                
            undo_info = make_move_with_undo_information(state, action, maximizing_player)
            eval = minmax(state, depth - 1, alpha, beta, colors.RED, f_heuristic, ai_player)
            undo_move(state, undo_info)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval