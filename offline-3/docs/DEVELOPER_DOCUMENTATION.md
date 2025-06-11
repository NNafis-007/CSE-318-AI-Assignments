# 📚 Chain Reaction Game - Complete Developer Documentation

## 🎯 **Overview**
This documentation provides a comprehensive guide to understanding every file, class, and method in the Chain Reaction game codebase. Use this to easily add game logic, features, and enhance the UI.

---

## 📁 **Project Architecture Overview**

```
🏗️ Architecture Layers:
├── 🚀 Entry Point (main.py)
├── ⚙️ Configuration Layer (src/config/)
├── 🏗️ Core Architecture (src/core/)
├── 🎨 UI Layer (src/ui/)
└── 📺 Screen Layer (src/screens/)
```

---

## 🔍 **File-by-File Detailed Analysis**

### 🚀 **Entry Point Layer**

#### **`main.py`** - Application Entry Point
```python
"""
🎯 PURPOSE: Clean application startup
🏗️ ARCHITECTURE: Single Responsibility Principle
📝 WHAT IT DOES: Only handles starting the application
"""
```

**Functions:**
- **`main()`**: 
  - **Purpose**: Entry point of the application
  - **What it does**: Creates a Game instance and starts it
  - **When to modify**: Never (unless changing the main class)

**🔧 How to extend**: This file should rarely be modified. All functionality goes in other modules.

---

### ⚙️ **Configuration Layer (`src/config/`)**

#### **`config.py`** - Game Constants & Settings
```python
"""
🎯 PURPOSE: Single source of truth for all game configuration
🏗️ ARCHITECTURE: Centralized configuration management
📝 WHAT IT DOES: Defines all constants used throughout the game
"""
```

**Constants Categories:**

**🖥️ Window Configuration:**
- `WINDOW_WIDTH = 900` - Main window width in pixels
- `WINDOW_HEIGHT = 600` - Main window height in pixels

**📐 Grid Configuration:**
- `GRID_ROWS = 9` - Number of rows in the game board
- `GRID_COLS = 6` - Number of columns in the game board  
- `CELL_SIZE = 60` - Size of each cell in pixels

**🎯 Auto-calculated Positioning:**
- `GRID_WIDTH` - Total grid width (calculated)
- `GRID_HEIGHT` - Total grid height (calculated)
- `GRID_X` - Horizontal center position (calculated)
- `GRID_Y` - Vertical center position (calculated)

**🎨 Color Palette:**
- `WHITE`, `BLACK`, `GRAY` - Basic colors for UI
- `LIGHT_GRAY` - Button backgrounds
- `BLUE`, `LIGHT_BLUE` - Accent colors
- `DARK_GRAY` - Dark UI elements

**⚙️ Game Settings:**
- `FPS = 60` - Target frame rate
- `BUTTON_WIDTH = 200` - Standard button width
- `BUTTON_HEIGHT = 50` - Standard button height

**🔧 How to extend:**
- Add new colors: `NEW_COLOR = (R, G, B)`
- Add game constants: `MAX_PLAYERS = 4`
- Add UI settings: `FONT_SIZE = 24`

#### **`enums.py`** - Type-Safe Enumerations
```python
"""
🎯 PURPOSE: Define type-safe enumerations for game states and modes
🏗️ ARCHITECTURE: Enum pattern for state management
📝 WHAT IT DOES: Provides strongly-typed constants
"""
```

**Classes:**

**`GameState` Enum:**
- `MENU = "menu"` - Main menu state
- `GAME = "game"` - Active gameplay state

**`GameMode` Enum:**
- `TWO_PLAYER = "2 Player"` - Human vs Human mode
- `HUMAN_VS_AI = "Human vs AI"` - Human vs Computer mode
- `AI_VS_AI = "AI vs AI"` - Computer vs Computer mode

**🔧 How to extend:**
```python
# Add new game states
class GameState(Enum):
    MENU = "menu"
    GAME = "game"
    SETTINGS = "settings"      # ← New state
    GAME_OVER = "game_over"    # ← New state

# Add new game modes  
class GameMode(Enum):
    TWO_PLAYER = "2 Player"
    HUMAN_VS_AI = "Human vs AI"
    AI_VS_AI = "AI vs AI"
    TOURNAMENT = "Tournament"   # ← New mode
```

---

### 🏗️ **Core Architecture Layer (`src/core/`)**

#### **`interfaces.py`** - Abstract Base Classes
```python
"""
🎯 PURPOSE: Define contracts and interfaces for polymorphism
🏗️ ARCHITECTURE: Strategy Pattern + Interface Segregation
📝 WHAT IT DOES: Ensures all screens have consistent event handling
"""
```

**Classes:**

**`EventHandler` (Abstract Base Class):**
- **Purpose**: Contract for all screen classes
- **Pattern**: Strategy Pattern for event handling

**Methods:**
- **`handle_mouse_click(pos: tuple[int, int]) -> None`**
  - **Purpose**: Process mouse click events
  - **Parameters**: `pos` - (x, y) coordinates of mouse click
  - **Returns**: Implementation-specific (usually GameMode or str)
  - **When called**: Every time user clicks mouse

- **`handle_key_press(key: int) -> Any`**
  - **Purpose**: Process keyboard events
  - **Parameters**: `key` - pygame key constant (e.g., pygame.K_ESCAPE)
  - **Returns**: Implementation-specific (usually str or None)
  - **When called**: Every time user presses a key

**🔧 How to extend:**
```python
class EventHandler(ABC):
    # ...existing methods...
    
    @abstractmethod
    def handle_mouse_hover(self, pos: tuple[int, int]) -> None:
        """Handle mouse hover events"""
        pass
    
    @abstractmethod
    def handle_mouse_wheel(self, delta: int) -> None:
        """Handle mouse wheel events"""
        pass
```

#### **`game_manager.py`** - Core Game Logic & State Management
```python
"""
🎯 PURPOSE: Central coordination of all game components
🏗️ ARCHITECTURE: State Pattern + Facade Pattern
📝 WHAT IT DOES: Manages state transitions and coordinates all systems
"""
```

**Classes:**

**`GameStateManager` Class:**
- **Purpose**: Manages different game states and transitions
- **Pattern**: State Pattern for clean state management

**Attributes:**
- `current_state: GameState` - Current application state
- `current_mode: Optional[GameMode]` - Selected game mode
- `ui_renderer: UIRenderer` - Shared rendering utility
- `menu_screen: MenuScreen` - Menu screen instance
- `game_screen: Optional[GameScreen]` - Game screen (created on demand)

**Methods:**
- **`__init__()`**
  - **Purpose**: Initialize the state manager
  - **What it does**: Creates shared renderer, menu screen
  - **When called**: Once when game starts

- **`transition_to_game(game_mode: GameMode)`**
  - **Purpose**: Switch from menu to game state
  - **Parameters**: `game_mode` - Selected game mode
  - **What it does**: Creates game screen, changes state
  - **When called**: When user selects a game mode

- **`transition_to_menu()`**
  - **Purpose**: Return to menu from game
  - **What it does**: Destroys game screen, resets state
  - **When called**: When user presses ESC in game

- **`handle_mouse_click(pos: tuple[int, int])`**
  - **Purpose**: Delegate mouse clicks to current screen
  - **Parameters**: `pos` - Mouse click coordinates
  - **What it does**: Routes events based on current state
  - **When called**: Every mouse click

- **`handle_key_press(key: int) -> bool`**
  - **Purpose**: Delegate key presses to current screen
  - **Parameters**: `key` - Pygame key constant
  - **Returns**: True if application should quit
  - **What it does**: Routes keyboard events, handles quit logic
  - **When called**: Every key press

- **`draw(surface: pygame.Surface)`**
  - **Purpose**: Render the current screen
  - **Parameters**: `surface` - Pygame surface to draw on
  - **What it does**: Delegates drawing to current screen
  - **When called**: Every frame

**`Game` Class:**
- **Purpose**: Main game loop and pygame management
- **Pattern**: Facade Pattern + Template Method

**Attributes:**
- `screen: pygame.Surface` - Main display surface
- `clock: pygame.time.Clock` - Frame rate control
- `running: bool` - Game loop control flag
- `state_manager: GameStateManager` - State management system

**Methods:**
- **`__init__()`**
  - **Purpose**: Initialize pygame and game systems
  - **What it does**: Sets up window, creates state manager
  - **When called**: Once when application starts

- **`handle_events()`**
  - **Purpose**: Process all pygame events
  - **What it does**: Handles quit, mouse, keyboard events
  - **When called**: Every frame in game loop

- **`update()`**
  - **Purpose**: Update game logic
  - **What it does**: Currently empty - ready for game logic
  - **When called**: Every frame in game loop
  - **🔧 Extend here**: Add game state updates, AI logic, animations

- **`draw()`**
  - **Purpose**: Render everything to screen
  - **What it does**: Delegates to state manager, flips display
  - **When called**: Every frame in game loop

- **`run()`**
  - **Purpose**: Main game loop
  - **What it does**: Runs handle_events() → update() → draw() loop
  - **When called**: Once from main.py

**🔧 How to extend GameStateManager:**
```python
def transition_to_settings(self):
    """Add settings screen"""
    self.current_state = GameState.SETTINGS
    self.settings_screen = SettingsScreen(self.ui_renderer)

def handle_game_logic_update(self):
    """Add game logic updates"""
    if self.current_state == GameState.GAME and self.game_screen:
        self.game_screen.update_game_logic()
```

---

### 🎨 **UI Layer (`src/ui/`)**

#### **`ui_renderer.py`** - Rendering Utilities
```python
"""
🎯 PURPOSE: Centralized UI rendering functionality  
🏗️ ARCHITECTURE: Utility Class + Builder Pattern
📝 WHAT IT DOES: Handles all drawing operations with consistent styling
"""
```

**Classes:**

**`UIRenderer` Class:**
- **Purpose**: Shared rendering utilities for all screens
- **Pattern**: Utility Pattern with configuration-driven rendering

**Attributes:**
- `font: pygame.font.Font` - Normal text font (36px)
- `title_font: pygame.font.Font` - Title font (48px)  
- `small_font: pygame.font.Font` - Small text font (24px)

**Methods:**
- **`__init__()`**
  - **Purpose**: Initialize font objects
  - **What it does**: Creates different font sizes for UI elements
  - **When called**: Once when UIRenderer is created

- **`draw_button(surface, text, x, y, width, height, bg_color, text_color, border_color, border_width) -> pygame.Rect`**
  - **Purpose**: Draw a customizable button with text
  - **Parameters**:
    - `surface` - Surface to draw on
    - `text` - Button text
    - `x, y` - Button position
    - `width, height` - Button size (defaults from config)
    - `bg_color` - Background color (default: LIGHT_GRAY)
    - `text_color` - Text color (default: BLACK)
    - `border_color` - Border color (default: BLACK)
    - `border_width` - Border thickness (default: 2)
  - **Returns**: pygame.Rect for collision detection
  - **What it does**: Draws button, centers text, returns clickable area
  - **When called**: When rendering buttons

- **`draw_text(surface, text, x, y, font_size, color, center) -> None`**
  - **Purpose**: Draw text with flexible positioning and sizing
  - **Parameters**:
    - `surface` - Surface to draw on
    - `text` - Text to display
    - `x, y` - Text position
    - `font_size` - "title", "normal", or "small"
    - `color` - Text color (default: BLACK)
    - `center` - Whether to center text at position (default: True)
  - **What it does**: Renders text with specified font and positioning
  - **When called**: For all text rendering

- **`draw_grid(surface) -> None`**
  - **Purpose**: Draw the game board grid
  - **Parameters**: `surface` - Surface to draw on
  - **What it does**: Draws 9x6 grid using config constants
  - **When called**: When rendering game screen

**🔧 How to extend UIRenderer:**
```python
def draw_circle(self, surface, color, center, radius):
    """Draw a circle (for game pieces)"""
    pygame.draw.circle(surface, color, center, radius)

def draw_game_piece(self, surface, x, y, count, player_color):
    """Draw a game piece with multiple dots"""
    cell_center = (x + CELL_SIZE//2, y + CELL_SIZE//2)
    for i in range(count):
        offset = i * 5  # Offset for multiple dots
        pygame.draw.circle(surface, player_color, 
                         (cell_center[0] + offset, cell_center[1]), 8)

def draw_player_info(self, surface, player_name, score, color):
    """Draw player information panel"""
    # Implementation for player stats display
```

---

### 📺 **Screen Layer (`src/screens/`)**

#### **`menu_screen.py`** - Main Menu Implementation
```python
"""
🎯 PURPOSE: Handle main menu user interface and logic
🏗️ ARCHITECTURE: Strategy Pattern implementation of EventHandler
📝 WHAT IT DOES: Displays menu, handles mode selection
"""
```

**Classes:**

**`MenuScreen` Class (extends EventHandler):**
- **Purpose**: Main menu screen implementation
- **Pattern**: Strategy Pattern for event handling

**Attributes:**
- `ui_renderer: UIRenderer` - Shared rendering utility (injected)
- `button_rects: dict[GameMode, pygame.Rect]` - Button collision areas
- `selected_mode: Optional[GameMode]` - Currently selected mode

**Methods:**
- **`__init__(ui_renderer: UIRenderer)`**
  - **Purpose**: Initialize menu screen
  - **Parameters**: `ui_renderer` - Shared renderer (dependency injection)
  - **What it does**: Stores renderer, initializes button tracking
  - **When called**: Once when state manager creates menu

- **`handle_mouse_click(pos: tuple[int, int]) -> Optional[GameMode]`**
  - **Purpose**: Process menu button clicks
  - **Parameters**: `pos` - Mouse click coordinates
  - **Returns**: Selected GameMode or None if no button clicked
  - **What it does**: Checks which button was clicked, returns mode
  - **When called**: Every mouse click while in menu

- **`handle_key_press(key: int) -> Optional[str]`**
  - **Purpose**: Process keyboard input in menu
  - **Parameters**: `key` - Pygame key constant
  - **Returns**: "quit" if ESC pressed, None otherwise
  - **What it does**: Handles ESC key for quitting, logs other keys
  - **When called**: Every key press while in menu

- **`draw(surface: pygame.Surface) -> None`**
  - **Purpose**: Render complete menu screen
  - **Parameters**: `surface` - Surface to draw on
  - **What it does**: Draws title, buttons, instructions; updates button_rects
  - **When called**: Every frame while in menu state

**🔧 How to extend MenuScreen:**
```python
def __init__(self, ui_renderer: UIRenderer):
    # ...existing code...
    self.settings_button_rect = None
    self.high_scores_button_rect = None

def handle_mouse_click(self, pos: tuple[int, int]):
    # ...existing code...
    if self.settings_button_rect and self.settings_button_rect.collidepoint(pos):
        return "settings"
    if self.high_scores_button_rect and self.high_scores_button_rect.collidepoint(pos):
        return "high_scores"

def draw(self, surface: pygame.Surface):
    # ...existing code...
    # Add more buttons
    self.settings_button_rect = self.ui_renderer.draw_button(
        surface, "Settings", button_x, 440)
    self.high_scores_button_rect = self.ui_renderer.draw_button(
        surface, "High Scores", button_x, 520)
```

#### **`game_screen.py`** - Game Board Implementation
```python
"""
🎯 PURPOSE: Handle game board display and interaction
🏗️ ARCHITECTURE: Model-View separation with EventHandler
📝 WHAT IT DOES: Displays game board, processes game input
"""
```

**Classes:**

**`GameBoard` Class:**
- **Purpose**: Represents game board state (Model)
- **Pattern**: Model in Model-View-Controller

**Attributes:**
- `rows: int` - Number of board rows
- `cols: int` - Number of board columns  
- `board: list[list[Any]]` - 2D array representing board state

**Methods:**
- **`__init__(rows=GRID_ROWS, cols=GRID_COLS)`**
  - **Purpose**: Initialize empty game board
  - **Parameters**: `rows, cols` - Board dimensions (defaults from config)
  - **What it does**: Creates 2D array filled with None
  - **When called**: When GameScreen is created

- **`is_valid_position(row: int, col: int) -> bool`**
  - **Purpose**: Check if coordinates are within board bounds
  - **Parameters**: `row, col` - Board coordinates
  - **Returns**: True if position is valid
  - **What it does**: Validates coordinates against board size
  - **When called**: Before accessing board positions

- **`get_cell_from_mouse_pos(mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]`**
  - **Purpose**: Convert screen coordinates to board coordinates
  - **Parameters**: `mouse_pos` - (x, y) mouse coordinates
  - **Returns**: (row, col) board coordinates or None if outside grid
  - **What it does**: Calculates which cell was clicked using grid positioning
  - **When called**: When processing mouse clicks on game board

**`GameScreen` Class (extends EventHandler):**
- **Purpose**: Game screen implementation (View + Controller)
- **Pattern**: Strategy Pattern + Model-View-Controller

**Attributes:**
- `ui_renderer: UIRenderer` - Shared rendering utility (injected)
- `game_mode: GameMode` - Current game mode
- `board: GameBoard` - Game board model (composition)

**Methods:**
- **`__init__(ui_renderer: UIRenderer, game_mode: GameMode)`**
  - **Purpose**: Initialize game screen
  - **Parameters**: `ui_renderer` - Shared renderer, `game_mode` - Selected mode
  - **What it does**: Stores dependencies, creates board
  - **When called**: When transitioning from menu to game

- **`handle_mouse_click(pos: tuple[int, int]) -> Optional[str]`**
  - **Purpose**: Process clicks on game board
  - **Parameters**: `pos` - Mouse click coordinates
  - **Returns**: Currently returns None
  - **What it does**: Converts click to board coordinates, logs to console
  - **When called**: Every mouse click while in game

- **`handle_key_press(key: int) -> Optional[str]`**
  - **Purpose**: Process keyboard input during gameplay
  - **Parameters**: `key` - Pygame key constant
  - **Returns**: "back_to_menu" if ESC pressed, None otherwise
  - **What it does**: Handles ESC for returning to menu
  - **When called**: Every key press while in game

- **`draw(surface: pygame.Surface) -> None`**
  - **Purpose**: Render complete game screen
  - **Parameters**: `surface` - Surface to draw on
  - **What it does**: Draws title, grid, instructions
  - **When called**: Every frame while in game state

**🔧 How to extend GameBoard:**
```python
class GameBoard:
    def __init__(self, rows=GRID_ROWS, cols=GRID_COLS):
        # ...existing code...
        self.current_player = 1
        self.players = {1: "Player 1", 2: "Player 2"}
        self.player_colors = {1: BLUE, 2: (255, 0, 0)}  # Red for player 2
    
    def place_piece(self, row: int, col: int, player: int) -> bool:
        """Place a game piece at the specified position"""
        if self.is_valid_position(row, col) and self.board[row][col] is None:
            self.board[row][col] = {"player": player, "count": 1}
            return True
        return False
    
    def get_cell_content(self, row: int, col: int):
        """Get the content of a specific cell"""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def switch_player(self):
        """Switch to the next player"""
        self.current_player = 2 if self.current_player == 1 else 1
```

**🔧 How to extend GameScreen:**
```python
class GameScreen(EventHandler):
    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[str]:
        cell_pos = self.board.get_cell_from_mouse_pos(pos)
        if cell_pos:
            row, col = cell_pos
            # Add actual game logic
            if self.board.place_piece(row, col, self.board.current_player):
                print(f"Player {self.board.current_player} placed piece at ({row}, {col})")
                self.board.switch_player()
            else:
                print("Invalid move!")
        return None
    
    def draw(self, surface: pygame.Surface):
        # ...existing code...
        
        # Draw game pieces
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell_content = self.board.get_cell_content(row, col)
                if cell_content:
                    x = GRID_X + col * CELL_SIZE
                    y = GRID_Y + row * CELL_SIZE
                    player = cell_content["player"]
                    count = cell_content["count"]
                    color = self.board.player_colors[player]
                    self.ui_renderer.draw_game_piece(surface, x, y, count, color)
        
        # Draw current player info
        player_name = self.board.players[self.board.current_player]
        self.ui_renderer.draw_text(surface, f"Current Player: {player_name}", 
                                 WINDOW_WIDTH // 2, 100, "normal")
```

---

## 🎯 **Quick Reference for Adding Features**

### 🎮 **Adding Game Logic**
1. **Extend GameBoard class** in `game_screen.py`:
   - Add game state variables (pieces, scores, turn tracking)
   - Add game logic methods (place piece, check win, etc.)

2. **Extend GameScreen.handle_mouse_click()** in `game_screen.py`:
   - Process player moves
   - Update game state
   - Check win conditions

3. **Extend Game.update()** in `game_manager.py`:
   - Add AI logic
   - Add animations
   - Add timer functionality

### 🎨 **Enhancing UI**
1. **Extend UIRenderer class** in `ui_renderer.py`:
   - Add new drawing methods
   - Add animation support
   - Add visual effects

2. **Extend draw() methods** in screen classes:
   - Add new visual elements
   - Add status displays
   - Add animations

### ⚙️ **Adding New Screens**
1. **Create new enum value** in `enums.py`:
   ```python
   class GameState(Enum):
       SETTINGS = "settings"  # New state
   ```

2. **Create new screen class** in `screens/`:
   ```python
   class SettingsScreen(EventHandler):
       # Implement required methods
   ```

3. **Update GameStateManager** in `game_manager.py`:
   - Add transition methods
   - Add handling in draw() and event methods

### 🤖 **Adding AI Players**
1. **Create AI module** in `src/ai/`:
   ```python
   class AIPlayer:
       def get_move(self, board_state):
           # AI logic here
           return (row, col)
   ```

2. **Integrate with GameScreen**:
   - Add AI turn handling
   - Add difficulty levels
   - Add AI vs AI mode logic

This documentation gives you everything you need to understand and extend the codebase! Each section explains not just what the code does, but how to modify and extend it for your specific needs. 🚀
