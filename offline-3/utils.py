import copy
import Board
import colors

def custom_copy(state:Board.Board):
    b = Board.Board()
    for i in range(9):
        for j in range(6):
            b.grid[i][j].player = state.grid[i][j].player
            b.grid[i][j].orb_count = state.grid[i][j].orb_count
    return b 
def make_move_with_undo_information(state:Board.Board,valid_moves:list[int],maximizing_player):
    logged = [[False for _ in range(6)] for _ in range(9)]
    undo_info = []
    i,j = valid_moves
    state.make_move(maximizing_player,i,j,logged,undo_info)
    return undo_info


def undo_move(state:Board.Board,undo_info:list[list[int]]):
    for info in undo_info:
        i,j,player,count = info 
        state.grid[i][j].player = player
        state.grid[i][j].orb_count = count
    
def result_board(state:Board.Board,valid_moves:list[int],maximizing_player):
    deep_copied_board = custom_copy(state)
    i,j = valid_moves
    deep_copied_board.make_move(maximizing_player,i,j)
    #deep_copied_board.print_board()
    #print()
    #print()
    return deep_copied_board

def heuristic(state:Board.Board,player):
    count = 0
    for row in state.grid:
        for cell in row:
            if cell.player == 1:  # RED player
                count += 1
            elif cell.player == 2:  # BLUE player
                count -= 1
    #print(f"heuristic: {count}")
    return count 

def heuristic_orb_count_diff(state:Board.Board,player):
    score = 0
    player_num = 1 if player == colors.RED else 2
    for row in state.grid:
        for cell in row:
            if cell.player == player_num:
                score += cell.orb_count
            elif cell.player is not None:
                score -= cell.orb_count
    
    if (player==colors.RED):
        return score
    
    return -score 

def heuristic_edge_corner_control(state:Board.Board,player):
    score = 0
    player_num = 1 if player == colors.RED else 2
    for i in range(9):
        for j in range(6):
            cell = state.grid[i][j]
            if cell.player == player_num:
                if (i in [0, 8]) and (j in [0, 5]):
                    score += 3  # corner
                elif i in [0, 8] or j in [0, 5]:
                    score += 2  # edge
                else:
                    score += 1  # center
    
    if (player==colors.RED):
        return score    
    return -score

def heuristic_vulnerability(state:Board.Board,player):
    penalty = 0
    player_num = 1 if player == colors.RED else 2
    for i in range(9):
        for j in range(6):
            cell = state.grid[i][j]
            if cell.player == player_num and cell.orb_count >= state.get_critical_mass(i, j) - 1:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < 9 and 0 <= nj < 6:
                        neighbor = state.grid[ni][nj]
                        if neighbor.player is not None and neighbor.player != player_num:
                            penalty -= 2
    if (player==colors.RED):
        return penalty
    
    return -penalty 

def heuristic_chain_reaction_opportunity(state:Board.Board,player):
    reward = 0
    player_num = 1 if player == colors.RED else 2
    for i in range(9):
        for j in range(6):
            cell = state.grid[i][j]
            if cell.player == player_num:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < 9 and 0 <= nj < 6:
                        neighbor = state.grid[ni][nj]
                        if neighbor.player is not None and neighbor.player != player_num:
                            if neighbor.orb_count == state.get_critical_mass(ni, nj) - 1:
                                reward += 3
    if (player==colors.RED):
        return reward
    
    return -reward 



def valid_moves(state:Board.Board,player):
    valid_moves = []
    player_num = 1 if player == colors.RED else 2
    for r in range(9):
        for c in range(6):
            cell = state.grid[r][c]
            if cell.player == player_num or cell.player is None:
                valid_moves.append((r, c))
    #print(f"valid moves:{valid_moves}")
    return valid_moves

#3:36 pm - 3:54 pm  
def who_won(state:Board.Board)->int:
    #print("reaching base case!")
    has_Red = False
    has_Blue = False
    for rows in state.grid:
        for cell in rows:
            if cell.player == 1:  # RED player
                has_Red = True
            elif cell.player == 2:  # BLUE player
                has_Blue=True
                if(has_Red==True and has_Blue==True):
                 #board filled but no one dominant color
                 print("draw!")
                 return 0
    if(has_Red==True):
        #red won, +INF
        #print("red won!")
        return int(1e9)
    #blue won, -INF
    elif has_Blue:
        #print("blue won!")
        return -int(1e9)
    #print("draw!")
    return 0


def get_best_move(state: Board.Board, player, depth=3, heuristic_func=heuristic):
    """
    Get the best move for the AI player using minimax algorithm.
    
    Args:
        state: Current board state
        player: Player color (colors.RED or colors.BLUE)
        depth: Search depth for minimax
        heuristic_func: Heuristic function to use for evaluation
    
    Returns:
        tuple: Best move as (row, col) or None if no valid moves
    """
    import minmax
    
    valid_moves_list = valid_moves(state, player)
    
    if not valid_moves_list:
        return None
    
    if len(valid_moves_list) == 1:
        return valid_moves_list[0]
    
    best_move = None
    best_value = float('-inf') if player == colors.RED else float('inf')
    
    for move in valid_moves_list:
        # Make the move and evaluate
        undo_info = make_move_with_undo_information(state, move, player)
        
        # Evaluate this move using minimax
        if player == colors.RED:
            value = minmax.minmax(state, depth - 1, float('-inf'), float('inf'), 
                                colors.BLUE, heuristic_func)
        else:
            value = minmax.minmax(state, depth - 1, float('-inf'), float('inf'), 
                                colors.RED, heuristic_func)
        
        # Undo the move
        undo_move(state, undo_info)
        
        # Update best move
        if player == colors.RED:
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move
    
    return best_move