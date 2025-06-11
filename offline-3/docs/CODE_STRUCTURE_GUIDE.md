# 🎮 Chain Reaction Game - Complete Code Structure Guide

## 📁 **New Project Structure**

```
chain_reaction/
├── main.py                  # 🚀 Application entry point
├── requirements.txt         # 📦 Dependencies
├── __init__.py             # 📦 Root package marker
├──
├── src/                    # 📂 Main source code
│   ├── __init__.py
│   ├── config/             # ⚙️ Configuration Layer
│   │   ├── __init__.py
│   │   ├── config.py       # 🔧 Game constants & settings
│   │   └── enums.py        # 📝 Enumerations (GameState, GameMode)
│   │
│   ├── core/               # 🏗️ Core Architecture Layer
│   │   ├── __init__.py
│   │   ├── interfaces.py   # 🎯 Abstract base classes
│   │   └── game_manager.py # 🎮 Main game logic & state management
│   │
│   ├── ui/                 # 🎨 User Interface Layer  
│   │   ├── __init__.py
│   │   └── ui_renderer.py  # 🖼️ UI rendering utilities
│   │
│   └── screens/            # 📺 Screen Implementations
│       ├── __init__.py
│       ├── menu_screen.py  # 📋 Main menu screen
│       └── game_screen.py  # 🎲 Game board screen
│
├── docs/                   # 📚 Documentation
│   └── README.md
│
└── tests/                  # 🧪 Test files
    └── test_structure.py
```

---

## 📋 **Detailed File-by-File Breakdown**

### 🚀 **Entry Point Layer**

#### **`main.py`** - Application Startup
```python
"""
🎯 Purpose: Clean application entry point
🏗️ Architecture: Follows Single Responsibility Principle
📝 Responsibility: Only handles application startup
"""

from src.core.game_manager import Game

def main():
    """Entry point of the application"""
    game = Game()  # Create main game instance
    game.run()     # Start the game loop

if __name__ == "__main__":
    main()
```

**Key Points:**
- ✅ **SRP**: Only responsible for starting the application
- ✅ **Clean**: No business logic, just entry point
- ✅ **Importable**: Can be imported as a module

---

### ⚙️ **Configuration Layer (`src/config/`)**

#### **`config.py`** - Centralized Configuration
```python
"""
🎯 Purpose: Single source of truth for all configuration
🏗️ Architecture: Centralized configuration management
📝 Responsibility: Define all game constants
"""

# Window Configuration
WINDOW_WIDTH = 900          # Main window width
WINDOW_HEIGHT = 600         # Main window height

# Grid Configuration  
GRID_ROWS = 9              # Number of board rows
GRID_COLS = 6              # Number of board columns
CELL_SIZE = 60             # Size of each cell in pixels

# Calculated Grid Positioning (auto-centered)
GRID_WIDTH = GRID_COLS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE
GRID_X = (WINDOW_WIDTH - GRID_WIDTH) // 2   # Center horizontally
GRID_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2 # Center vertically

# Color Palette (RGB tuples)
WHITE = (255, 255, 255)     # Background color
BLACK = (0, 0, 0)           # Text and borders
GRAY = (128, 128, 128)      # Secondary text
LIGHT_GRAY = (192, 192, 192) # Button backgrounds
BLUE = (0, 100, 200)        # Accent color
LIGHT_BLUE = (100, 150, 255) # Light accent
DARK_GRAY = (64, 64, 64)    # Dark elements

# Game Settings
FPS = 60                    # Target frame rate
BUTTON_WIDTH = 200          # Standard button width
BUTTON_HEIGHT = 50          # Standard button height
```

**Benefits:**
- ✅ **DRY Principle**: No magic numbers scattered in code
- ✅ **Easy Maintenance**: Change values in one place
- ✅ **Consistency**: All components use same values
- ✅ **Auto-calculated**: Grid positioning computed automatically

#### **`enums.py`** - Type-Safe Enumerations
```python
"""
🎯 Purpose: Define type-safe enumerations
🏗️ Architecture: Enum pattern for state management
📝 Responsibility: Provide strongly-typed constants
"""

from enum import Enum

class GameState(Enum):
    """Application state machine states"""
    MENU = "menu"           # Main menu state
    GAME = "game"           # Active gameplay state

class GameMode(Enum):
    """Available game modes"""
    TWO_PLAYER = "2 Player"     # Human vs Human
    HUMAN_VS_AI = "Human vs AI" # Human vs Computer
    AI_VS_AI = "AI vs AI"       # Computer vs Computer
```

**Benefits:**
- ✅ **Type Safety**: Prevents invalid states
- ✅ **IDE Support**: Auto-completion and error checking
- ✅ **Maintainable**: Easy to add new modes/states
- ✅ **Readable**: Self-documenting code

---

### 🏗️ **Core Architecture Layer (`src/core/`)**

#### **`interfaces.py`** - Abstract Base Classes
```python
"""
🎯 Purpose: Define contracts and interfaces
🏗️ Architecture: Strategy Pattern + Interface Segregation
📝 Responsibility: Abstract base classes for polymorphism
"""

from abc import ABC, abstractmethod
import pygame
from typing import Any

class EventHandler(ABC):
    """
    Abstract base class for handling events
    Implements Strategy Pattern for event handling
    """
    
    @abstractmethod
    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """Handle mouse click events"""
        pass
    
    @abstractmethod
    def handle_key_press(self, key: int) -> Any:
        """Handle key press events"""
        pass
```

**Design Patterns Applied:**
- ✅ **Strategy Pattern**: Different screens handle events differently
- ✅ **Template Method**: Common interface, specific implementations
- ✅ **Interface Segregation**: Small, focused interface
- ✅ **Dependency Inversion**: High-level modules depend on abstractions

#### **`game_manager.py`** - Core Game Logic
```python
"""
🎯 Purpose: Central game coordination and state management
🏗️ Architecture: State Pattern + Facade Pattern
📝 Responsibility: Orchestrate all game components
"""

class GameStateManager:
    """
    Manages different game states and transitions
    Implements State Pattern for clean state management
    """
    
    def __init__(self):
        self.current_state = GameState.MENU
        self.current_mode = None
        # Dependency Injection: Shared renderer instance
        self.ui_renderer = UIRenderer()
        self.menu_screen = MenuScreen(self.ui_renderer)
        self.game_screen = None  # Lazy loading
    
    def transition_to_game(self, game_mode: GameMode):
        """State transition with mode selection"""
        self.current_mode = game_mode
        self.current_state = GameState.GAME
        # Create game screen on demand
        self.game_screen = GameScreen(self.ui_renderer, game_mode)
    
    def transition_to_menu(self):
        """Return to menu state"""
        self.current_state = GameState.MENU
        self.current_mode = None
        self.game_screen = None  # Clean up resources

class Game:
    """
    Main game class following Facade Pattern
    Provides simple interface to complex subsystem
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chain Reaction Game")
        self.clock = pygame.time.Clock()
        self.running = True
        # Composition: Has-a state manager
        self.state_manager = GameStateManager()
    
    def run(self):
        """Main game loop - Template Method Pattern"""
        while self.running:
            self.handle_events()  # Input
            self.update()         # Logic
            self.draw()          # Render
            self.clock.tick(FPS) # Timing
        
        pygame.quit()
        sys.exit()
```

**Design Patterns:**
- ✅ **State Pattern**: Clean state transitions
- ✅ **Facade Pattern**: Simple interface to complex system
- ✅ **Template Method**: Standard game loop structure
- ✅ **Composition**: Game has-a StateManager

---

### 🎨 **UI Layer (`src/ui/`)**

#### **`ui_renderer.py`** - Rendering Utilities
```python
"""
🎯 Purpose: Centralized UI rendering functionality
🏗️ Architecture: Utility Class + Builder Pattern
📝 Responsibility: Handle all drawing operations
"""

class UIRenderer:
    """
    Handles rendering of UI elements
    Follows Single Responsibility Principle
    """
    
    def __init__(self):
        # Font management
        self.font = pygame.font.Font(None, 36)        # Normal text
        self.title_font = pygame.font.Font(None, 48)  # Titles
        self.small_font = pygame.font.Font(None, 24)  # Small text
    
    def draw_button(self, surface, text, x, y, width=BUTTON_WIDTH, 
                   height=BUTTON_HEIGHT, bg_color=LIGHT_GRAY, 
                   text_color=BLACK, border_color=BLACK, 
                   border_width=2) -> pygame.Rect:
        """
        Flexible button drawing with collision detection
        Returns: pygame.Rect for collision detection
        """
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, bg_color, button_rect)
        pygame.draw.rect(surface, border_color, button_rect, border_width)
        
        # Center text in button
        text_surface = self.font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        
        return button_rect  # Return for collision detection
    
    def draw_text(self, surface, text, x, y, font_size="normal", 
                 color=BLACK, center=True):
        """Flexible text rendering with multiple font sizes"""
        
    def draw_grid(self, surface):
        """Draw the 9x6 game grid using configuration constants"""
```

**Benefits:**
- ✅ **Reusability**: Shared across all screens
- ✅ **Consistency**: Uniform look and feel
- ✅ **Flexibility**: Configurable parameters
- ✅ **Separation**: UI logic separate from game logic

---

### 📺 **Screen Layer (`src/screens/`)**

#### **`menu_screen.py`** - Main Menu Implementation
```python
"""
🎯 Purpose: Handle main menu user interface and logic
🏗️ Architecture: Strategy Pattern implementation
📝 Responsibility: Menu navigation and mode selection
"""

class MenuScreen(EventHandler):
    """
    Implements EventHandler interface for menu functionality
    Follows Strategy Pattern for event handling
    """
    
    def __init__(self, ui_renderer: UIRenderer):
        # Dependency Injection: Receives renderer
        self.ui_renderer = ui_renderer
        self.button_rects = {}  # Store button collision areas
        self.selected_mode = None
    
    def handle_mouse_click(self, pos) -> Optional[GameMode]:
        """
        Process menu button clicks
        Returns: Selected GameMode or None
        """
        for mode, rect in self.button_rects.items():
            if rect.collidepoint(pos):
                self.selected_mode = mode
                print(f"Selected: {mode.value}")
                return mode
        return None
    
    def draw(self, surface):
        """
        Render complete menu screen
        Updates button_rects for collision detection
        """
        surface.fill(WHITE)
        
        # Dynamic button creation and collision area tracking
        button_configs = [
            (GameMode.TWO_PLAYER, 200),
            (GameMode.HUMAN_VS_AI, 280),
            (GameMode.AI_VS_AI, 360)
        ]
        
        self.button_rects.clear()
        for mode, y in button_configs:
            rect = self.ui_renderer.draw_button(surface, mode.value, 
                                              button_x, y)
            self.button_rects[mode] = rect  # Store for collision detection
```

#### **`game_screen.py`** - Game Board Implementation
```python
"""
🎯 Purpose: Handle game board display and interaction
🏗️ Architecture: Model-View separation
📝 Responsibility: Game board rendering and input processing
"""

class GameBoard:
    """
    Represents the game board state (Model)
    Separated from UI for better architecture
    """
    
    def __init__(self, rows=GRID_ROWS, cols=GRID_COLS):
        self.rows = rows
        self.cols = cols
        self.board = [[None for _ in range(cols)] for _ in range(rows)]
    
    def get_cell_from_mouse_pos(self, mouse_pos) -> Optional[Tuple[int, int]]:
        """
        Convert screen coordinates to board coordinates
        Returns: (row, col) tuple or None if outside grid
        """
        mouse_x, mouse_y = mouse_pos
        
        if (GRID_X <= mouse_x <= GRID_X + GRID_WIDTH and
            GRID_Y <= mouse_y <= GRID_Y + GRID_HEIGHT):
            
            col = (mouse_x - GRID_X) // CELL_SIZE
            row = (mouse_y - GRID_Y) // CELL_SIZE
            
            if self.is_valid_position(row, col):
                return (row, col)
        return None

class GameScreen(EventHandler):
    """
    Game screen implementation (View + Controller)
    Handles board display and user interaction
    """
    
    def __init__(self, ui_renderer, game_mode):
        self.ui_renderer = ui_renderer  # Dependency injection
        self.game_mode = game_mode      # Current game mode
        self.board = GameBoard()        # Composition: has-a board
    
    def handle_mouse_click(self, pos):
        """Process clicks on game board"""
        cell_pos = self.board.get_cell_from_mouse_pos(pos)
        if cell_pos:
            row, col = cell_pos
            print(f"Clicked cell: Row {row}, Column {col}")
```

**Architecture Benefits:**
- ✅ **Model-View Separation**: GameBoard separate from GameScreen
- ✅ **Single Responsibility**: Each class has one job
- ✅ **Testability**: Logic can be tested without UI
- ✅ **Reusability**: GameBoard can be used in different contexts

---

## 🎯 **SOLID Principles Applied**

### ✅ **Single Responsibility Principle (SRP)**
- **`UIRenderer`**: Only handles rendering
- **`MenuScreen`**: Only handles menu logic  
- **`GameScreen`**: Only handles game screen logic
- **`GameBoard`**: Only handles board state
- **`GameStateManager`**: Only manages state transitions

### ✅ **Open/Closed Principle (OCP)**
- **EventHandler interface**: Easy to add new screen types
- **GameMode enum**: Easy to add new game modes
- **UIRenderer**: Easy to add new UI elements

### ✅ **Liskov Substitution Principle (LSP)**
- **All screens implement EventHandler**: Can be used interchangeably
- **Polymorphic event handling**: Any EventHandler can process events

### ✅ **Interface Segregation Principle (ISP)**
- **Small, focused interfaces**: EventHandler only has necessary methods
- **No fat interfaces**: Classes only implement what they need

### ✅ **Dependency Inversion Principle (DIP)**
- **High-level modules depend on abstractions**: GameStateManager uses EventHandler interface
- **Dependency injection**: Components receive dependencies rather than creating them

---

## 🚀 **How to Run the Refactored Project**

```bash
# Navigate to project directory
cd "d:\buet classes\CSE 318 AI Lab\offline-3"

# Activate virtual environment (if using one)
chain_reaction\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

---

## 🔧 **Adding New Features**

### Adding a New Screen:
1. Create class inheriting from `EventHandler`
2. Implement required methods
3. Add to `GameStateManager`

### Adding a New Game Mode:
1. Add to `GameMode` enum in `enums.py`
2. Update menu screen button configuration
3. Handle new mode in game logic

### Adding New UI Elements:
1. Add methods to `UIRenderer`
2. Use in screen implementations
3. Update configuration if needed

This structure provides a solid foundation for building a complete Chain Reaction game while maintaining professional code organization and following industry best practices! 🎮✨
