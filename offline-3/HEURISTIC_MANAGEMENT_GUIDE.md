# Heuristic Management Guide

## Recent Changes

### Latest Update: Weighted Combined Heuristic
- **Removed**: `heuristic()` basic function from `utils.py`
- **Added**: `heuristic_weighted_combined()` function that combines:
  - 1 × `heuristic_edge_corner_control()`
  - 2 × `heuristic_strategic_evaluation()`
- **Updated**: Default heuristic in AI player and menu to `weighted_combined`
- **Updated**: All references from 'basic' to 'weighted_combined' in:
  - `src/core/ai_player.py` - Default parameter and mapping
  - `src/core/game_manager.py` - Default parameter
  - `src/screens/game_screen.py` - Default parameter
  - `src/screens/menu_screen.py` - Default selection
  - `src/config/enums.py` - Enum definition
- **Verified**: No remaining BASIC/basic references in source code

## Summary of Changes Made

### Implemented Strategic Heuristic
- **Location**: `utils.py`
- **Function**: `heuristic_strategic_evaluation(state: Board.Board, player)`
- **Features**:
  - Win/Loss detection: ±10000 points
  - Vulnerability analysis: -5 + critical_mass for each critical enemy
  - Safe orb bonuses: +2 (edge), +3 (corner), +2 (critical)
  - Orb count bonus: +1 per orb
  - Critical block analysis: +2 × block_size for contiguous critical blocks

### Removed Vulnerability Heuristic
- **Removed**: `heuristic_vulnerability()` function from `utils.py`
- **Updated**: AI player mapping to exclude vulnerability option
- **Updated**: Menu enum to replace vulnerability with strategic

## Files to Modify When Adding/Removing Heuristics

### 1. Core Heuristic Implementation
**File**: `utils.py`
- **Add**: Implement new heuristic function following the pattern:
  ```python
  def heuristic_your_name(state: Board.Board, player):
      # Implementation here
      # Return positive score for advantage, negative for disadvantage
      # Use player==colors.RED check for perspective
      return score if player == colors.RED else -score
  ```
- **Remove**: Delete the heuristic function

### 2. AI Player Mapping
**File**: `src/core/ai_player.py`
- **Location**: `_get_heuristic_function()` method
- **Add**: Add entry to `heuristic_map` dictionary:
  ```python
  'your_key': utils.heuristic_your_name,
  ```
- **Remove**: Remove the entry from `heuristic_map`

### 3. Menu Configuration
**File**: `src/config/enums.py`
- **Location**: `AIHeuristic` enum class
- **Add**: Add new enum entry:
  ```python
  YOUR_NAME = ("Display Name", "your_key")
  ```
- **Remove**: Remove the enum entry

### 4. Optional: Documentation Updates
**Files**: 
- `AI_CONFIG_IMPLEMENTATION.md`
- `README.md` (if exists)
- Test files

## Template for New Heuristic

### Step 1: Implement in utils.py
```python
def heuristic_my_strategy(state: Board.Board, player):
    """
    Description of your heuristic strategy
    """
    player_num = 1 if player == colors.RED else 2
    score = 0
    
    # Your evaluation logic here
    for i in range(state.rows):
        for j in range(state.cols):
            cell = state.grid[i][j]
            if cell.player == player_num:
                # Add scoring logic
                pass
    
    return score if player == colors.RED else -score
```

### Step 2: Add to AI Player (src/core/ai_player.py)
```python
def _get_heuristic_function(self, heuristic_name):
    heuristic_map = {
        'weighted_combined': utils.heuristic_weighted_combined,
        'orb_count': utils.heuristic_orb_count_diff,
        'edge_corner': utils.heuristic_edge_corner_control,
        'strategic': utils.heuristic_strategic_evaluation,
        'chain_reaction': utils.heuristic_chain_reaction_opportunity,
        'my_strategy': utils.heuristic_my_strategy,  # ADD THIS LINE
    }
    return heuristic_map.get(heuristic_name, utils.heuristic_weighted_combined)
```

### Step 3: Add to Menu (src/config/enums.py)
```python
class AIHeuristic(Enum):
    WEIGHTED_COMBINED = ("Weighted Combined", "weighted_combined")
    ORB_COUNT = ("Orb Count", "orb_count")
    EDGE_CORNER = ("Edge Corner", "edge_corner")
    STRATEGIC = ("Strategic", "strategic")
    CHAIN_REACTION = ("Chain Reaction", "chain_reaction")
    MY_STRATEGY = ("My Strategy", "my_strategy")  # ADD THIS LINE
    
    def __init__(self, display_name, key):
        self.display_name = display_name
        self.key = key
```

## Current Available Heuristics

1. **Weighted Combined** (`weighted_combined`) - Combination of 1×edge_corner + 2×strategic (DEFAULT)
2. **Orb Count** (`orb_count`) - Simple orb count difference  
3. **Edge Corner** (`edge_corner`) - Positional strategy favoring edges/corners
4. **Strategic** (`strategic`) - Advanced multi-factor evaluation
5. **Chain Reaction** (`chain_reaction`) - Focuses on chain reaction opportunities

## Testing Your Heuristic

Create a test file to verify your heuristic:
```python
import Board
import utils
import colors

def test_my_heuristic():
    board = Board.Board(3, 3)
    # Set up test scenarios
    score = utils.heuristic_my_strategy(board, colors.RED)
    print(f"Heuristic score: {score}")

test_my_heuristic()
```

## Important Notes

1. **Consistent Perspective**: Always return positive scores for the specified player's advantage
2. **Terminal States**: Consider checking for win/loss conditions first
3. **Performance**: Avoid expensive computations for deep search trees
4. **Testing**: Create test scenarios to verify your heuristic behaves as expected
5. **Enum Ordering**: Add new heuristics at the end to maintain backward compatibility

## Verification Checklist

When adding/removing heuristics:
- [ ] Implemented/removed function in `utils.py`
- [ ] Updated mapping in `src/core/ai_player.py`
- [ ] Updated enum in `src/config/enums.py`
- [ ] Tested with simple board scenarios
- [ ] Verified menu shows correct options
- [ ] Confirmed AI uses the heuristic in game
