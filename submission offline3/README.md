# Chain Reaction Game

A sophisticated implementation of the Chain Reaction game with AI opponents featuring multiple difficulty levels and heuristic strategies.

## Overview

Chain Reaction is a strategic board game where players place orbs on a grid to trigger explosive chain reactions. The goal is to eliminate all opponent orbs by strategically causing chain reactions that convert enemy cells to your color.

## Game Mechanics

- **Grid**: Configurable grid size (default 3x3, supports up to 9x6)
- **Players**: 2 players (Red and Blue)
- **Critical Mass**: 
  - Corner cells: 2 orbs
  - Edge cells: 3 orbs  
  - Center cells: 4 orbs
- **Chain Reactions**: When a cell reaches critical mass, it explodes and distributes orbs to adjacent cells
- **Victory**: Eliminate all opponent orbs from the board

## Features

### Game Modes
1. **Two Player**: Human vs Human
2. **Human vs AI**: Play against computer with configurable difficulty and strategy
3. **AI vs AI**: Watch AI opponents battle each other

### AI Difficulty Levels
- **Easy** (Depth 3): Quick decisions, suitable for beginners
- **Medium** (Depth 4): Balanced performance and challenge
- **Hard** (Depth 6): Deep analysis, challenging gameplay

### AI Heuristic Strategies
1. **Weighted Combined**: Balanced approach (1×positional + 2×strategic)
2. **Orb Count**: Focuses on orb count advantage
3. **Edge Corner**: Prioritizes board position control
4. **Strategic**: Advanced multi-factor evaluation
5. **Chain Reaction**: Emphasizes chain reaction opportunities

## Installation & Setup

### Prerequisites
- Python 3.8+
- pygame 2.5.2+

### Installation
```bash
# Clone or download the project
cd chain-reaction-game

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Configuration
Edit `src/config/config.py` to customize:
- Grid size (GRID_ROWS, GRID_COLS)
- Window dimensions
- Visual settings
- Game parameters

## How to Play

### Starting the Game
1. Run `python main.py`
2. Select game mode from the main menu
3. For Human vs AI, configure difficulty and heuristic
4. Click "Start Game"

### Gameplay
1. **Placing Orbs**: Click on any empty cell or cell you own
2. **Chain Reactions**: Watch explosions trigger automatically
3. **Turn System**: Alternates between players after each move
4. **Winning**: Eliminate all opponent orbs

### Controls
- **Mouse**: Click cells to place orbs
- **ESC**: Return to menu or quit
- **Visual Feedback**: 
  - Cell info displays on hover
  - Animation shows chain reactions
  - Player indicators show current turn

## Technical Architecture

### Core Components
- **GameBoard**: Manages game state and logic
- **Cell**: Represents individual board cells
- **AI System**: Minimax algorithm with alpha-beta pruning
- **UI System**: Pygame-based rendering and interaction
- **Animation**: Smooth visual effects for chain reactions

### AI Implementation
- **Algorithm**: Minimax with alpha-beta pruning
- **Heuristics**: Multiple evaluation strategies
- **Performance**: Configurable depth for different difficulty levels
- **Optimization**: Efficient move generation and board evaluation

### Project Structure
```
chain-reaction-game/
├── main.py                 # Entry point
├── Board.py                # Core game board logic
├── utils.py                # Game utilities and heuristics
├── minmax.py               # AI minimax algorithm
├── colors.py               # Color constants
├── requirements.txt        # Dependencies
├── src/
│   ├── config/             # Configuration files
│   ├── core/               # Core game logic
│   ├── screens/            # UI screens
│   └── ui/                 # UI components
└── tests/                  # Test files
```

## AI Heuristics Explained

### Weighted Combined (Default)
Combines positional strategy with strategic evaluation:
- 1× Edge/Corner control score
- 2× Strategic evaluation score

### Strategic Evaluation
Advanced heuristic considering:
- Win/loss states (±10000 points)
- Vulnerability to enemy attacks
- Positional bonuses (corners +3, edges +2)
- Critical cell advantages
- Contiguous critical block bonuses

### Orb Count Difference
Simple strategy focusing on:
- Total orb count advantage
- Basic material evaluation

### Edge Corner Control
Positional strategy emphasizing:
- Corner cell control (+3 points)
- Edge cell control (+2 points)
- Board position advantages

### Chain Reaction Opportunities
Tactical strategy prioritizing:
- Potential chain reaction setups
- Enemy vulnerability exploitation
- Explosive combination creation

## Customization

### Adding New Heuristics
1. Implement heuristic function in `utils.py`
2. Add mapping in `src/core/ai_player.py`
3. Add enum entry in `src/config/enums.py`
4. Test the new strategy

### Modifying Game Rules
- Edit `Board.py` for core game mechanics
- Modify `utils.py` for move validation
- Update `src/config/config.py` for visual settings

### Extending AI
- Adjust minimax depth in difficulty settings
- Implement new search algorithms
- Add learning capabilities

## Performance Notes

- **Grid Size**: Larger grids exponentially increase AI computation time
- **Difficulty**: Higher depths provide better play but slower response
- **Optimization**: Alpha-beta pruning significantly improves performance
- **Memory**: Efficient board copying minimizes memory usage

## Development

### Code Style
- Type hints for better code clarity
- Modular design for easy maintenance
- Comprehensive documentation
- Clean separation of concerns

### Testing
Run tests with:
```bash
python tests/test_structure.py
```

### Contributing
1. Follow existing code style
2. Add type hints for new functions
3. Update documentation for new features
4. Test thoroughly before submitting

## Troubleshooting

### Common Issues
- **Import Errors**: Ensure Python path includes project root
- **Pygame Issues**: Verify pygame installation
- **Performance**: Reduce AI depth for faster gameplay
- **Display**: Check window size configuration

### Debugging
- Enable debug prints in AI modules
- Use test files for isolated testing
- Check configuration values
- Verify game state integrity

## Credits

- **Core Game Logic**: Chain Reaction mechanics implementation
- **AI System**: Minimax with alpha-beta pruning
- **UI Framework**: Pygame-based interface
- **Architecture**: Modular design pattern

## License

Educational project for AI and game development learning.

---

**Enjoy playing Chain Reaction!** 🎮
