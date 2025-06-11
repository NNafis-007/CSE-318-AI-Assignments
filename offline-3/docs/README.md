# 🎮 Chain Reaction Game

A professionally structured pygame-based game implementation following SOLID principles and Object-Oriented Programming best practices.

## 🚀 **Quick Start**

```bash
# Navigate to project directory
cd "d:\buet classes\CSE 318 AI Lab\offline-3"

# Install dependencies (if not already done)
pip install pygame

# Run the game
python main.py
# OR use the development script
python run_game.py
```

## 🏗️ **Project Architecture**

### **📁 Folder Structure**
```
chain_reaction/
├── 🚀 main.py                 # Application entry point
├── 🔧 run_game.py             # Development run script
├── 📦 requirements.txt        # Dependencies
├── 📦 __init__.py            # Root package
│
├── 📂 src/                   # Main source code
│   ├── ⚙️ config/            # Configuration layer
│   │   ├── config.py         # Constants & settings
│   │   └── enums.py          # Game states & modes
│   │
│   ├── 🏗️ core/              # Architecture layer
│   │   ├── interfaces.py     # Abstract base classes
│   │   └── game_manager.py   # Core game logic
│   │
│   ├── 🎨 ui/                # User interface layer
│   │   └── ui_renderer.py    # Rendering utilities
│   │
│   └── 📺 screens/           # Screen implementations
│       ├── menu_screen.py    # Main menu
│       └── game_screen.py    # Game board
│
├── 📚 docs/                  # Documentation
│   ├── README.md            # This file
│   └── CODE_STRUCTURE_GUIDE.md  # Detailed code guide
│
└── 🧪 tests/                # Test files
    └── test_structure.py    # Structure validation
```

## 🎯 **SOLID Principles Applied**

| Principle | Implementation | Benefits |
|-----------|---------------|----------|
| **Single Responsibility** | Each class has one job | Easy to maintain & test |
| **Open/Closed** | Interface-based design | Easy to extend features |
| **Liskov Substitution** | Polymorphic screen handling | Consistent behavior |
| **Interface Segregation** | Small, focused interfaces | Clean dependencies |
| **Dependency Inversion** | Abstract dependencies | Flexible architecture |

## 🎮 **Game Features**

### **Menu System**
- 🎯 **2 Player Mode**: Human vs Human
- 🤖 **Human vs AI**: Human vs Computer
- 🔄 **AI vs AI**: Computer vs Computer

### **Game Board**
- 📐 **9x6 Grid**: Interactive game board
- 🖱️ **Click Detection**: Responsive cell selection
- 📍 **Coordinate Display**: Console logging of clicked cells
- ⌨️ **Keyboard Controls**: ESC for navigation

## 🔧 **Technical Highlights**

### **Design Patterns Used**
- 🎯 **Strategy Pattern**: Event handling
- 🔄 **State Pattern**: Game state management
- 🏗️ **Facade Pattern**: Simplified game interface
- 🧩 **Template Method**: Game loop structure
- 💉 **Dependency Injection**: Component composition

### **Code Quality Features**
- ✅ **Type Hints**: Full type annotation
- 📝 **Documentation**: Comprehensive docstrings
- 🧪 **Error Handling**: Robust error management
- 🔧 **Configuration**: Centralized settings
- 📦 **Modular Design**: Reusable components

## 🛠️ **Development Guide**

### **Adding New Features**

#### 🆕 New Screen Type:
```python
# 1. Create new screen class
class NewScreen(EventHandler):
    def handle_mouse_click(self, pos): pass
    def handle_key_press(self, key): pass
    def draw(self, surface): pass

# 2. Add to GameStateManager
# 3. Update state transitions
```

#### 🎮 New Game Mode:
```python
# 1. Add to GameMode enum
class GameMode(Enum):
    NEW_MODE = "New Mode"

# 2. Update menu configuration
# 3. Handle in game logic
```

#### 🎨 New UI Element:
```python
# 1. Add method to UIRenderer
def draw_new_element(self, surface, ...):
    # Implementation here
    
# 2. Use in screen classes
# 3. Update configuration if needed
```

## 🎯 **Learning Objectives Achieved**

### **Object-Oriented Programming**
- ✅ **Encapsulation**: Data and methods grouped logically
- ✅ **Inheritance**: EventHandler base class
- ✅ **Polymorphism**: Screen-specific event handling
- ✅ **Composition**: Component relationships

### **Software Engineering Principles**
- ✅ **Separation of Concerns**: Clear layer boundaries
- ✅ **Don't Repeat Yourself (DRY)**: Centralized configuration
- ✅ **Keep It Simple, Stupid (KISS)**: Clean, readable code
- ✅ **You Aren't Gonna Need It (YAGNI)**: Focused implementation

## 🔍 **Code Navigation Guide**

### **🚀 Starting Point**: `main.py`
```python
from src.core.game_manager import Game
# Clean entry point with single responsibility
```

### **⚙️ Configuration**: `src/config/`
- 📐 **Dimensions & Layout**: Window size, grid configuration
- 🎨 **Visual Settings**: Colors, fonts, UI elements
- 📝 **Game Constants**: FPS, button sizes

### **🏗️ Core Logic**: `src/core/`
- 🎯 **Interfaces**: Abstract base classes for consistency
- 🔄 **State Management**: Game state transitions
- 🎮 **Main Loop**: Event handling and rendering coordination

### **🎨 UI Components**: `src/ui/`
- 🖼️ **Rendering**: Centralized drawing utilities
- 🎯 **Consistency**: Uniform UI elements
- 🔧 **Flexibility**: Configurable visual components

### **📺 Screen Logic**: `src/screens/`
- 📋 **Menu**: Game mode selection interface
- 🎲 **Game Board**: Interactive grid and gameplay
- ⌨️ **Input Handling**: Mouse and keyboard events

## 🧪 **Testing**

```bash
# Test the modular structure
python tests/test_structure.py

# Run with development script (better error reporting)
python run_game.py
```

## 📚 **Additional Resources**

- 📖 **Detailed Code Guide**: `docs/CODE_STRUCTURE_GUIDE.md`
- 🧪 **Test Files**: `tests/`
- 📦 **Dependencies**: `requirements.txt`

---

**🎮 Ready to explore and extend the codebase!** Each component is designed to be independently understandable while working together as a cohesive system. The structure supports easy maintenance, testing, and feature addition following industry best practices.
