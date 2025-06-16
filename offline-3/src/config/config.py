
GRID_ROWS = 9 # ← Change this for different number of rows
GRID_COLS = 6  # ← Change this for different number of columns

# ======================================================

# Window configuration (auto-adjusts to grid size)
BASE_CELL_SIZE = 65
MIN_CELL_SIZE = 40
MAX_CELL_SIZE = 80

# Calculate optimal cell size based on grid dimensions
def calculate_cell_size():
    max_width_for_cells = 800  # Reserve space for UI
    max_height_for_cells = 600
    
    width_based_size = max_width_for_cells // GRID_COLS
    height_based_size = max_height_for_cells // GRID_ROWS
    
    optimal_size = min(width_based_size, height_based_size, MAX_CELL_SIZE)
    return max(optimal_size, MIN_CELL_SIZE)

CELL_SIZE = calculate_cell_size()
GRID_WIDTH = GRID_COLS * CELL_SIZE
GRID_HEIGHT = GRID_ROWS * CELL_SIZE

# Window size adapts to grid
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 700
WINDOW_WIDTH = max(GRID_WIDTH + 300, MIN_WINDOW_WIDTH)  # Extra space for UI
WINDOW_HEIGHT = max(GRID_HEIGHT + 150, MIN_WINDOW_HEIGHT)  # Extra space for UI

GRID_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
BLUE = (0, 100, 200)
LIGHT_BLUE = (100, 150, 255)
DARK_GRAY = (64, 64, 64)

# Game settings
FPS = 60
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
TIME_LIMIT = 10 # Time limit for each AI turn in seconds
