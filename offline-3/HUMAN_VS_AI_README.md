# Human vs AI Implementation for Chain Reaction

## Overview
Successfully implemented a Human vs AI mode for the Chain Reaction game using minimax algorithm with alpha-beta pruning and file-based communication.

## Files Created/Modified

### New Files Created:
1. **`Board.py`** - Game board class compatible with existing Cell structure
2. **`colors.py`** - Color constants (RED=1, BLUE=2, EMPTY=0)
3. **`gamestate_manager.py`** - Handles file I/O for game state communication
4. **`human_vs_ai_complete.py`** - Complete Human vs AI game with file communication
5. **`human_vs_ai_test.py`** - Simple test version of Human vs AI game

### Modified Files:
1. **`utils.py`** - Fixed and completed all heuristic functions and game utilities
2. **`minmax.py`** - Fixed minimax algorithm with proper alpha-beta pruning

## Key Features Implemented

### 1. Minimax Algorithm
- **Algorithm**: Minimax with alpha-beta pruning
- **Depth Control**: Configurable depth (Easy=2, Medium=3, Hard=4)
- **Player Colors**: RED=1, BLUE=2
- **Evaluation**: Multiple heuristic functions available

### 2. Heuristic Functions
- **Basic**: Simple cell count difference
- **Orb Count**: Weighted by number of orbs
- **Edge/Corner Control**: Positional advantage evaluation
- **Vulnerability**: Penalty for near-critical cells
- **Chain Reaction**: Reward for setup opportunities

### 3. File-Based Communication
- **Format**: Exactly as specified in requirements
- **Header**: "Human Move:" or "AI Move:"
- **Board**: 9 rows × 6 columns
- **Cells**: "0" for empty, "<n><C>" for occupied (e.g., "2R", "1B")
- **File**: `gamestate.txt`

### 4. Game Features
- **Load/Save**: Can load existing games from file
- **Human vs AI**: Choose your color and AI difficulty
- **Multiple Heuristics**: Select AI strategy
- **Move Validation**: Ensures legal moves only
- **Game End Detection**: Proper terminal state checking

## Usage Instructions

### Activate Environment:
```powershell
.\chain_reaction\Scripts\Activate.ps1
```

### Run Complete Game:
```bash
python human_vs_ai_complete.py
```

### Run Simple Test:
```bash
python human_vs_ai_test.py
```

### Test Game State Manager:
```bash
python gamestate_manager.py
```

## File Format Example

### gamestate.txt:
```
Human Move:
1R 0 0 0 0 0
0 1B 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

## Integration with Existing Codebase

### Compatibility:
- **Cell Structure**: Uses existing `src/core/cell.py` with `orb_count` and `player` attributes
- **Config**: Uses existing `src/config/config.py` for board dimensions
- **No Conflicts**: All new files are in root directory, no modifications to src/ structure

### Board Mapping:
- **Cell.player**: 1 (Red), 2 (Blue), None (Empty)
- **Cell.orb_count**: Number of orbs in cell
- **Critical Mass**: Calculated automatically based on position

## Testing Completed

✅ **Import Tests**: All modules import successfully
✅ **Board Creation**: Board initialization works
✅ **Move Generation**: Valid moves calculated correctly
✅ **Minimax**: AI finds best moves using minimax
✅ **File I/O**: Game state saves/loads correctly
✅ **Game Flow**: Complete game loop functions

## Next Steps

1. **Integration**: Integrate with your existing GUI in `src/screens/game_screen.py`
2. **Menu Option**: Add "Human vs AI" option to your game menu
3. **Difficulty Settings**: Add UI controls for AI difficulty and heuristic selection
4. **File Monitoring**: Optionally add file watching for external AI components

## Sample Usage

```python
# Create game
game = HumanVsAIGame(colors.RED, difficulty=3, heuristic='orb_count')

# Make human move
game.make_move(0, 0)  # Human plays at (0,0)

# Get AI move
ai_move = game.get_ai_move()  # AI calculates best move
game.make_move(ai_move[0], ai_move[1])  # AI makes move

# All moves automatically saved to gamestate.txt
```

The implementation is ready for integration into your existing game!
