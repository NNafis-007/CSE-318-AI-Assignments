"""
Enhanced Animation system for Chain Reaction game.
Handles visual effects like explosions and moving orbs.
Completely separated from game logic.
"""

import pygame
from typing import List, Dict, Tuple, Optional
import time
import math


class Animation:
    """Base class for animations"""
    
    def __init__(self, duration: float):
        self.duration = duration
        self.start_time = time.time()
        self.completed = False
    
    def get_progress(self) -> float:
        """Get animation progress from 0.0 to 1.0"""
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        if progress >= 1.0:
            self.completed = True
        return progress
    
    def is_completed(self) -> bool:
        """Check if animation is completed"""
        return self.completed
    
    def update(self, dt: float) -> None:
        """Update animation state"""
        pass
    
    def draw(self, surface: pygame.Surface, renderer) -> None:
        """Draw the animation effect"""
        pass


class ExplosionAnimation(Animation):
    """Animation for cell explosions"""
    
    def __init__(self, position: Tuple[int, int], duration: float = 0.5):
        super().__init__(duration)
        self.position = position  # (row, col)
    
    def draw(self, surface: pygame.Surface, renderer) -> None:
        """Draw explosion effect"""
        if not self.completed:
            progress = self.get_progress()
            renderer.draw_explosion_effect(surface, self.position, progress)


class MovingOrbAnimation(Animation):
    """Animation for orbs moving between cells"""
    
    def __init__(self, start_cell: Tuple[int, int], end_cell: Tuple[int, int], 
                 player: int, duration: float = 0.3):
        super().__init__(duration)
        self.start_cell = start_cell  # (row, col)
        self.end_cell = end_cell      # (row, col)
        self.player = player
    
    def draw(self, surface: pygame.Surface, renderer) -> None:
        """Draw moving orb"""
        if not self.completed:
            progress = self.get_progress()
            renderer.draw_moving_orb(surface, self.start_cell, self.end_cell, 
                                   progress, self.player)


class AnimationManager:
    """
    Manages all animations for the game.
    Handles timing, updates, and rendering of visual effects.
    """
    
    def __init__(self):
        self.animations: List[Animation] = []
        self.explosion_effects: List[ExplosionAnimation] = []
        self.moving_orbs: List[MovingOrbAnimation] = []
    
    def add_explosion_effect(self, position: Tuple[int, int], duration: float = 0.5) -> None:
        """Add an explosion animation at the specified cell position"""
        explosion = ExplosionAnimation(position, duration)
        self.animations.append(explosion)
        self.explosion_effects.append(explosion)
    
    def add_moving_orb(self, start_cell: Tuple[int, int], end_cell: Tuple[int, int],
                      player: int, duration: float = 0.3) -> None:
        """Add a moving orb animation between two cells"""
        moving_orb = MovingOrbAnimation(start_cell, end_cell, player, duration)
        self.animations.append(moving_orb)
        self.moving_orbs.append(moving_orb)
    
    def update(self, dt: float) -> None:
        """Update all animations and remove completed ones"""
        # Update all animations
        for animation in self.animations:
            animation.update(dt)
        
        # Remove completed animations
        self.animations = [anim for anim in self.animations if not anim.is_completed()]
        self.explosion_effects = [anim for anim in self.explosion_effects if not anim.is_completed()]
        self.moving_orbs = [anim for anim in self.moving_orbs if not anim.is_completed()]
    
    def draw(self, surface: pygame.Surface, renderer) -> None:
        """Draw all active animations"""
        for animation in self.animations:
            animation.draw(surface, renderer)
    
    def has_active_animations(self) -> bool:
        """Check if there are any active animations"""
        return len(self.animations) > 0
    
    def wait_for_completion(self) -> bool:
        """Check if all animations are completed"""
        return len(self.animations) == 0
    
    def clear_all(self) -> None:
        """Clear all animations"""
        self.animations.clear()
        self.explosion_effects.clear()
        self.moving_orbs.clear()
    
    def get_animation_count(self) -> Dict[str, int]:
        """Get count of different animation types for debugging"""
        return {
            'total': len(self.animations),
            'explosions': len(self.explosion_effects),
            'moving_orbs': len(self.moving_orbs)
        }
