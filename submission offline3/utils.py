import copy
import Board
import colors

# Get grid configuration
try:
    from src.config.config import GRID_ROWS, GRID_COLS
except ImportError:
    GRID_ROWS, GRID_COLS = 9, 6

def custom_copy(state:Board.Board):
    b = Board.Board(state.rows, state.cols)
    for i in range(state.rows):
        for j in range(state.cols):
            b.grid[i][j].player = state.grid[i][j].player
            b.grid[i][j].orb_count = state.grid[i][j].orb_count
    return b 
def make_move_with_undo_information(state:Board.Board,valid_moves:list[int],maximizing_player):
    logged = [[False for _ in range(state.cols)] for _ in range(state.rows)]
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
    return deep_copied_board

def heuristic_weighted_combined(state: Board.Board, player):
    """
    Weighted combination heuristic:
    1 * edge_corner_control + 2 * strategic_evaluation
    """
    chain_reaction = heuristic_chain_reaction_opportunity(state, player)
    strategic_score = heuristic_strategic_evaluation(state, player)
    
    return 1 * chain_reaction + 2 * strategic_score

def heuristic_strategic_evaluation(state: Board.Board, player):
    """
    Strategic heuristic based on game state evaluation:
    - Win/loss: ±10000
    - Orb vulnerability to critical enemies: -5 + critical_mass
    - Safe orb bonuses: +2 (edge), +3 (corner), +2 (critical)
    - Orb count: +1 per orb
    - Critical block bonuses: +2 * block_size for contiguous critical blocks
    """
    player_num = 1 if player == colors.RED else 2
    enemy_num = 2 if player == colors.RED else 1
    
    # Check for terminal states
    terminal_result = who_won(state)
    if terminal_result != 0:
        if (player == colors.RED and terminal_result > 0) or (player == colors.BLUE and terminal_result < 0):
            return 10000  # Win
        else:
            return -10000  # Loss
    
    score = 0
    
    # Track visited cells for contiguous block detection
    visited = [[False for _ in range(state.cols)] for _ in range(state.rows)]
    
    for i in range(state.rows):
        for j in range(state.cols):
            cell = state.grid[i][j]
            
            # Only consider player's orbs
            if cell.player == player_num and cell.orb_count > 0:
                # Base score: +1 for each orb
                score += cell.orb_count
                
                # Check for critical enemy cells surrounding this orb
                critical_enemies = []
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < state.rows and 0 <= nj < state.cols:
                        neighbor = state.grid[ni][nj]
                        if (neighbor.player == enemy_num and 
                            neighbor.orb_count == state.get_critical_mass(ni, nj) - 1):
                            critical_enemies.append((ni, nj))
                
                if critical_enemies:
                    # Subtract penalty for each critical enemy
                    for enemy_pos in critical_enemies:
                        enemy_critical_mass = state.get_critical_mass(enemy_pos[0], enemy_pos[1])
                        score -= (5 - enemy_critical_mass)
                else:
                    # No critical enemies, add positional bonuses
                    is_corner = ((i == 0 or i == state.rows - 1) and 
                               (j == 0 or j == state.cols - 1))
                    is_edge = (i == 0 or i == state.rows - 1 or 
                              j == 0 or j == state.cols - 1)
                    is_critical = cell.orb_count == state.get_critical_mass(i, j) - 1
                    
                    if is_corner:
                        score += 3
                    elif is_edge:
                        score += 2
                    
                    if is_critical:
                        score += 2
    
    # Find contiguous blocks of critical cells
    for i in range(state.rows):
        for j in range(state.cols):
            cell = state.grid[i][j]
            if (not visited[i][j] and cell.player == player_num and 
                cell.orb_count == state.get_critical_mass(i, j) - 1):
                # Start a new block search
                block_size = _get_critical_block_size(state, i, j, player_num, visited)
                if block_size > 0:
                    score += 2 * block_size
    
    return score if player == colors.RED else -score

def _get_critical_block_size(state: Board.Board, start_i: int, start_j: int, player_num: int, visited: list) -> int:
    """
    Helper function to calculate the size of a contiguous block of critical cells.
    Uses DFS to find all connected critical cells of the same player.
    """
    if (start_i < 0 or start_i >= state.rows or start_j < 0 or start_j >= state.cols or
        visited[start_i][start_j]):
        return 0
    
    cell = state.grid[start_i][start_j]
    if (cell.player != player_num or 
        cell.orb_count != state.get_critical_mass(start_i, start_j) - 1):
        return 0
    
    visited[start_i][start_j] = True
    size = 1
    
    # Check all four directions
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = start_i + dx, start_j + dy
        size += _get_critical_block_size(state, ni, nj, player_num, visited)
    
    return size

def heuristic_chain_reaction_opportunity(state:Board.Board,player):
    reward = 0
    player_num = 1 if player == colors.RED else 2
    for i in range(state.rows):
        for j in range(state.cols):
            cell = state.grid[i][j]
            if cell.player == player_num:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < state.rows and 0 <= nj < state.cols:
                        neighbor = state.grid[ni][nj]
                        if neighbor.player is not None and neighbor.player != player_num:
                            if neighbor.orb_count == state.get_critical_mass(ni, nj) - 1:
                                reward += 3
    if (player==colors.RED):
        return reward
    
    return -reward 

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
    for i in range(state.rows):
        for j in range(state.cols):
            cell = state.grid[i][j]
            if cell.player == player_num:
                if (i in [0, state.rows - 1]) and (j in [0, state.cols - 1]):
                    score += 3  # corner
                elif i in [0, state.rows - 1] or j in [0, state.cols - 1]:
                    score += 2  # edge
                else:
                    score += 1  # center
    
    if (player==colors.RED):
        return score    
    return -score



def valid_moves(state:Board.Board,player):
    """Get all valid moves for a player."""
    valid_moves = []
    player_num = 1 if player == colors.RED else 2
    for r in range(state.rows):
        for c in range(state.cols):
            cell = state.grid[r][c]
            if cell.player == player_num or cell.player is None:
                valid_moves.append((r, c))
    return valid_moves

def who_won(state:Board.Board)->int:
    """Check who won the game. Returns 1e9 for red win, -1e9 for blue win, 0 for draw."""
    has_Red = False
    has_Blue = False
    for rows in state.grid:
        for cell in rows:
            if cell.player == 1:  # RED player
                has_Red = True
            elif cell.player == 2:  # BLUE player
                has_Blue = True
                if has_Red and has_Blue:
                    return 0  # Draw - both players have orbs
    
    if has_Red:
        return int(1e9)  # Red won
    elif has_Blue:
        return -int(1e9)  # Blue won
    return 0  # Draw


def get_best_move(state: Board.Board, player, depth=3, heuristic_func=heuristic_weighted_combined):
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