from itertools import chain
from shutil import move
from typing import Callable, List, Tuple, Dict, Optional
from enum import Enum
import time
import math
import random

class Player(Enum):
    EMPTY = "Empty"
    RED = "Red"
    BLUE = "Blue"

class GameMode(Enum):
    USER_VS_USER = 1
    USER_VS_AI = 2
    AI_VS_AI = 3

class AIType(Enum):
    SMART = "Smart AI (Minimax)"
    RANDOM = "Random AI"

class Cell:
    def __init__(self):
        self.orbs = 0
        self.player = Player.EMPTY
    
    # to print a cell easily
    def __str__(self):
        if self.player == Player.EMPTY:
            return "⚫"
        elif self.player == Player.RED:
            return f"🔴{self.orbs}" if self.orbs > 0 else "⚫"
        else:  # BLUE
            return f"🔵{self.orbs}" if self.orbs > 0 else "⚫"

# Game Class
class ChainReactionGame:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.current_player = Player.RED
        self.game_over = False
        self.winner = None
        self.move_count = 0
        self._initialize_critical_mass_cache() 
    
    def _initialize_critical_mass_cache(self):
        """Pre-calculate critical mass for each position"""
        self.critical_mass_cache = {}
        for row in range(self.rows):
            for col in range(self.cols):
                if (row == 0 or row == self.rows - 1) and (col == 0 or col == self.cols - 1):
                    neighbors = 2
                elif row == 0 or row == self.rows - 1 or col == 0 or col == self.cols - 1:
                    neighbors = 3
                else:
                    neighbors = 4
                # Store critical mass in cache
                self.critical_mass_cache[(row, col)] = neighbors
    
    def get_critical_mass(self, row: int, col: int) -> int:
        """Get critical mass for a position (number of neighbors)"""
        return self.critical_mass_cache.get((row, col), 0)
    
    def is_valid_move(self, row: int, col: int, player: Player) -> bool:
        """Check if a move is valid"""
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return False
         
        cell = self.board[row][col]
        return cell.player == Player.EMPTY or cell.player == player
    
    def get_valid_moves(self, player: Player) -> List[Tuple[int, int]]:
        """Get all valid moves for a player"""
        moves = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves
    
    def make_move(self, row: int, col: int, player: Player) -> bool:
        """Make a move and handle explosions"""
        if not self.is_valid_move(row, col, player) or self.game_over:
            return False

        self.board[row][col].orbs += 1
        self.board[row][col].player = player
        self.move_count += 1
        
        self._handle_explosions(row, col)
        self._check_win_condition()
        #switch player if game is not over
        if not self.game_over:
            self.current_player = Player.BLUE if self.current_player == Player.RED else Player.RED
        return True
    
    def _handle_explosions(self, row: int, col: int):
        """Handle chain explosions with game-over checking to prevent infinite loops"""        
        if self._is_game_over():
            return
        cell = self.board[row][col]
        if cell.orbs >= self.get_critical_mass(row, col):
            self._explode_cell(row, col)
        

    def _is_game_over(self) -> bool:
        """Check if game is over during explosion processing"""
        red_orbs = 0
        blue_orbs = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player == Player.RED:
                    red_orbs += cell.orbs
                elif cell.player == Player.BLUE:
                    blue_orbs += cell.orbs
        
        total_orbs = red_orbs + blue_orbs
        if total_orbs > 0 and self.move_count > 2:
            return (red_orbs == 0 and blue_orbs > 0) or (blue_orbs == 0 and red_orbs > 0)
        
        return False
    
    def _explode_cell(self, row: int, col: int):
        explosion_queue :List[Tuple[int,int]] = []
        explosion_queue.append((row, col))
        chain_len = 0

        while len(explosion_queue) > 0:
            if self._is_game_over():
                break
            chain_len += 1
            current_row, current_col = explosion_queue.pop(0)
            cell = self.board[current_row][current_col]
            critical_mass = self.get_critical_mass(current_row, current_col)
            exploding_player = cell.player

            if cell.orbs >= critical_mass:
                # Reset cell due to explosion
                cell.orbs = 0
                cell.player = Player.EMPTY
                
                neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dr, dc in neighbors:
                    nr, nc = current_row + dr, current_col + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbor_cell = self.board[nr][nc]
                        neighbor_cell.orbs += 1
                        neighbor_cell.player = exploding_player
                        if neighbor_cell.orbs >= self.get_critical_mass(nr, nc):
                            explosion_queue.append((nr, nc))


        # """Explode a single cell"""
        # cell = self.board[row][col]
        # exploding_player = cell.player
        # critical_mass = self.get_critical_mass(row, col)
        # orbs_to_distribute = critical_mass
        # cell.orbs -= orbs_to_distribute
        # if cell.orbs <= 0:
        #     cell.orbs = 0
        #     cell.player = Player.EMPTY
    
        # neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # for dr, dc in neighbors:
        #     nr, nc = row + dr, col + dc
        #     if 0 <= nr < self.rows and 0 <= nc < self.cols:
        #         neighbor_cell = self.board[nr][nc]
        #         neighbor_cell.orbs += 1
        #         neighbor_cell.player = exploding_player
    
    def _check_win_condition(self):
        """Check if game is over and determine winner"""
        red_orbs = 0
        blue_orbs = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player == Player.RED:
                    red_orbs += cell.orbs
                elif cell.player == Player.BLUE:
                    blue_orbs += cell.orbs
        
        total_orbs = red_orbs + blue_orbs

        if total_orbs > 0 and self.move_count >= 2:
            if red_orbs > 0 and blue_orbs == 0:
                self.game_over = True
                self.winner = Player.RED
            elif blue_orbs > 0 and red_orbs == 0:
                self.game_over = True
                self.winner = Player.BLUE
    
    def get_score(self) -> Dict[Player, int]:
        """Get current score for each player"""
        scores = {Player.RED: 0, Player.BLUE: 0}
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player in scores:
                    scores[cell.player] += cell.orbs
        return scores
    
    def display_board(self):
        """Display the current board state"""
        print("\nCurrent Board:")
        for row in range(self.rows):
            print(' '.join(str(self.board[row][col]) for col in range(self.cols)))
        
        scores = self.get_score()
        print(f"\nScores - Red: {scores[Player.RED]}, Blue: {scores[Player.BLUE]}")
        print(f"Current Player: {self.current_player.value}")
    
    def copy(self):
        """Create a deep copy of the game state"""
        new_game = ChainReactionGame(self.rows, self.cols)
        new_game.current_player = self.current_player
        new_game.game_over = self.game_over
        new_game.winner = self.winner
        new_game.move_count = self.move_count
        
        for row in range(self.rows):
            for col in range(self.cols):
                new_game.board[row][col].orbs = self.board[row][col].orbs
                new_game.board[row][col].player = self.board[row][col].player
        
        return new_game
    
    def to_file_format(self, move_type: str, mode : GameMode = GameMode.USER_VS_AI) -> str:
        """Convert board to file format with numerical representation"""
            
        lines = [f"{move_type} Move:"]        
        for row in range(self.rows):
            row_cells = []
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player == Player.EMPTY:
                    row_cells.append("0")
                elif cell.player == Player.RED:
                    row_cells.append(f"{cell.orbs}R")
                elif cell.player == Player.BLUE:
                    row_cells.append(f"{cell.orbs}B")
            lines.append(" ".join(row_cells))
        return '\n'.join(lines)
    
    def save_to_file(self, filename: str, move_type: str, game_mode: GameMode = GameMode.USER_VS_USER):
        """Save game state to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.to_file_format(move_type, mode=game_mode))
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'ChainReactionGame':
        """Load game state from file with numerical format"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            lines = content.split('\n')
            if not lines:
                raise ValueError("Empty file")
            
            # Skip the header line (e.g., "Human Move:")
            board_lines = lines[1:] if lines[0].endswith("Move:") else lines
            
            if not board_lines:
                raise ValueError("No board data found")
            
            # Determine board dimensions from the data
            first_line_cells = board_lines[0].split()
            cols = len(first_line_cells)
            rows = len(board_lines)   
            
            # Create new game instance
            game = cls(rows, cols)
            
            # Parse board state
            for row_idx, line in enumerate(board_lines):
                cells = line.split()
                if len(cells) != cols:
                    raise ValueError(f"Inconsistent column count in row {row_idx}")
                
                for col_idx, cell_str in enumerate(cells):
                    if cell_str == "0":
                        game.board[row_idx][col_idx].orbs = 0
                        game.board[row_idx][col_idx].player = Player.EMPTY
                    elif cell_str.endswith('R'):
                        orbs = int(cell_str[:-1])
                        game.board[row_idx][col_idx].orbs = orbs
                        game.board[row_idx][col_idx].player = Player.RED
                    elif cell_str.endswith('B'):
                        orbs = int(cell_str[:-1])
                        game.board[row_idx][col_idx].orbs = orbs
                        game.board[row_idx][col_idx].player = Player.BLUE
                    else:
                        raise ValueError(f"Invalid cell format: {cell_str}")
            
            # Restore game state from board
            game._restore_game_state_from_board()
            
            return game
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Game state file '{filename}' not found")
        except Exception as e:
            raise ValueError(f"Error loading game state: {str(e)}")
    
    def _restore_game_state_from_board(self):
        """Restore game state properties from board data"""
        red_orbs = 0
        blue_orbs = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.player == Player.RED:
                    red_orbs += cell.orbs
                elif cell.player == Player.BLUE:
                    blue_orbs += cell.orbs
        
        self.move_count = red_orbs + blue_orbs
        # Determine current player based on total moves
        self.current_player = Player.RED if self.move_count % 2 == 0 else Player.BLUE
        self._check_win_condition()
        
class ChainReactionHeuristics:
    @staticmethod
    def orb_count_heuristic(game: ChainReactionGame, player: Player) -> float:
        """Simple orb count difference"""
        scores = game.get_score()
        opponent = Player.BLUE if player == Player.RED else Player.RED
        return scores[player] - scores[opponent]
    
    @staticmethod
    def explosion_potential_heuristic(game: ChainReactionGame, player: Player) -> float:
        """Evaluates potential chain reaction opportunities"""
        score = 0
        opponent = Player.BLUE if player == Player.RED else Player.RED
        
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.board[row][col]
                critical = game.get_critical_mass(row, col)
                
                if cell.player == player:
                    if cell.orbs == critical - 1:
                        score += 50
                    neighbor_bonus = 0
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < game.rows and 0 <= nc < game.cols:
                            neighbor = game.board[nr][nc]
                            if neighbor.player == opponent and neighbor.orbs > 0:
                                neighbor_bonus += 15  
                            elif neighbor.player == player:
                                neighbor_bonus += 5   
                    score += neighbor_bonus * (cell.orbs / critical)
                
                elif cell.player == opponent:
                    if cell.orbs == critical - 1:
                        score -= 60  
        return score

    @staticmethod
    def strategic_eval_heuristic(game: ChainReactionGame, player: Player) -> float:
        """ Based on game state and positioning"""
        score = 0
        opponent = Player.BLUE if player == Player.RED else Player.RED
        center_row, center_col = game.rows // 2, game.cols // 2

        for i in range(game.rows):
            for j in range(game.cols):
                cell = game.board[i][j]

                if cell.player == player and cell.orbs > 0:
                    score += cell.orbs
                    critical_opponent_neighbors = []
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = i + dr, j + dc
                        if 0 <= nr < game.rows and 0 <= nc < game.cols:
                            nei_cell = game.board[nr][nc]
                            if (nei_cell.player == opponent and 
                                nei_cell.orbs == game.get_critical_mass(nr, nc) - 1):
                                critical_opponent_neighbors.append((nr, nc))
                    
                    # If there's nearby explodable opponent cells, increase score
                    if critical_opponent_neighbors:
                        for nr, nc in critical_opponent_neighbors:
                            opp_critical_mass = game.get_critical_mass(nr, nc)
                            score -= (50 - 10*opp_critical_mass)
                    else:
                        # If no critical opponent neighbors, add positional bonuses

                        # for corners
                        if (i == 0 or i == game.rows-1) and (j == 0 or j == game.cols-1):
                            score += 30
                        # for edges
                        elif i == 0 or i == game.rows-1 or j == 0 or j == game.cols-1:
                            score += 20
                        
                        # for explodable cells
                        if cell.orbs >= game.get_critical_mass(i, j) - 1:
                            score += 20
        return score


    @staticmethod
    def threat_analysis_heuristic(game: ChainReactionGame, player: Player) -> float:
        """Advanced threat detection and response evaluation"""
        score = 0
        opponent = Player.BLUE if player == Player.RED else Player.RED
        immediate_threats = 0
        potential_threats = 0
        
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.board[row][col]
                critical = game.get_critical_mass(row, col)
                
                if cell.player == opponent:
                    # Immediate threats (will explode next turn)
                    if cell.orbs == critical - 1:
                        immediate_threats += 1
                        # Evaluating ability to block
                        can_block = False
                        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < game.rows and 0 <= nc < game.cols:
                                if game.board[nr][nc].player == player:
                                    can_block = True
                                    break
                        score -= 50 if not can_block else 25
                    
                    # Potential threats (could explode soon)
                    elif cell.orbs >= critical - 2:
                        potential_threats += 1
                        score -= 20 * (cell.orbs / critical)
                
                elif cell.player == player:
                    #defensive formations
                    if cell.orbs > 0:
                        defensive_strength = 0
                        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < game.rows and 0 <= nc < game.cols:
                                neighbor = game.board[nr][nc]
                                if neighbor.player == player:
                                    defensive_strength += neighbor.orbs
                        score += min(30, defensive_strength * 2)
        
        #Global threat assessment
        threat_ratio = (immediate_threats * 2 + potential_threats) / max(1, game.rows * game.cols)
        score -= 100 * threat_ratio
        
        return score

    @staticmethod
    def tempo_heuristic(game: ChainReactionGame, player: Player) -> float:
        """Measures initiative and turn advantage"""
        score = 0
        opponent = Player.BLUE if player == Player.RED else Player.RED
        
        player_forcing_moves = 0
        opponent_forcing_moves = 0
        
        for row in range(game.rows):
            for col in range(game.cols):
                cell = game.board[row][col]
                critical = game.get_critical_mass(row, col)
                
                # forcing moves are those that make a cell explodable
                if cell.player == player and cell.orbs == critical - 2:
                    player_forcing_moves += 1
                elif cell.player == opponent and cell.orbs == critical - 2:
                    opponent_forcing_moves += 1
        
        #evaluate board development
        player_development = sum(cell.orbs for row in game.board for cell in row if cell.player == player)
        opponent_development = sum(cell.orbs for row in game.board for cell in row if cell.player == opponent)
        development_ratio = player_development / max(1, opponent_development)
        
        #calculate tempo score
        score += (player_forcing_moves - opponent_forcing_moves) * 40
        return score

    @staticmethod
    def strat_eval_expl_potential_combined_heuristic(game: ChainReactionGame, player: Player) -> float:
        """Combined heuristic using strategic evaluation and explosion potential"""
        score = 2*ChainReactionHeuristics.strategic_eval_heuristic(game, player)
        score += ChainReactionHeuristics.explosion_potential_heuristic(game, player)
        return score

class MinimaxAI:
    def __init__(self, player: Player, depth: int = 3, heuristic_func=None):
        self.player = player
        self.depth = depth
        self.heuristic_func = heuristic_func or ChainReactionHeuristics.orb_count_heuristic
        self.nodes_evaluated = 0
        self.nodes_pruned = 0
        self.total_moves_considered = 0
        self.cache_hits = 0
        self.transposition_table = {}
        self.max_nodes = 750000  # Conservative node limit
        self.search_start_time = 0
        self.max_search_time = 10.0  # Conservative time limit

    def get_game_state_key(self, game: ChainReactionGame) -> tuple:
        """Generate a hashable key for the game state"""
        state = tuple((cell.orbs, cell.player.value) for row in game.board for cell in row)
        return (state, game.current_player.value)

    def minimax_search(self, game: ChainReactionGame, depth: int, 
                      alpha: float = float('-inf'), beta: float = float('inf'), 
                      maximizing: bool = True) -> Tuple[float, Optional[Tuple[int, int]]]:
        self.nodes_evaluated += 1
    
        if (time.time() - self.search_start_time > self.max_search_time or 
            self.nodes_evaluated > self.max_nodes):
            return self.heuristic_func(game, self.player), None
        
        #state key for caching
        state_key = self.get_game_state_key(game)
        
        #check transposition table
        if state_key in self.transposition_table:
            cached_score, cached_depth, cached_move = self.transposition_table[state_key]
            if cached_depth >= depth:
                self.cache_hits += 1
                return cached_score, cached_move
        
        #base cases: 
        if depth == 0 or game.game_over:
            if game.game_over:
                score = 1e9 if game.winner == self.player else (-1e9 if game.winner is not None else 0)
            else:
                score = self.heuristic_func(game, self.player)
            self.transposition_table[state_key] = (score, depth, None)
            return score, None
        
        current_player = self.player if maximizing else (Player.BLUE if self.player == Player.RED else Player.RED)
        valid_moves = game.get_valid_moves(current_player)
        
        if not valid_moves:
            # If current player has no moves, they lose (all cell occupied)
            if current_player == self.player:
                score = -1e9  
            else:
                score = 1e9   
            self.transposition_table[state_key] = (score, depth, None)
            return score, None
        
        best_move = None
        moves_evaluated = 0
        
        # For Max agent
        if maximizing:
            max_eval = float('-inf')
            for move in valid_moves:
                if (time.time() - self.search_start_time > self.max_search_time or 
                    self.nodes_evaluated > self.max_nodes):
                    break
                    
                self.total_moves_considered += 1
                moves_evaluated += 1
                game_copy = game.copy()
                game_copy.make_move(move[0], move[1], current_player)
                
                eval_score, _ = self.minimax_search(game_copy, depth - 1, alpha, beta, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                    
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    self.nodes_pruned += len(valid_moves) - moves_evaluated
                    break
                    
            self.transposition_table[state_key] = (max_eval, depth, best_move)
            return max_eval, best_move
        # For Min agent 
        else: 
            min_eval = float('inf')
            for move in valid_moves:
                if (time.time() - self.search_start_time > self.max_search_time or 
                    self.nodes_evaluated > self.max_nodes):
                    break
                    
                self.total_moves_considered += 1
                moves_evaluated += 1
                
                game_copy = game.copy()
                game_copy.make_move(move[0], move[1], current_player)
                eval_score, _ = self.minimax_search(game_copy, depth - 1, alpha, beta, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    self.nodes_pruned += len(valid_moves) - moves_evaluated
                    break
                    
            self.transposition_table[state_key] = (min_eval, depth, best_move)
            return min_eval, best_move

    def get_best_move(self, game: ChainReactionGame) -> Optional[Tuple[int, int]]:
        self.nodes_evaluated = 0
        self.nodes_pruned = 0
        self.total_moves_considered = 0
        self.cache_hits = 0
        self.transposition_table.clear()
        self.search_start_time = time.time()
        
        total_orbs = sum(cell.orbs for row in game.board for cell in row if cell.player != Player.EMPTY)
        valid_moves_count = len(game.get_valid_moves(self.player))
        # print(f" --- AI searching at depth {self.depth} for {total_orbs} orbs, {valid_moves_count} valid moves")
        
        _, best_move = self.minimax_search(game, self.depth)
        
        search_time = time.time() - self.search_start_time
        # print(f" --- Search completed in {search_time:.2f}s with {self.nodes_evaluated:,} nodes")
        return best_move
    
class RandomAI:
    """Simple AI that makes random valid moves"""
    
    def __init__(self, player: Player):
        self.player = player
    
    def get_best_move(self, game: ChainReactionGame) -> Optional[Tuple[int, int]]:
        """Get a random valid move"""
        valid_moves = game.get_valid_moves(self.player)
        if not valid_moves:
            return None
        move = random.choice(valid_moves)
        # print(f" --- Random AI selected move: {move[0]}, {move[1]}")
        return move

class GameController:
    def __init__(self):
        self.game = None
        self.ai_red = None
        self.ai_blue = None
        self.start_time = None
        self.game_state_file = "gamestate.txt"  
    
    def get_game_configuration(self) -> Tuple[int, int, int, int, 'AIType' , 'AIType' , 'GameMode' , Callable, Callable]:
        """Get game configuration from user"""
        print("🎮 Chain Reaction Game")
        # print("🚀 Features: Game-over detection during explosions (no infinite loops!)")
        print("=" * 60)
       
        print("\n🔲 Grid Size Configuration:")
        while True:
            try:
                rows = int(input("Enter number of rows (3-10): "))
                if 3 <= rows <= 10:
                    break
                else:
                    print("Invalid input. Please enter a number between 3 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        while True:
            try:
                cols = int(input("Enter number of columns (3-10): "))
                if 3 <= cols <= 10:
                    break
                else:
                    print("Invalid input. Please enter a number between 3 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        print("\n🎯 Game Mode Selection:")
        print("1. User vs User")
        print("2. User vs AI")
        print("3. AI vs AI")
        depth_red = 1
        depth_blue = 1
        
        while True:
            try:
                mode_choice = int(input("Select game mode (1-3): "))
                if mode_choice in [1, 2, 3]:
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Print options for depth
        def ai_depth_menu(player_name: str = "") -> int:
            print(f"\n🤖 Smart {player_name} AI Difficulty Configuration:")
            print("2 - Easy (Fast)")
            print("3 - Medium (Balanced)")
            print("4 - Hard (Strategic)")
            # Take depth input
            while True:
                try:
                    d = int(input("Select Smart AI depth (2-4): "))
                    if 2 <= d <= 4:
                        break
                    else:
                        print("Invalid input. Please enter 2, 3, or 4.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            return d
        
        
        def get_ai_type(player_name: str) -> AIType:
            print(f"\n{player_name} AI Type:")
            print("1 - Smart AI (Strategic Minimax)")
            print("2 - Random AI (Makes random moves)")
            
            while True:
                try:
                    choice = int(input(f"Select {player_name} AI type (1-2): "))
                    if choice == 1:
                        return AIType.SMART
                    elif choice == 2:
                        return AIType.RANDOM
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        
        def get_heuristic_choice(player_name: str):
            """Get heuristic function choice for Smart AI"""
            print(f"\n🧠 {player_name} Smart AI Heuristic Selection:")
            print("1 - Orb Count (Simple orb difference)")
            print("2 - Explosion Potential (Chain reaction focus)")
            print("3 - Strategic Evaluation (Board control and positioning)")
            print("4 - Threat Analysis (Defensive play)")
            print("5 - Tempo (Initiative and forcing moves)")
            print("6 - Combined Strategy (Strategic + Explosion Potential)")
            
            while True:
                try:
                    choice = int(input(f"Select {player_name} AI heuristic (1-6): "))
                    if choice == 1:
                        return ChainReactionHeuristics.orb_count_heuristic
                    elif choice == 2:
                        return ChainReactionHeuristics.explosion_potential_heuristic
                    elif choice == 3:
                        return ChainReactionHeuristics.strategic_eval_heuristic
                    elif choice == 4:
                        return ChainReactionHeuristics.threat_analysis_heuristic
                    elif choice == 5:
                        return ChainReactionHeuristics.tempo_heuristic
                    elif choice == 6:
                        return ChainReactionHeuristics.strat_eval_expl_potential_combined_heuristic
                    else:
                        print("Invalid choice. Please enter 1-6.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
        
        if mode_choice == 1:  # User vs User
            print("\n👥 User vs User mode selected")
            red_ai_type : Optional['AIType'] = None 
            blue_ai_type : Optional['AIType'] = None
            red_heuristic : Optional[Callable] = None
            blue_heuristic : Optional[Callable] = None
        elif mode_choice == 2:  # User vs AI  
            print("\n🤖 Human vs AI mode selected:")
            red_ai_type : Optional['AIType'] = None  
            blue_ai_type = get_ai_type("Blue")

            red_heuristic = None
            
            if blue_ai_type == AIType.SMART:
                depth_blue = ai_depth_menu("Blue")
                blue_heuristic = get_heuristic_choice("Blue")
            else:
                blue_heuristic = None
        else:  
            print("\n🤖 AI vs AI Configuration:")
            red_ai_type = get_ai_type("Red")
            blue_ai_type = get_ai_type("Blue")
            
            if red_ai_type == AIType.SMART:
                depth_red = ai_depth_menu("Red")
                red_heuristic = get_heuristic_choice("Red")
            else:
                red_heuristic = None
                
            if blue_ai_type == AIType.SMART:
                depth_blue = ai_depth_menu("Blue")
                blue_heuristic = get_heuristic_choice("Blue")
            else:
                blue_heuristic = None
        
        return rows, cols, depth_red, depth_blue, red_ai_type, blue_ai_type, GameMode(mode_choice), red_heuristic, blue_heuristic
    
    def initialize_game(self, rows: int, cols: int, depth_red: int, depth_blue: int, red_ai_type: AIType, blue_ai_type: AIType, red_heuristic=None, blue_heuristic=None):
        """Initialize game with specified configuration"""
        self.game = ChainReactionGame(rows, cols)
        
        if red_ai_type == AIType.SMART:
            heuristic = red_heuristic or ChainReactionHeuristics.orb_count_heuristic
            self.ai_red = MinimaxAI(Player.RED, depth=depth_red, heuristic_func=heuristic)
        elif red_ai_type == AIType.RANDOM:
            self.ai_red = RandomAI(Player.RED)
        else:
            self.ai_red = None
            
        if blue_ai_type == AIType.SMART:
            heuristic = blue_heuristic or ChainReactionHeuristics.threat_analysis_heuristic
            self.ai_blue = MinimaxAI(Player.BLUE, depth=depth_blue, heuristic_func=heuristic)
        elif blue_ai_type == AIType.RANDOM:
            self.ai_blue = RandomAI(Player.BLUE)
        else:
            self.ai_blue = None
        
        print(f"\n✅ Game initialized: {rows}x{cols} grid")
        if red_ai_type:
            print(f"🔴 Red AI: {red_ai_type.value}")
            if red_ai_type == AIType.SMART and red_heuristic:
                print(f"    📈 Red AI Heuristic: {red_heuristic.__name__.replace('_heuristic', '').replace('_', ' ').title()}")
        if blue_ai_type:    
            print(f"🔵 Blue AI: {blue_ai_type.value}")
            if blue_ai_type == AIType.SMART and blue_heuristic:
                print(f"    📈 Blue AI Heuristic: {blue_heuristic.__name__.replace('_heuristic', '').replace('_', ' ').title()}")
        if red_ai_type == AIType.SMART:
            print(f"🎯 Smart Red AI depth: {depth_red}")
        if blue_ai_type == AIType.SMART:
            print(f"🎯 Smart Blue AI depth: {depth_blue}")
    
    def get_game_mode(self) -> GameMode:
        """Get game mode from user"""
        print("\n🎯 Game Mode Selection:")
        print("1. User vs User")
        print("2. User vs AI")
        print("3. AI vs AI")
        
        while True:
            try:
                choice = int(input("Select game mode (1-3): "))
                if choice in [1, 2, 3]:
                    return GameMode(choice)
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def get_user_move(self, player: Player) -> Tuple[int, int]:
        """Get move from user with immediate validation"""
        while True:
            try:
                print(f"\n{player.value} player's turn")
                move_input = input("Enter move as 'row col' (0-indexed, e.g., '0 1'): ")
                row, col = map(int, move_input.strip().split())
                if not (0 <= row < self.game.rows and 0 <= col < self.game.cols):
                    print(f"❌ Invalid position! Row must be 0-{self.game.rows-1}, column must be 0-{self.game.cols-1}")
                    continue
                    
                if not self.game.is_valid_move(row, col, player):
                    cell = self.game.board[row][col]
                    if cell.player != Player.EMPTY and cell.player != player:
                        print(f"❌ That cell belongs to {cell.player.value}! You can only place on empty cells or your own cells.")
                    continue
                    
                return row, col
            except ValueError:
                print("❌ Invalid input. Please enter two numbers separated by a space.")
            except KeyboardInterrupt:
                print("\n👋 Game cancelled by user.")
                exit(0)

    def play_game(self):
        """Main game loop with file-based backend"""
        rows, cols, depth_red, depth_blue, red_ai_type, blue_ai_type, mode, red_heuristic, blue_heuristic = self.get_game_configuration()
        self.initialize_game(rows, cols, depth_red, depth_blue, red_ai_type, blue_ai_type, red_heuristic, blue_heuristic)
        
        self.start_time = time.time()
        #save initial game state to file
        if mode == GameMode.USER_VS_USER:
            self.game.save_to_file(self.game_state_file, "First")
        elif mode == GameMode.USER_VS_AI:
            self.game.save_to_file(self.game_state_file, "Human")
        else:  # AI vs AI
            self.game.save_to_file(self.game_state_file, "AI Red")
                    
        print(f"\n*** Starting {mode.name.replace('_', ' ').title()} game! ***")
        print("=" * 60)
        
        while True:
            try:
                self.game = ChainReactionGame.load_from_file(self.game_state_file)
            except (FileNotFoundError, ValueError) as e:
                print(f"❌ Error loading game state: {e}")
                break
            if self.game.game_over:
                break
                
            self.game.display_board()
            
            current_player = self.game.current_player
            
            if mode == GameMode.USER_VS_USER:
                row, col = self.get_user_move(current_player)
                self.game.make_move(row, col, current_player)
                move_type = f"{current_player.value}"
                self.game.save_to_file(self.game_state_file, move_type)
                    
            elif mode == GameMode.USER_VS_AI:
                if current_player == Player.RED:
                    row, col = self.get_user_move(current_player)
                    self.game.make_move(row, col, current_player)
                    self.game.save_to_file(self.game_state_file, "Human")
                else:
                    ai_type_name = blue_ai_type.value
                    print(f"\n🤖 {ai_type_name} ({current_player.value}) is thinking...")
                    if blue_ai_type == AIType.SMART:
                        heuristic = blue_heuristic or ChainReactionHeuristics.threat_analysis_heuristic
                        ai_instance = MinimaxAI(Player.BLUE, depth_blue, heuristic_func=heuristic)
                    else:
                        ai_instance = RandomAI(Player.BLUE)
                    
                    move = ai_instance.get_best_move(self.game)
                    if move and self.game.make_move(move[0], move[1], current_player):
                        print(f"{ai_type_name} plays: {move[0]}, {move[1]}")
                        self.game.save_to_file(self.game_state_file, f"AI")
                    else:
                        print(f"{ai_type_name} could not find a valid move!")
                        break
                        
            elif mode == GameMode.AI_VS_AI:
                if current_player == Player.RED:
                    ai_type_name = red_ai_type.value
                    if red_ai_type == AIType.SMART:
                        heuristic = red_heuristic or ChainReactionHeuristics.orb_count_heuristic
                        ai_instance = MinimaxAI(Player.RED, depth_red, heuristic_func=heuristic)
                    else:
                        ai_instance = RandomAI(Player.RED)
                else:
                    ai_type_name = blue_ai_type.value
                    if blue_ai_type == AIType.SMART:
                        heuristic = blue_heuristic or ChainReactionHeuristics.threat_analysis_heuristic
                        ai_instance = MinimaxAI(Player.BLUE, depth_blue, heuristic_func=heuristic)
                    else:
                        ai_instance = RandomAI(Player.BLUE)
                
                print(f"\n🤖 {ai_type_name} ({current_player.value}) is thinking...")
                move = ai_instance.get_best_move(self.game)
                
                if move and self.game.make_move(move[0], move[1], current_player):
                    print(f"{ai_type_name} ({current_player.value}) plays: {move[0]}, {move[1]}")
                    ai_move_type = f"{ai_type_name} ({current_player.value})"
                    self.game.save_to_file(self.game_state_file, ai_move_type)
                else:
                    print(f"{ai_type_name} ({current_player.value}) could not find a valid move!")
                    break
        #final state loaded
        try:
            self.game = ChainReactionGame.load_from_file(self.game_state_file)
        except (FileNotFoundError, ValueError):
            pass  #current state if loading fails
        # Game over
        self.game.save_to_file(self.game_state_file, "Game Over")
        
        self.game.display_board()
        elapsed_time = time.time() - self.start_time
        
        print("\n" + "=" * 50)
        print(" GAME OVER! ")
        if self.game.winner:
            print(f" Winner: {self.game.winner.value} Player!")
        else:
            print(" It's a draw! (ERROR)")
        
        scores = self.game.get_score()
        print(f" Final Scores - Red: {scores[Player.RED]}, Blue: {scores[Player.BLUE]}")
        print(f"  Game duration: {elapsed_time:.1f} seconds")
        print(f" Game state saved to: {self.game_state_file}")
        print("=" * 50)

if __name__ == "__main__":
    controller = GameController()
    controller.play_game()
