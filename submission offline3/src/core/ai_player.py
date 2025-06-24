import sys
import os
import time
import threading

# Add root directory to path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import minmax
import utils
import colors
import random
from src.config.config import TIME_LIMIT

class AIPlayer:
    def __init__(self, color, difficulty=3, heuristic_name='weighted_combined'):
        self.color = color
        self.difficulty = difficulty  # depth for minimax
        self.heuristic_function = self._get_heuristic_function(heuristic_name)
        self.time_limit = TIME_LIMIT
        self.start_time = None
        self.time_up = False
    
    def _get_heuristic_function(self, heuristic_name):
        heuristic_map = {
            'weighted_combined': utils.heuristic_weighted_combined,
            'orb_count': utils.heuristic_orb_count_diff,
            'edge_corner': utils.heuristic_edge_corner_control,
            'strategic': utils.heuristic_strategic_evaluation,
            'chain_reaction': utils.heuristic_chain_reaction_opportunity
        }
        return heuristic_map.get(heuristic_name, utils.heuristic_weighted_combined)
    
    def is_time_up(self):
        """Check if the time limit has been exceeded"""
        if self.start_time is None:
            return False
        return time.time() - self.start_time >= self.time_limit
    
    def get_best_move(self, board):
        """Get the best move for the AI using minimax algorithm with time limit"""
        print(f"AI Player ({colors.get_color_name(self.color)}) is thinking...")
        
        # Start timing
        self.start_time = time.time()
        
        valid_moves_list = utils.valid_moves(board, self.color)
        
        if not valid_moves_list:
            return None
        
        if len(valid_moves_list) == 1:
            elapsed_time = time.time() - self.start_time
            print(f"AI found only one valid move in {elapsed_time:.3f} seconds")
            return valid_moves_list[0]
        
        best_move = None
        best_value = float('-inf') if self.color == colors.RED else float('inf')
        moves_evaluated = 0
        
        # Try iterative deepening with time limit
        max_depth = self.difficulty
        for current_depth in range(1, max_depth + 1):
            if self.is_time_up():
                print(f"Time limit reached at depth {current_depth - 1}")
                break
                
            depth_best_move = None
            depth_best_value = float('-inf') if self.color == colors.RED else float('inf')
            
            for move in valid_moves_list:
                if self.is_time_up():
                    print(f"Time limit reached while evaluating moves at depth {current_depth}")
                    break
                    
                # Make the move and evaluate
                undo_info = utils.make_move_with_undo_information(board, move, self.color)
                
                # Evaluate this move using minimax with time check
                if self.color == colors.RED:
                    value = minmax.minmax(board, current_depth - 1, float('-inf'), float('inf'), 
                                        colors.BLUE, self.heuristic_function, self)
                else:
                    value = minmax.minmax(board, current_depth - 1, float('-inf'), float('inf'), 
                                        colors.RED, self.heuristic_function, self)
                
                # Undo the move
                utils.undo_move(board, undo_info)
                moves_evaluated += 1
                
                # Update best move for this depth
                if self.color == colors.RED:
                    if value > depth_best_value:
                        depth_best_value = value
                        depth_best_move = move
                else:
                    if value < depth_best_value:
                        depth_best_value = value
                        depth_best_move = move
                
                # Check time limit
                if self.is_time_up():
                    break
            
            # If we completed this depth, update the overall best move
            if depth_best_move is not None and not self.is_time_up():
                best_move = depth_best_move
                best_value = depth_best_value
                print(f"Completed depth {current_depth}, best value: {best_value:.3f}")
        
        # Calculate elapsed time and report
        elapsed_time = time.time() - self.start_time
        print(f"AI ({colors.get_color_name(self.color)}) move completed in {elapsed_time:.3f} seconds")
        print(f"Evaluated {moves_evaluated} moves, final depth reached: {current_depth if not self.is_time_up() else current_depth - 1}")
        
        # If no move was found (shouldn't happen), return the first valid move
        if best_move is None:
            print("Warning: No best move found, using first valid move")
            best_move = valid_moves_list[0]
        
        return best_move