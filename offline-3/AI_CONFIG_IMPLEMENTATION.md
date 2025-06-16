# AI Configuration Menu - Implementation Guide

## Overview
Added difficulty and heuristic selection options to the Human vs AI game mode without creating separate screens. The implementation uses a submenu approach within the existing menu system.

## New Features

### 1. AI Difficulty Levels
- **Easy**: Depth 3 - Quick decisions, suitable for beginners
- **Medium**: Depth 4 - Balanced performance and challenge (default)
- **Hard**: Depth 6 - Deep analysis, challenging gameplay

### 2. AI Heuristic Options
- **Basic**: Standard evaluation function
- **Orb Count**: Focuses on orb count differences
- **Edge Corner**: Prioritizes edge and corner control
- **Vulnerability**: Considers cell vulnerability
- **Chain Reaction**: Evaluates chain reaction opportunities

## Implementation Details

### Modified Files

#### 1. `src/config/enums.py`
- Added `AIDifficulty` enum with display names and depth values
- Added `AIHeuristic` enum with display names and internal keys
- Added `GameState.AI_CONFIG` for future extensibility

#### 2. `src/screens/menu_screen.py`
- Added submenu functionality for AI configuration
- Enhanced `handle_mouse_click()` to return tuple with game settings
- Added `_draw_ai_config_screen()` method for the configuration interface
- Added state management for difficulty and heuristic selection

#### 3. `src/core/game_manager.py`
- Updated `transition_to_game()` to accept AI configuration parameters
- Modified event handling to process the new menu return format

#### 4. `src/screens/game_screen.py`
- Updated constructor to accept `AIDifficulty` and `AIHeuristic` parameters
- Modified AI initialization to use the selected difficulty and heuristic

## User Experience

### Menu Flow
1. User clicks "Human vs AI" from main menu
2. AI Configuration screen appears with two columns:
   - Left: Difficulty selection (Easy/Medium/Hard)
   - Right: Heuristic selection (5 options)
3. Selected options are highlighted in blue
4. User can click "Back" to return to main menu
5. User clicks "Start Game" to begin with selected settings

### Visual Indicators
- Selected difficulty/heuristic buttons appear with blue background
- Current selection is displayed at the bottom of the config screen
- Clear labels show depth values for each difficulty level

## Technical Benefits

### 1. No Additional Screens
- Reused existing menu screen class
- Simple state management with boolean flag
- Maintains single responsibility principle

### 2. Extensible Design
- Easy to add new difficulty levels or heuristics
- Enum-based configuration for type safety
- Clean separation of display and logic concerns

### 3. Backward Compatibility
- Other game modes (2 Player, AI vs AI) work unchanged
- Default settings ensure graceful fallback
- Non-breaking changes to existing interfaces

## Testing

Run `test_menu.py` to verify enum functionality:
```bash
python test_menu.py
```

Expected output shows all difficulty levels and heuristics with their associated values.

## Future Enhancements

### Potential Additions
1. Save user preferences
2. Add more difficulty levels
3. Implement custom heuristic combinations
4. Add tooltips explaining each heuristic
5. Preview mode to see AI behavior differences

### Code Structure
The modular design makes it easy to:
- Add new AI algorithms
- Implement difficulty scaling
- Create tournament modes
- Add AI vs AI configuration
