import sys
import os

# Add root directory to path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import minmax
import utils
import colors
import random

class AIPlayer:
    def __init__(self, color, difficulty=3, heuristic_name='basic'):
        self.color = color
        self.difficulty = difficulty  # depth for minimax
        self.heuristic_function = self._get_heuristic_function(heuristic_name)
    
    def _get_heuristic_function(self, heuristic_name):
        heuristic_map = {
            'basic': utils.heuristic,
            'orb_count': utils.heuristic_orb_count_diff,
            'edge_corner': utils.heuristic_edge_corner_control,
            'vulnerability': utils.heuristic_vulnerability,
            'chain_reaction': utils.heuristic_chain_reaction_opportunity
        }
        return heuristic_map.get(heuristic_name, utils.heuristic)
    
    def get_best_move(self, board):
        """Get the best move for the AI using minimax algorithm"""
        valid_moves_list = utils.valid_moves(board, self.color)
        
        if not valid_moves_list:
            return None
        
        if len(valid_moves_list) == 1:
            return valid_moves_list[0]
        
        best_move = None
        best_value = float('-inf') if self.color == colors.RED else float('inf')
        
        for move in valid_moves_list:
            # Make the move and evaluate
            undo_info = utils.make_move_with_undo_information(board, move, self.color)
            
            # Evaluate this move using minimax
            if self.color == colors.RED:
                value = minmax.minmax(board, self.difficulty - 1, float('-inf'), float('inf'), 
                                    colors.BLUE, self.heuristic_function)
            else:
                value = minmax.minmax(board, self.difficulty - 1, float('-inf'), float('inf'), 
                                    colors.RED, self.heuristic_function)
            
            # Undo the move
            utils.undo_move(board, undo_info)
            
            # Update best move
            if self.color == colors.RED:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
        
        return best_move