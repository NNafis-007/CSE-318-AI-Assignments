# 🚀 Quick Development Guide - Chain Reaction Game

## 🎯 **Most Common Development Tasks**

### 1. 🎮 **Adding Game Logic (Chain Reaction Rules)**

#### **Step 1: Enhance GameBoard class**
```python
# In src/screens/game_screen.py - GameBoard class

def __init__(self, rows=GRID_ROWS, cols=GRID_COLS):
    self.rows = rows
    self.cols = cols
    # Change from None to empty dict for each cell
    self.board = [[{"player": None, "count": 0} for _ in range(cols)] for _ in range(rows)]
    self.current_player = 1
    self.max_players = 2
    self.player_colors = {1: BLUE, 2: (255, 0, 0)}  # Red

def get_max_capacity(self, row: int, col: int) -> int:
    """Get maximum capacity for a cell based on position"""
    # Corner cells: capacity 2
    if (row == 0 or row == self.rows-1) and (col == 0 or col == self.cols-1):
        return 2
    # Edge cells: capacity 3
    elif row == 0 or row == self.rows-1 or col == 0 or col == self.cols-1:
        return 3
    # Center cells: capacity 4
    else:
        return 4

def place_piece(self, row: int, col: int, player: int) -> bool:
    """Place a piece and handle chain reactions"""
    if not self.is_valid_position(row, col):
        return False
    
    cell = self.board[row][col]
    
    # Can only place on empty cells or own pieces
    if cell["player"] is not None and cell["player"] != player:
        return False
    
    # Place the piece
    cell["player"] = player
    cell["count"] += 1
    
    # Check for explosion and chain reaction
    self.check_explosions()
    return True

def check_explosions(self):
    """Check for explosions and handle chain reactions"""
    exploded = True
    while exploded:
        exploded = False
        explosion_queue = []
        
        # Find all cells that should explode
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell["count"] >= self.get_max_capacity(row, col):
                    explosion_queue.append((row, col))
        
        # Process explosions
        for row, col in explosion_queue:
            self.explode_cell(row, col)
            exploded = True

def explode_cell(self, row: int, col: int):
    """Explode a cell and distribute pieces to neighbors"""
    cell = self.board[row][col]
    player = cell["player"]
    
    # Reset the exploding cell
    cell["player"] = None
    cell["count"] = 0
    
    # Distribute to neighbors
    neighbors = self.get_neighbors(row, col)
    for neighbor_row, neighbor_col in neighbors:
        neighbor_cell = self.board[neighbor_row][neighbor_col]
        neighbor_cell["player"] = player  # Convert to exploding player
        neighbor_cell["count"] += 1

def get_neighbors(self, row: int, col: int) -> list:
    """Get valid neighboring cells"""
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if self.is_valid_position(new_row, new_col):
            neighbors.append((new_row, new_col))
    
    return neighbors

def check_winner(self) -> Optional[int]:
    """Check if there's a winner"""
    players_with_pieces = set()
    
    for row in range(self.rows):
        for col in range(self.cols):
            cell = self.board[row][col]
            if cell["player"] is not None:
                players_with_pieces.add(cell["player"])
    
    if len(players_with_pieces) == 1:
        return list(players_with_pieces)[0]
    elif len(players_with_pieces) == 0:
        return None  # Draw
    else:
        return None  # Game continues
```

#### **Step 2: Update GameScreen to use new logic**
```python
# In src/screens/game_screen.py - GameScreen class

def __init__(self, ui_renderer: UIRenderer, game_mode: GameMode):
    self.ui_renderer = ui_renderer
    self.game_mode = game_mode
    self.board = GameBoard()
    self.game_over = False
    self.winner = None

def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[str]:
    if self.game_over:
        return None
        
    cell_pos = self.board.get_cell_from_mouse_pos(pos)
    if cell_pos:
        row, col = cell_pos
        if self.board.place_piece(row, col, self.board.current_player):
            print(f"Player {self.board.current_player} placed piece at ({row}, {col})")
            
            # Check for winner
            winner = self.board.check_winner()
            if winner:
                self.game_over = True
                self.winner = winner
                print(f"Player {winner} wins!")
            else:
                self.board.current_player = 2 if self.board.current_player == 1 else 1
        else:
            print("Invalid move!")
    return None

def draw(self, surface: pygame.Surface):
    surface.fill(WHITE)
    
    # Draw title with current game mode
    self.ui_renderer.draw_text(surface, f"Mode: {self.game_mode.value}", 
                             WINDOW_WIDTH // 2, 30, "title")
    
    # Draw current player or winner
    if self.game_over:
        if self.winner:
            self.ui_renderer.draw_text(surface, f"Player {self.winner} Wins!", 
                                     WINDOW_WIDTH // 2, 70, "normal", (255, 0, 0))
        else:
            self.ui_renderer.draw_text(surface, "It's a Draw!", 
                                     WINDOW_WIDTH // 2, 70, "normal", GRAY)
    else:
        self.ui_renderer.draw_text(surface, f"Current Player: {self.board.current_player}", 
                                 WINDOW_WIDTH // 2, 70, "normal")
    
    # Draw the grid
    self.ui_renderer.draw_grid(surface)
    
    # Draw game pieces
    for row in range(self.board.rows):
        for col in range(self.board.cols):
            cell = self.board.board[row][col]
            if cell["count"] > 0:
                x = GRID_X + col * CELL_SIZE
                y = GRID_Y + row * CELL_SIZE
                self.draw_game_piece(surface, x, y, cell["count"], cell["player"])
    
    # Draw instructions
    if not self.game_over:
        self.ui_renderer.draw_text(surface, "Click a cell to place your piece", 
                                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, "normal", GRAY)
    else:
        self.ui_renderer.draw_text(surface, "Press ESC to return to menu", 
                                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, "normal", GRAY)
    
    self.ui_renderer.draw_text(surface, "Press ESC to go back to menu", 
                             WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20, "normal", GRAY)

def draw_game_piece(self, surface, x, y, count, player):
    """Draw game pieces with multiple dots"""
    player_color = self.board.player_colors.get(player, BLACK)
    
    # Calculate dot positions based on count
    dot_positions = []
    center_x = x + CELL_SIZE // 2
    center_y = y + CELL_SIZE // 2
    
    if count == 1:
        dot_positions = [(center_x, center_y)]
    elif count == 2:
        dot_positions = [(center_x - 10, center_y), (center_x + 10, center_y)]
    elif count == 3:
        dot_positions = [(center_x, center_y - 10), (center_x - 10, center_y + 10), (center_x + 10, center_y + 10)]
    elif count >= 4:
        dot_positions = [(center_x - 10, center_y - 10), (center_x + 10, center_y - 10),
                        (center_x - 10, center_y + 10), (center_x + 10, center_y + 10)]
    
    # Draw dots
    for pos in dot_positions:
        pygame.draw.circle(surface, player_color, pos, 8)
        pygame.draw.circle(surface, BLACK, pos, 8, 2)  # Border
```

### 2. 🎨 **Enhancing UI Components**

#### **Add new drawing methods to UIRenderer**
```python
# In src/ui/ui_renderer.py

def draw_game_piece(self, surface, x, y, count, player_color):
    """Draw a game piece with count indicators"""
    # Implementation above

def draw_player_panel(self, surface, player_num, is_current, color):
    """Draw player information panel"""
    panel_width = 150
    panel_height = 80
    x = 50 if player_num == 1 else WINDOW_WIDTH - panel_width - 50
    y = 100
    
    # Draw panel background
    bg_color = LIGHT_GRAY if not is_current else color
    panel_rect = pygame.Rect(x, y, panel_width, panel_height)
    pygame.draw.rect(surface, bg_color, panel_rect)
    pygame.draw.rect(surface, BLACK, panel_rect, 2)
    
    # Draw player text
    self.draw_text(surface, f"Player {player_num}", x + panel_width//2, y + 20, "normal", BLACK)
    if is_current:
        self.draw_text(surface, "Your Turn", x + panel_width//2, y + 50, "small", BLACK)

def draw_explosion_effect(self, surface, x, y):
    """Draw explosion animation effect"""
    # Add visual effects for explosions
    explosion_radius = 30
    pygame.draw.circle(surface, (255, 255, 0), (x + CELL_SIZE//2, y + CELL_SIZE//2), explosion_radius, 3)
```

### 3. 🤖 **Adding AI Players**

#### **Create AI module**
```python
# Create new file: src/ai/ai_player.py

import random
from typing import Tuple, Optional
from src.screens.game_screen import GameBoard

class AIPlayer:
    """Simple AI player for Chain Reaction"""
    
    def __init__(self, player_id: int, difficulty: str = "easy"):
        self.player_id = player_id
        self.difficulty = difficulty
    
    def get_move(self, board: GameBoard) -> Optional[Tuple[int, int]]:
        """Get AI move based on difficulty"""
        if self.difficulty == "easy":
            return self.get_random_move(board)
        elif self.difficulty == "medium":
            return self.get_strategic_move(board)
        elif self.difficulty == "hard":
            return self.get_optimal_move(board)
    
    def get_random_move(self, board: GameBoard) -> Optional[Tuple[int, int]]:
        """Random valid move"""
        valid_moves = []
        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.board[row][col]
                if cell["player"] is None or cell["player"] == self.player_id:
                    valid_moves.append((row, col))
        
        return random.choice(valid_moves) if valid_moves else None
    
    def get_strategic_move(self, board: GameBoard) -> Optional[Tuple[int, int]]:
        """Strategic move - prefer corners and edges"""
        # Prioritize corners, then edges, then center
        for priority in ["corner", "edge", "center"]:
            moves = self.get_moves_by_type(board, priority)
            if moves:
                return random.choice(moves)
        return None
    
    def get_moves_by_type(self, board: GameBoard, move_type: str) -> list:
        """Get moves of specific type"""
        moves = []
        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.board[row][col]
                if cell["player"] is None or cell["player"] == self.player_id:
                    if move_type == "corner" and self.is_corner(row, col, board):
                        moves.append((row, col))
                    elif move_type == "edge" and self.is_edge(row, col, board):
                        moves.append((row, col))
                    elif move_type == "center" and self.is_center(row, col, board):
                        moves.append((row, col))
        return moves
    
    def is_corner(self, row: int, col: int, board: GameBoard) -> bool:
        return (row == 0 or row == board.rows-1) and (col == 0 or col == board.cols-1)
    
    def is_edge(self, row: int, col: int, board: GameBoard) -> bool:
        return (row == 0 or row == board.rows-1 or col == 0 or col == board.cols-1) and not self.is_corner(row, col, board)
    
    def is_center(self, row: int, col: int, board: GameBoard) -> bool:
        return not self.is_corner(row, col, board) and not self.is_edge(row, col, board)
```

#### **Integrate AI into GameScreen**
```python
# In src/screens/game_screen.py

from src.ai.ai_player import AIPlayer  # Add this import

def __init__(self, ui_renderer: UIRenderer, game_mode: GameMode):
    # ...existing code...
    self.ai_players = {}
    
    if game_mode == GameMode.HUMAN_VS_AI:
        self.ai_players[2] = AIPlayer(2, "medium")
    elif game_mode == GameMode.AI_VS_AI:
        self.ai_players[1] = AIPlayer(1, "easy")
        self.ai_players[2] = AIPlayer(2, "medium")

def update_ai_turn(self):
    """Handle AI turn"""
    if not self.game_over and self.board.current_player in self.ai_players:
        ai_player = self.ai_players[self.board.current_player]
        move = ai_player.get_move(self.board)
        if move:
            row, col = move
            if self.board.place_piece(row, col, self.board.current_player):
                print(f"AI Player {self.board.current_player} placed piece at ({row}, {col})")
                
                winner = self.board.check_winner()
                if winner:
                    self.game_over = True
                    self.winner = winner
                else:
                    self.board.current_player = 2 if self.board.current_player == 1 else 1
```

#### **Update Game.update() for AI timing**
```python
# In src/core/game_manager.py - Game class

def __init__(self):
    # ...existing code...
    self.ai_timer = 0
    self.ai_delay = 1000  # 1 second delay for AI moves

def update(self):
    """Update game logic"""
    if self.state_manager.current_state == GameState.GAME and self.state_manager.game_screen:
        # Handle AI turns with delay
        self.ai_timer += self.clock.get_time()
        if self.ai_timer >= self.ai_delay:
            self.state_manager.game_screen.update_ai_turn()
            self.ai_timer = 0
```

### 4. ⚙️ **Adding New Screens (Settings Example)**

#### **Step 1: Add to enums**
```python
# In src/config/enums.py
class GameState(Enum):
    MENU = "menu"
    GAME = "game"
    SETTINGS = "settings"  # New state
```

#### **Step 2: Create settings screen**
```python
# Create new file: src/screens/settings_screen.py

import pygame
from typing import Optional
from src.core.interfaces import EventHandler
from src.ui.ui_renderer import UIRenderer
from src.config.config import *

class SettingsScreen(EventHandler):
    """Settings screen implementation"""
    
    def __init__(self, ui_renderer: UIRenderer):
        self.ui_renderer = ui_renderer
        self.button_rects = {}
        self.settings = {
            "ai_difficulty": "medium",
            "sound_enabled": True,
            "grid_size": "9x6"
        }
    
    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[str]:
        """Handle settings button clicks"""
        # Implementation for settings interactions
        return None
    
    def handle_key_press(self, key: int) -> Optional[str]:
        """Handle key presses in settings"""
        if key == pygame.K_ESCAPE:
            return "back_to_menu"
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the settings screen"""
        surface.fill(WHITE)
        
        # Draw title
        self.ui_renderer.draw_text(surface, "Settings", WINDOW_WIDTH // 2, 100, "title")
        
        # Draw settings options
        y_start = 200
        for i, (setting, value) in enumerate(self.settings.items()):
            y = y_start + i * 60
            self.ui_renderer.draw_text(surface, f"{setting}: {value}", 
                                     WINDOW_WIDTH // 2, y, "normal")
        
        # Draw back instruction
        self.ui_renderer.draw_text(surface, "Press ESC to go back", 
                                 WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, "normal", GRAY)
```

#### **Step 3: Update GameStateManager**
```python
# In src/core/game_manager.py - GameStateManager class

def __init__(self):
    # ...existing code...
    self.settings_screen = None

def transition_to_settings(self):
    """Transition to settings screen"""
    self.current_state = GameState.SETTINGS
    if not self.settings_screen:
        self.settings_screen = SettingsScreen(self.ui_renderer)

def handle_mouse_click(self, pos: tuple[int, int]):
    # ...existing code...
    elif self.current_state == GameState.SETTINGS and self.settings_screen:
        self.settings_screen.handle_mouse_click(pos)

def handle_key_press(self, key: int) -> bool:
    # ...existing code...
    elif self.current_state == GameState.SETTINGS and self.settings_screen:
        result = self.settings_screen.handle_key_press(key)
        if result == "back_to_menu":
            self.transition_to_menu()

def draw(self, surface: pygame.Surface):
    # ...existing code...
    elif self.current_state == GameState.SETTINGS and self.settings_screen:
        self.settings_screen.draw(surface)
```

## 🎯 **Next Steps Checklist**

### ✅ **Immediate Tasks (Easy)**
- [ ] Implement basic Chain Reaction rules in GameBoard
- [ ] Add game piece visual representation
- [ ] Add win condition checking
- [ ] Add turn switching logic

### ✅ **Medium Tasks**
- [ ] Add AI player with different difficulty levels
- [ ] Add explosion animations
- [ ] Add sound effects
- [ ] Add score tracking

### ✅ **Advanced Tasks**
- [ ] Add network multiplayer support
- [ ] Add replay system
- [ ] Add tournament mode
- [ ] Add custom board sizes

This guide gives you concrete, copy-paste examples for the most common development tasks! 🚀
