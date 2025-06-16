"""
Color constants for Chain Reaction game.
"""

# Player colors
RED = 1
BLUE = 2

# Empty cell
EMPTY = 0

def get_color_name(color):
    """Get human-readable name for a color"""
    if color == RED:
        return "Red"
    elif color == BLUE:
        return "Blue"
    else:
        return "Empty"
