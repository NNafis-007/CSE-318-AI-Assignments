# Chain Reaction - Configuration Guide

## 🎮 How to Change Grid Size

To play with different grid sizes, simply modify these values in `src/config/config.py`:

```python
GRID_ROWS = 9  # ← Change this for different number of rows
GRID_COLS = 6  # ← Change this for different number of columns
```

### 📐 Recommended Grid Sizes:

#### Standard Sizes:
- **Classic**: `GRID_ROWS = 9, GRID_COLS = 6` (original Chain Reaction)
- **Small**: `GRID_ROWS = 6, GRID_COLS = 4` (faster games)
- **Large**: `GRID_ROWS = 12, GRID_COLS = 8` (longer games)
- **Square**: `GRID_ROWS = 8, GRID_COLS = 8` (symmetric gameplay)

#### Fun Variations:
- **Narrow**: `GRID_ROWS = 10, GRID_COLS = 3` (vertical strategy)
- **Wide**: `GRID_ROWS = 4, GRID_COLS = 10` (horizontal strategy)
- **Tiny**: `GRID_ROWS = 4, GRID_COLS = 3` (quick games)
- **Huge**: `GRID_ROWS = 15, GRID_COLS = 10` (epic battles)

## 🔧 What Happens When You Change Grid Size:

### ✅ Automatic Adjustments:
- **Window size** adapts to fit the grid
- **Cell size** scales appropriately (40-80 pixels)
- **Critical mass** calculated correctly for each position
- **AI heuristics** work with any grid size
- **Game logic** supports any rectangular grid
- **File format** adapts to save any size grid

### 🎯 Game Balance:
- **Smaller grids**: Faster, more tactical games
- **Larger grids**: Longer, more strategic games
- **Square grids**: Symmetric gameplay
- **Rectangular grids**: Different strategic dynamics

## 📝 Examples:

### For Quick Games (Small Grid):
```python
GRID_ROWS = 6
GRID_COLS = 4
```

### For Epic Battles (Large Grid):
```python
GRID_ROWS = 12
GRID_COLS = 8
```

### For Symmetric Games (Square Grid):
```python
GRID_ROWS = 8
GRID_COLS = 8
```

## 💡 Tips:
- **Minimum recommended**: 3x3 grid
- **Maximum recommended**: 20x15 grid (for performance)
- **Odd numbers** often work better for symmetric gameplay
- **Test different sizes** to find your preferred gameplay style

## 🚀 How to Apply:
1. Edit `src/config/config.py`
2. Change `GRID_ROWS` and `GRID_COLS` values
3. Save the file
4. Run `python main.py`
5. Enjoy your custom grid size!

The game will automatically adapt all features to your chosen grid size! 🎉
