"""
Game renderer for Chain Reaction - handles all visual representation.
Completely separated from game logic, only receives data to render.
"""

import pygame
import math
from typing import Dict, List, Tuple, Optional
from src.config.config import *
from src.core.game_logic import GameState


class GameRenderer:
    """
    Handles all visual rendering for the Chain Reaction game.
    Contains no game logic - only receives state data and renders it.
    """
    
    def __init__(self):
        # Rendering configuration
        self.grid_x = GRID_X
        self.grid_y = GRID_Y
        self.cell_size = CELL_SIZE
        self.rows = GRID_ROWS
        self.cols = GRID_COLS
        
        # Colors for rendering
        self.colors = {
            'background': WHITE,
            'grid_line': BLACK,
            'cell_empty': WHITE,
            'cell_hover': (240, 240, 240),
            'player1': (255, 50, 50),    # Red for Player 1
            'player2': (50, 50, 255),    # Blue for Player 2
            'text_dark': BLACK,
            'text_light': WHITE,
            'critical_border': (255, 215, 0),  # Gold for critical cells
        }
        
        # Fonts for text rendering
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
        self.font_title = pygame.font.Font(None, 48)
        
        # Animation state (for visual effects only)
        self.animation_time = 0.0
        
    def update_animation_time(self, dt: float):
        """Update animation timer for visual effects"""
        self.animation_time += dt
    
    def draw_game_screen(self, surface: pygame.Surface, game_state: GameState, 
                        hover_cell: Optional[Tuple[int, int]] = None,
                        selected_cell: Optional[Tuple[int, int]] = None) -> None:
        """
        Draw the complete game screen including grid, orbs, and UI elements.
        
        Args:
            surface: Pygame surface to draw on
            game_state: Current game state containing all game data
            hover_cell: Cell being hovered by mouse (row, col) or None
            selected_cell: Currently selected cell (row, col) or None
        """
        # Clear background
        surface.fill(self.colors['background'])
        
        # Draw the game grid
        self._draw_grid(surface, hover_cell, selected_cell)
        
        # Draw orbs in cells
        self._draw_orbs(surface, game_state)
        
        # Draw game information
        self._draw_game_info(surface, game_state)
        
        # Draw instructions
        self._draw_instructions(surface)
    
    def _draw_grid(self, surface: pygame.Surface, 
                   hover_cell: Optional[Tuple[int, int]] = None,
                   selected_cell: Optional[Tuple[int, int]] = None) -> None:
        """Draw the game grid with optional hover and selection highlights"""
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.grid_x + col * self.cell_size
                y = self.grid_y + row * self.cell_size
                
                # Determine cell color
                cell_color = self.colors['cell_empty']
                if hover_cell and hover_cell == (row, col):
                    cell_color = self.colors['cell_hover']
                
                # Draw cell
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, cell_color, cell_rect)
                pygame.draw.rect(surface, self.colors['grid_line'], cell_rect, 1)
                
                # Draw selection highlight
                if selected_cell and selected_cell == (row, col):
                    pygame.draw.rect(surface, self.colors['critical_border'], cell_rect, 3)
    
    def _draw_orbs(self, surface: pygame.Surface, game_state: GameState) -> None:
        """Draw orbs in all cells based on current game state"""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = game_state.get_cell(row, col)
                if cell and not cell.is_empty():
                    self._draw_cell_orbs(surface, cell, row, col)
    
    def _draw_cell_orbs(self, surface: pygame.Surface, cell, row: int, col: int) -> None:
        """Draw orbs for a specific cell"""
        # Calculate cell center
        cell_x = self.grid_x + col * self.cell_size + self.cell_size // 2
        cell_y = self.grid_y + row * self.cell_size + self.cell_size // 2
        
        # Choose player color
        if cell.player == 1:
            orb_color = self.colors['player1']
            text_color = (200, 0, 0)
        else:
            orb_color = self.colors['player2']
            text_color = (0, 0, 200)
        
        orb_radius = 8
        
        # Draw orbs based on count in appropriate patterns
        if cell.orb_count == 1:
            self._draw_orb_with_glow(surface, orb_color, (cell_x, cell_y), orb_radius)
            
        elif cell.orb_count == 2:
            self._draw_orb_with_glow(surface, orb_color, (cell_x - 10, cell_y), orb_radius)
            self._draw_orb_with_glow(surface, orb_color, (cell_x + 10, cell_y), orb_radius)
            
        elif cell.orb_count == 3:
            self._draw_orb_with_glow(surface, orb_color, (cell_x, cell_y - 10), orb_radius)
            self._draw_orb_with_glow(surface, orb_color, (cell_x - 10, cell_y + 5), orb_radius)
            self._draw_orb_with_glow(surface, orb_color, (cell_x + 10, cell_y + 5), orb_radius)
            
        else:  # 4 or more orbs
            # Draw orbs in a circular pattern with rotation animation
            for i in range(min(cell.orb_count, 4)):
                angle = (i * 2 * math.pi / 4) + self.animation_time * 2
                pos_x = cell_x + math.cos(angle) * 15
                pos_y = cell_y + math.sin(angle) * 15
                self._draw_orb_with_glow(surface, orb_color, (int(pos_x), int(pos_y)), orb_radius)
        
        # Draw critical mass indicator
        if cell.orb_count >= cell.critical_mass:
            # Draw pulsing border to indicate ready to explode
            pulse = abs(math.sin(self.animation_time * 4)) * 100 + 155
            border_color = (255, int(pulse), 0)  # Pulsing yellow/orange
            border_rect = pygame.Rect(
                self.grid_x + col * self.cell_size + 2,
                self.grid_y + row * self.cell_size + 2,
                self.cell_size - 4, self.cell_size - 4
            )
            pygame.draw.rect(surface, border_color, border_rect, 3)
        
        # Draw orb count number
        count_text = self.font_small.render(str(cell.orb_count), True, text_color)
        text_rect = count_text.get_rect(center=(cell_x, cell_y + 20))
        surface.blit(count_text, text_rect)
    
    def _draw_orb_with_glow(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                           pos: Tuple[int, int], radius: int) -> None:
        """Draw an orb with a subtle glow effect"""
        x, y = pos
        
        # Draw glow (larger, semi-transparent circle)
        glow_color = (*color, 100)  # Add alpha for transparency
        glow_surface = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, glow_color, (radius * 2, radius * 2), radius + 4)
        surface.blit(glow_surface, (x - radius * 2, y - radius * 2))
        
        # Draw main orb
        pygame.draw.circle(surface, color, (x, y), radius)
        pygame.draw.circle(surface, self.colors['text_dark'], (x, y), radius, 1)
    
    def _draw_game_info(self, surface: pygame.Surface, game_state: GameState) -> None:
        """Draw game information panel"""
        info = game_state.get_game_info()
        
        # Title
        title_text = "Chain Reaction"
        title_surface = self.font_title.render(title_text, True, self.colors['text_dark'])
        surface.blit(title_surface, (WINDOW_WIDTH // 2 - title_surface.get_width() // 2, 30))
        
        # Current player or game over status
        if info['game_over']:
            if info['winner']:
                winner_text = f"🎉 Player {info['winner']} Wins! 🎉"
                winner_color = self.colors['player1'] if info['winner'] == 1 else self.colors['player2']
                winner_surface = self.font_large.render(winner_text, True, winner_color)
                surface.blit(winner_surface, (WINDOW_WIDTH // 2 - winner_surface.get_width() // 2, 80))
            else:
                draw_text = "Game Over - Draw!"
                draw_surface = self.font_large.render(draw_text, True, self.colors['text_dark'])
                surface.blit(draw_surface, (WINDOW_WIDTH // 2 - draw_surface.get_width() // 2, 80))
        else:
            current_player_text = f"Player {info['current_player']}'s Turn"
            player_color = self.colors['player1'] if info['current_player'] == 1 else self.colors['player2']
            player_surface = self.font_medium.render(current_player_text, True, player_color)
            surface.blit(player_surface, (WINDOW_WIDTH // 2 - player_surface.get_width() // 2, 80))
        
        # Game statistics
        stats_y = WINDOW_HEIGHT - 150
        stats = [
            f"Move: {info['total_moves']}",
            f"Player 1: {info['player1_cells']} cells",
            f"Player 2: {info['player2_cells']} cells",
            f"Total Orbs: {info['total_orbs']}"
        ]
        
        for i, stat in enumerate(stats):
            color = self.colors['text_dark']
            if "Player 1" in stat:
                color = self.colors['player1']
            elif "Player 2" in stat:
                color = self.colors['player2']
            
            stat_surface = self.font_small.render(stat, True, color)
            surface.blit(stat_surface, (50, stats_y + i * 25))
    
    def _draw_instructions(self, surface: pygame.Surface) -> None:
        """Draw game instructions"""
        instructions = [
            "Click on a cell to place an orb",
            "Reach critical mass to trigger explosions",
            "Eliminate all opponent orbs to win",
            "Press R to reset | ESC for menu"
        ]
        
        instruction_y = WINDOW_HEIGHT - 40
        for instruction in instructions:
            inst_surface = self.font_small.render(instruction, True, self.colors['text_dark'])
            surface.blit(inst_surface, (WINDOW_WIDTH // 2 - inst_surface.get_width() // 2, instruction_y))
            instruction_y += 20
    
    def draw_explosion_effect(self, surface: pygame.Surface, position: Tuple[int, int], 
                             progress: float) -> None:
        """
        Draw explosion animation effect at the given position.
        
        Args:
            surface: Surface to draw on
            position: Cell position (row, col)
            progress: Animation progress from 0.0 to 1.0
        """
        row, col = position
        center_x = self.grid_x + col * self.cell_size + self.cell_size // 2
        center_y = self.grid_y + row * self.cell_size + self.cell_size // 2
        
        # Create explosion effect
        max_radius = int(self.cell_size * 0.8 * progress)
        alpha = int(255 * (1.0 - progress))
        
        # Draw expanding circle
        explosion_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)
        explosion_color = (255, 255, 0, alpha)  # Yellow with fading alpha
        pygame.draw.circle(explosion_surface, explosion_color, 
                          (max_radius, max_radius), max_radius)
        
        surface.blit(explosion_surface, 
                    (center_x - max_radius, center_y - max_radius))
    
    def draw_moving_orb(self, surface: pygame.Surface, 
                       start_pos: Tuple[int, int], end_pos: Tuple[int, int],
                       progress: float, player: int) -> None:
        """
        Draw a moving orb animation between two positions.
        
        Args:
            surface: Surface to draw on
            start_pos: Starting cell position (row, col)
            end_pos: Ending cell position (row, col)
            progress: Animation progress from 0.0 to 1.0
            player: Player number for orb color
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        
        # Calculate screen positions
        start_x = self.grid_x + start_col * self.cell_size + self.cell_size // 2
        start_y = self.grid_y + start_row * self.cell_size + self.cell_size // 2
        end_x = self.grid_x + end_col * self.cell_size + self.cell_size // 2
        end_y = self.grid_y + end_row * self.cell_size + self.cell_size // 2
        
        # Interpolate position
        current_x = int(start_x + (end_x - start_x) * progress)
        current_y = int(start_y + (end_y - start_y) * progress)
        
        # Choose color
        orb_color = self.colors['player1'] if player == 1 else self.colors['player2']
        
        # Draw moving orb
        self._draw_orb_with_glow(surface, orb_color, (current_x, current_y), 6)
    
    def get_cell_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Convert mouse position to cell coordinates.
        
        Args:
            mouse_pos: Mouse position (x, y)
            
        Returns:
            Cell coordinates (row, col) or None if outside grid
        """
        x, y = mouse_pos
        
        # Check if click is within grid bounds
        if (x < self.grid_x or y < self.grid_y or 
            x >= self.grid_x + self.cols * self.cell_size or
            y >= self.grid_y + self.rows * self.cell_size):
            return None
        
        # Calculate grid position
        col = (x - self.grid_x) // self.cell_size
        row = (y - self.grid_y) // self.cell_size
        
        return (row, col)
