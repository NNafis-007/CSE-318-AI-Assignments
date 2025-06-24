import pygame
import math
from typing import List, Tuple, Optional
from src.config.config import *

class MovingOrb:
    """Represents an orb moving from one cell to another during explosion"""
    
    def __init__(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], 
                 player: int, duration: float = 2):
        """
        Initialize a moving orb animation
        
        Args:
            start_pos: (x, y) screen coordinates of starting position
            end_pos: (x, y) screen coordinates of ending position  
            player: Player number (1 or 2) for color
            duration: Animation duration in seconds
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.player = player
        self.duration = duration
        self.elapsed_time = 0.0
        self.is_complete = False
        
        # Calculate movement vector
        self.dx = end_pos[0] - start_pos[0]
        self.dy = end_pos[1] - start_pos[1]
    
    def update(self, dt: float) -> None:
        """Update animation state"""
        if self.is_complete:
            return
            
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.elapsed_time = self.duration
            self.is_complete = True
    
    def get_current_position(self) -> Tuple[int, int]:
        """Get current position of the moving orb"""
        if self.is_complete:
            return self.end_pos
            
        # Use easing function for smooth movement
        t = self.elapsed_time / self.duration
        # Ease-out cubic for natural deceleration
        eased_t = 1 - (1 - t) ** 3
        
        current_x = self.start_pos[0] + self.dx * eased_t
        current_y = self.start_pos[1] + self.dy * eased_t
        
        return (int(current_x), int(current_y))
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the moving orb"""
        if self.is_complete:
            return
            
        pos = self.get_current_position()
        
        # Choose color based on player
        if self.player == 1:
            orb_color = (255, 0, 0)  # Red for Player 1
        else:
            orb_color = (0, 0, 255)  # Blue for Player 2
        
        # Draw orb with slight glow effect during movement
        orb_radius = 8
        
        # Draw glow effect
        glow_radius = orb_radius + 4
        glow_color = tuple(c // 3 for c in orb_color)  # Darker version for glow
        pygame.draw.circle(surface, glow_color, pos, glow_radius)
        
        # Draw main orb
        pygame.draw.circle(surface, orb_color, pos, orb_radius)
        pygame.draw.circle(surface, BLACK, pos, orb_radius, 2)


class ExplosionEffect:
    """Handles visual effects for cell explosions"""
    
    def __init__(self, center_pos: Tuple[int, int], duration: float = 0.8):
        """
        Initialize explosion effect
        
        Args:
            center_pos: (x, y) screen coordinates of explosion center
            duration: Effect duration in seconds
        """
        self.center_pos = center_pos
        self.duration = duration
        self.elapsed_time = 0.0
        self.is_complete = False
        self.max_radius = 30
    
    def update(self, dt: float) -> None:
        """Update explosion effect"""
        if self.is_complete:
            return
            
        self.elapsed_time += dt
        if self.elapsed_time >= self.duration:
            self.elapsed_time = self.duration
            self.is_complete = True
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw explosion effect"""
        if self.is_complete:
            return
            
        # Calculate current radius and alpha
        t = self.elapsed_time / self.duration
        current_radius = int(self.max_radius * t)
        alpha = int(255 * (1 - t))  # Fade out over time
        
        # Create surface for alpha blending
        explosion_surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        
        # Draw expanding circle with decreasing alpha
        color_with_alpha = (255, 255, 0, alpha)  # Yellow explosion
        pygame.draw.circle(explosion_surface, color_with_alpha, 
                         (current_radius, current_radius), current_radius)
        
        # Blit to main surface
        rect = explosion_surface.get_rect(center=self.center_pos)
        surface.blit(explosion_surface, rect)


class AnimationManager:
    """Manages all animations in the game"""
    
    def __init__(self):
        self.moving_orbs: List[MovingOrb] = []
        self.explosion_effects: List[ExplosionEffect] = []
        self.is_animating = False
    
    def add_moving_orb(self, start_cell: Tuple[int, int], end_cell: Tuple[int, int], 
                      player: int, duration: float = 2.5) -> None:
        """
        Add a moving orb animation
        
        Args:
            start_cell: (row, col) of starting cell
            end_cell: (row, col) of ending cell
            player: Player number
            duration: Animation duration
        """
        # Convert cell coordinates to screen positions
        start_pos = self._cell_to_screen_pos(start_cell)
        end_pos = self._cell_to_screen_pos(end_cell)
        
        orb = MovingOrb(start_pos, end_pos, player, duration)
        self.moving_orbs.append(orb)
        self.is_animating = True
    
    def add_explosion_effect(self, cell: Tuple[int, int], duration: float = 0.8) -> None:
        """
        Add an explosion effect
        
        Args:
            cell: (row, col) of exploding cell
            duration: Effect duration
        """
        center_pos = self._cell_to_screen_pos(cell)
        effect = ExplosionEffect(center_pos, duration)
        self.explosion_effects.append(effect)
        self.is_animating = True
    
    def _cell_to_screen_pos(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Convert cell coordinates to screen position"""
        row, col = cell
        x = GRID_X + col * CELL_SIZE + CELL_SIZE // 2
        y = GRID_Y + row * CELL_SIZE + CELL_SIZE // 2
        return (x, y)
    
    def update(self, dt: float) -> None:
        """Update all animations"""
        # Update moving orbs
        for orb in self.moving_orbs[:]:  # Copy list to avoid modification during iteration
            orb.update(dt)
            if orb.is_complete:
                self.moving_orbs.remove(orb)
        
        # Update explosion effects
        for effect in self.explosion_effects[:]:
            effect.update(dt)
            if effect.is_complete:
                self.explosion_effects.remove(effect)
        
        # Check if any animations are still running
        self.is_animating = len(self.moving_orbs) > 0 or len(self.explosion_effects) > 0
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw all animations"""
        # Draw explosion effects first (behind orbs)
        for effect in self.explosion_effects:
            effect.draw(surface)
        
        # Draw moving orbs on top
        for orb in self.moving_orbs:
            orb.draw(surface)
    
    def clear_all(self) -> None:
        """Clear all animations"""
        self.moving_orbs.clear()
        self.explosion_effects.clear()
        self.is_animating = False
    
    def wait_for_completion(self) -> bool:
        """Check if all animations are complete"""
        return not self.is_animating
