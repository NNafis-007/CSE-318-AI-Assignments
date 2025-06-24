import pygame
import sys
import os
import time
import subprocess
from typing import Optional, Tuple, List, Callable

# Import from the game engine
from chainReactionEngine import (
    ChainReactionGame, 
    Player, 
    GameMode, 
    AIType,
    MinimaxAI, 
    RandomAI,
    ChainReactionHeuristics
)

class ChainReactionGUI:
    def __init__(self):
        pygame.init()
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.GREEN = (0, 255, 0)
        self.DARK_GREEN = (0, 128, 0)
        self.YELLOW = (255, 255, 0)
        
        # Game state - using the actual game engine
        self.game = None
        self.game_mode = None
        self.ai_red = None
        self.ai_blue = None
        
        # Menu state
        self.in_menu = True
        self.menu_state = "main"  # "main", "grid_size", "ai_config_red", "ai_config_blue", "heuristic_red", "heuristic_blue", "depth_red", "depth_blue"
        self.selected_mode = None
        self.selected_rows = 3
        self.selected_cols = 3
        self.depth_red = 3
        self.depth_blue = 3
        self.red_ai_type = None
        self.blue_ai_type = None
        self.red_heuristic = None
        self.blue_heuristic = None
          # GUI settings
        self.cell_size = 80
        self.margin = 10
        self.top_margin = 150
        self.bottom_margin = 200
        self.min_screen_width = 600
        self.min_screen_height = 600
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Files
        self.gamestate_file = "gamestate.txt"
        self.last_move_time = 0
        
        # Heuristic options
        self.heuristic_options = [
            ("Orb Count", ChainReactionHeuristics.orb_count_heuristic),
            ("Explosion Potential", ChainReactionHeuristics.explosion_potential_heuristic),
            ("Strategic Evaluation", ChainReactionHeuristics.strategic_eval_heuristic),
            ("Threat Analysis", ChainReactionHeuristics.threat_analysis_heuristic),
            ("Tempo", ChainReactionHeuristics.tempo_heuristic),
            ("Combined Strategy", ChainReactionHeuristics.strat_eval_expl_potential_combined_heuristic)
        ]
    def reset_game_state(self):
        """Reset all game configuration"""
        self.game = None
        self.game_mode = None
        self.ai_red = None
        self.ai_blue = None
        self.selected_mode = None
        self.red_ai_type = None
        self.blue_ai_type = None
        self.red_heuristic = None
        self.blue_heuristic = None
        self.menu_state = "main"
        self.in_menu = True
        
        # Reset cell size and font to defaults
        self.cell_size = 80
        self.font = pygame.font.Font(None, 36)
    
    def initialize_game(self):
        """Initialize the game with current configuration"""
        self.game = ChainReactionGame(self.selected_rows, self.selected_cols)
        self.game_mode = self.selected_mode
        
        # Calculate optimal cell size for the selected grid
        _, _, optimal_cell_size = self.calculate_screen_dimensions()
        self.cell_size = optimal_cell_size
        
        # Adjust font sizes based on cell size for better readability
        if self.cell_size < 60:
            self.font = pygame.font.Font(None, max(24, int(self.cell_size * 0.4)))
        else:
            self.font = pygame.font.Font(None, 36)
        
        # Set up AI players based on configuration
        if self.red_ai_type == AIType.SMART:
            heuristic = self.red_heuristic or ChainReactionHeuristics.orb_count_heuristic
            self.ai_red = MinimaxAI(Player.RED, depth=self.depth_red, heuristic_func=heuristic)
        elif self.red_ai_type == AIType.RANDOM:
            self.ai_red = RandomAI(Player.RED)
        else:
            self.ai_red = None
            
        if self.blue_ai_type == AIType.SMART:
            heuristic = self.blue_heuristic or ChainReactionHeuristics.strategic_eval_heuristic
            self.ai_blue = MinimaxAI(Player.BLUE, depth=self.depth_blue, heuristic_func=heuristic)
        elif self.blue_ai_type == AIType.RANDOM:
            self.ai_blue = RandomAI(Player.BLUE)
        else:
            self.ai_blue = None
        
        # Save initial game state
        self.save_game_state()
        self.in_menu = False
        
    def save_game_state(self):
        """Save current game state to file"""
        if self.game:
            move_type = "Game State"
            if self.game_mode == GameMode.USER_VS_USER:
                move_type = f"{self.game.current_player.value}"
            elif self.game_mode == GameMode.USER_VS_AI:
                move_type = "Human" if self.game.current_player == Player.RED else "AI"
            elif self.game_mode == GameMode.AI_VS_AI:
                move_type = f"AI {self.game.current_player.value}"
            
            self.game.save_to_file(self.gamestate_file, move_type, self.game_mode)
    
    def make_move(self, row: int, col: int) -> bool:
        """Make a move using the game engine"""
        if not self.game or self.game.game_over:
            return False
        
        current_player = self.game.current_player
        success = self.game.make_move(row, col, current_player)
        
        if success:
            self.save_game_state()
            self.last_move_time = time.time()
        
        return success
    
    def make_ai_move(self):
        """Make an AI move using the configured AI"""
        if not self.game or self.game.game_over:
            return False
        
        current_player = self.game.current_player
        ai_player = None
        
        if current_player == Player.RED and self.ai_red:
            ai_player = self.ai_red
        elif current_player == Player.BLUE and self.ai_blue:
            ai_player = self.ai_blue
        
        if ai_player:
            move = ai_player.get_best_move(self.game)
            if move:
                success = self.game.make_move(move[0], move[1], current_player)
                if success:
                    self.save_game_state()
                    self.last_move_time = time.time()
                    print(f"AI {current_player.value} played: {move[0]}, {move[1]}")
                return success
        
        return False
    
    def get_cell_color(self, cell) -> tuple:
        """Get color for a cell based on its player"""
        if cell.player == Player.RED:
            return self.RED
        elif cell.player == Player.BLUE:
            return self.BLUE
        else:
            return self.WHITE
    
    def draw_menu(self, screen):
        """Draw the appropriate menu based on menu_state"""
        if self.menu_state == "main":
            self.draw_main_menu(screen)
        elif self.menu_state == "grid_size":
            self.draw_grid_size_menu(screen)
        elif self.menu_state == "ai_config_red":
            self.draw_ai_config_menu(screen, "Red")
        elif self.menu_state == "ai_config_blue":
            self.draw_ai_config_menu(screen, "Blue")
        elif self.menu_state == "heuristic_red":
            self.draw_heuristic_menu(screen, "Red")
        elif self.menu_state == "heuristic_blue":
            self.draw_heuristic_menu(screen, "Blue")
        elif self.menu_state == "depth_red":
            self.draw_depth_menu(screen, "Red")
        elif self.menu_state == "depth_blue":
            self.draw_depth_menu(screen, "Blue")
    
    def draw_main_menu(self, screen):
        """Draw the main menu"""
        screen.fill(self.WHITE)
        
        # Title
        title_text = self.title_font.render("Chain Reaction", True, self.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 80))
        screen.blit(title_text, title_rect)
        
        # Menu options
        menu_items = [
            "1. User vs User",
            "2. User vs AI", 
            "3. AI vs AI",
            "4. Exit"
        ]
        
        y_start = 180
        for i, item in enumerate(menu_items):
            color = self.DARK_GREEN if i < 3 else self.RED
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(screen.get_width()//2, y_start + i * 60))
            screen.blit(text, text_rect)
        
        # Instructions
        instructions = [
            "Click on a menu option to start configuration",
            "Configure grid size and AI settings in next steps"
        ]
        
        y_start = 450
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, self.GRAY)
            text_rect = text.get_rect(center=(screen.get_width()//2, y_start + i * 30))
            screen.blit(text, text_rect)
    
    def draw_grid_size_menu(self, screen):
        """Draw grid size selection menu"""
        screen.fill(self.WHITE)
        
        # Title
        title_text = self.title_font.render("Select Grid Size", True, self.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 80))
        screen.blit(title_text, title_rect)
        
        # Current mode
        mode_text = f"Mode: {self.selected_mode.name.replace('_', ' ')}"
        mode_surface = self.font.render(mode_text, True, self.DARK_GREEN)
        mode_rect = mode_surface.get_rect(center=(screen.get_width()//2, 130))
        screen.blit(mode_surface, mode_rect)
        
        # Grid size options
        grid_options = [
            "1. 3x3 Grid (Quick)",
            "2. 6x4 Grid (Casual)",
            "3. 9x6 Grid (Marathon)",
            "4. Back to Main Menu"
        ]
        
        y_start = 200
        for i, option in enumerate(grid_options):
            color = self.DARK_GREEN if i < 3 else self.RED
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width()//2, y_start + i * 60))
            screen.blit(text, text_rect)
    
    def draw_ai_config_menu(self, screen, configuring_player: str):
        """Draw AI configuration menu"""
        screen.fill(self.WHITE)
        
        # Title
        title_text = self.title_font.render(f"Configure {configuring_player} AI", True, self.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 60))
        screen.blit(title_text, title_rect)
        
        # Current selections
        info_y = 100
        info_text = f"Mode: {self.selected_mode.name.replace('_', ' ')} | Grid: {self.selected_rows}x{self.selected_cols}"
        info_surface = self.small_font.render(info_text, True, self.GRAY)
        info_rect = info_surface.get_rect(center=(screen.get_width()//2, info_y))
        screen.blit(info_surface, info_rect)
        
        # AI Type selection
        ai_options = [
            "1. Smart AI (Minimax)",
            "2. Random AI",
            "3. Back"
        ]
        
        y_start = 150
        for i, option in enumerate(ai_options):
            color = self.DARK_GREEN if i < 2 else self.RED
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width()//2, y_start + i * 50))
            screen.blit(text, text_rect)
    
    def draw_heuristic_menu(self, screen, configuring_player: str):
        """Draw heuristic selection menu"""
        screen.fill(self.WHITE)
        
        # Title
        title_text = self.title_font.render(f"{configuring_player} AI Heuristic", True, self.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 50))
        screen.blit(title_text, title_rect)
        
        # Heuristic options
        y_start = 120
        for i, (name, _) in enumerate(self.heuristic_options):
            text = self.small_font.render(f"{i+1}. {name}", True, self.DARK_GREEN)
            text_rect = text.get_rect(center=(screen.get_width()//2, y_start + i * 40))
            screen.blit(text, text_rect)
        
        # Back option
        back_text = self.small_font.render(f"{len(self.heuristic_options)+1}. Back", True, self.RED)
        back_rect = back_text.get_rect(center=(screen.get_width()//2, y_start + len(self.heuristic_options) * 40))
        screen.blit(back_text, back_rect)
    
    def draw_depth_menu(self, screen, configuring_player: str):
        """Draw depth selection menu"""
        screen.fill(self.WHITE)
        
        # Title
        title_text = self.title_font.render(f"{configuring_player} AI Difficulty", True, self.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 80))
        screen.blit(title_text, title_rect)
        
        # Depth options
        depth_options = [
            "1. Easy (Depth 2) - Fast",
            "2. Medium (Depth 3) - Balanced", 
            "3. Hard (Depth 4) - Strategic",
            "4. Back"
        ]
        
        y_start = 180
        for i, option in enumerate(depth_options):
            color = self.DARK_GREEN if i < 3 else self.RED
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width()//2, y_start + i * 60))
            screen.blit(text, text_rect)
    
    def handle_menu_click(self, pos: Tuple[int, int], screen_width: int) -> bool:
        """Handle menu clicks based on current menu state"""
        x, y = pos
        
        # Check if click is in menu area
        if x < screen_width//2 - 200 or x > screen_width//2 + 200:
            return True
        
        if self.menu_state == "main":
            return self.handle_main_menu_click(y)
        elif self.menu_state == "grid_size":
            return self.handle_grid_size_click(y)
        elif self.menu_state == "ai_config_red":
            return self.handle_ai_config_click(y, "red")
        elif self.menu_state == "ai_config_blue":
            return self.handle_ai_config_click(y, "blue")
        elif self.menu_state == "heuristic_red":
            return self.handle_heuristic_click(y, "red")
        elif self.menu_state == "heuristic_blue":
            return self.handle_heuristic_click(y, "blue")
        elif self.menu_state == "depth_red":
            return self.handle_depth_click(y, "red")
        elif self.menu_state == "depth_blue":
            return self.handle_depth_click(y, "blue")
        
        return True
    
    def handle_main_menu_click(self, y: int) -> bool:
        """Handle main menu clicks"""
        y_start = 180
        option_height = 60
        
        for i in range(4):
            option_y = y_start + i * option_height
            if option_y - 30 <= y <= option_y + 30:
                if i == 0:  # User vs User
                    self.selected_mode = GameMode.USER_VS_USER
                    self.menu_state = "grid_size"
                elif i == 1:  # User vs AI
                    self.selected_mode = GameMode.USER_VS_AI
                    self.menu_state = "grid_size"
                elif i == 2:  # AI vs AI
                    self.selected_mode = GameMode.AI_VS_AI
                    self.menu_state = "grid_size"
                elif i == 3:  # Exit
                    return False
                break
        return True
    
    def handle_grid_size_click(self, y: int) -> bool:
        """Handle grid size menu clicks"""
        y_start = 200
        option_height = 60
        
        for i in range(4):
            option_y = y_start + i * option_height
            if option_y - 30 <= y <= option_y + 30:
                if i == 0:  # 3x3
                    self.selected_rows = 3
                    self.selected_cols = 3
                    self.proceed_after_grid_selection()
                elif i == 1:  # 6x4
                    self.selected_rows = 6
                    self.selected_cols = 4
                    self.proceed_after_grid_selection()
                elif i == 2:  # 9x6
                    self.selected_rows = 9
                    self.selected_cols = 6
                    self.proceed_after_grid_selection()
                elif i == 3:  # Back
                    self.menu_state = "main"
                break
        return True
    
    def proceed_after_grid_selection(self):
        """Decide what to do after grid size is selected"""
        if self.selected_mode == GameMode.USER_VS_USER:
            # No AI configuration needed, start game directly
            self.initialize_game()
        elif self.selected_mode == GameMode.USER_VS_AI:
            # Only need to configure Blue AI
            self.menu_state = "ai_config_blue"
        elif self.selected_mode == GameMode.AI_VS_AI:
            # Need to configure Red AI first
            self.menu_state = "ai_config_red"
    
    def handle_ai_config_click(self, y: int, player: str) -> bool:
        """Handle AI configuration clicks"""
        y_start = 150
        option_height = 50
        
        for i in range(3):
            option_y = y_start + i * option_height
            if option_y - 25 <= y <= option_y + 25:
                if i == 0:  # Smart AI
                    if player == "red":
                        self.red_ai_type = AIType.SMART
                        self.menu_state = "heuristic_red"
                    else:
                        self.blue_ai_type = AIType.SMART
                        self.menu_state = "heuristic_blue"
                elif i == 1:  # Random AI
                    if player == "red":
                        self.red_ai_type = AIType.RANDOM
                        self.proceed_after_red_ai_config()
                    else:
                        self.blue_ai_type = AIType.RANDOM
                        self.proceed_after_blue_ai_config()
                elif i == 2:  # Back
                    self.menu_state = "grid_size"
                break
        return True
    
    def handle_heuristic_click(self, y: int, player: str) -> bool:
        """Handle heuristic selection clicks"""
        y_start = 120
        option_height = 40
        
        total_options = len(self.heuristic_options) + 1  # +1 for back option
        
        for i in range(total_options):
            option_y = y_start + i * option_height
            if option_y - 20 <= y <= option_y + 20:
                if i < len(self.heuristic_options):
                    # Selected a heuristic
                    _, heuristic_func = self.heuristic_options[i]
                    if player == "red":
                        self.red_heuristic = heuristic_func
                        self.menu_state = "depth_red"
                    else:
                        self.blue_heuristic = heuristic_func
                        self.menu_state = "depth_blue"
                else:
                    # Back option
                    if player == "red":
                        self.menu_state = "ai_config_red"
                    else:
                        self.menu_state = "ai_config_blue"
                break
        return True
    
    def handle_depth_click(self, y: int, player: str) -> bool:
        """Handle depth selection clicks"""
        y_start = 180
        option_height = 60
        
        for i in range(4):
            option_y = y_start + i * option_height
            if option_y - 30 <= y <= option_y + 30:
                if i == 0:  # Easy (Depth 2)
                    if player == "red":
                        self.depth_red = 2
                        self.proceed_after_red_ai_config()
                    else:
                        self.depth_blue = 2
                        self.proceed_after_blue_ai_config()
                elif i == 1:  # Medium (Depth 3)
                    if player == "red":
                        self.depth_red = 3
                        self.proceed_after_red_ai_config()
                    else:
                        self.depth_blue = 3
                        self.proceed_after_blue_ai_config()
                elif i == 2:  # Hard (Depth 4)
                    if player == "red":
                        self.depth_red = 4
                        self.proceed_after_red_ai_config()
                    else:
                        self.depth_blue = 4
                        self.proceed_after_blue_ai_config()
                elif i == 3:  # Back
                    if player == "red":
                        self.menu_state = "heuristic_red"
                    else:
                        self.menu_state = "heuristic_blue"
                break
        return True
    
    def proceed_after_red_ai_config(self):
        """Proceed after Red AI configuration is complete"""
        if self.selected_mode == GameMode.AI_VS_AI:
            # Now configure Blue AI
            self.menu_state = "ai_config_blue"
        else:
            # This shouldn't happen in current flow, but just in case
            self.initialize_game()
    
    def proceed_after_blue_ai_config(self):
        """Proceed after Blue AI configuration is complete"""
        # Blue AI configuration is always the last step
        self.initialize_game()
    
    def draw_game(self, screen):
        """Draw the game board and UI using the actual game engine"""
        if not self.game:
            return
            
        screen.fill(self.WHITE)
        
        # Calculate board position
        board_width = self.game.cols * self.cell_size + (self.game.cols - 1) * self.margin
        board_height = self.game.rows * self.cell_size + (self.game.rows - 1) * self.margin
        start_x = (screen.get_width() - board_width) // 2
        start_y = self.top_margin
        
        # Draw title and scores
        title_text = self.font.render("Chain Reaction", True, self.BLACK)
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 30))
        screen.blit(title_text, title_rect)
        
        # Get scores from game engine
        scores = self.game.get_score()
        score_text = f"Red: {scores[Player.RED]}  Blue: {scores[Player.BLUE]}"
        score_surface = self.font.render(score_text, True, self.BLACK)
        score_rect = score_surface.get_rect(center=(screen.get_width()//2, 60))
        screen.blit(score_surface, score_rect)
        
        # Draw current player
        if not self.game.game_over:
            player_text = f"Current Player: {self.game.current_player.value}"
            player_color = self.RED if self.game.current_player == Player.RED else self.BLUE
            player_surface = self.font.render(player_text, True, player_color)
            player_rect = player_surface.get_rect(center=(screen.get_width()//2, 90))
            screen.blit(player_surface, player_rect)
            
            # Show game mode
            mode_text = f"Mode: {self.game_mode.name.replace('_', ' ')}"
            mode_surface = self.small_font.render(mode_text, True, self.GRAY)
            mode_rect = mode_surface.get_rect(center=(screen.get_width()//2, 115))
            screen.blit(mode_surface, mode_rect)
        
        # Draw board using game engine data
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                x = start_x + col * (self.cell_size + self.margin)
                y = start_y + row * (self.cell_size + self.margin)
                
                cell = self.game.board[row][col]
                color = self.get_cell_color(cell)
                
                # Draw cell background
                pygame.draw.rect(screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, self.BLACK, (x, y, self.cell_size, self.cell_size), 2)
                
                # Draw orbs
                if cell.orbs > 0:
                    orb_text = str(cell.orbs)
                    text_color = self.WHITE if cell.player != Player.EMPTY else self.BLACK
                    orb_surface = self.font.render(orb_text, True, text_color)
                    text_rect = orb_surface.get_rect(center=(x + self.cell_size//2, y + self.cell_size//2))
                    screen.blit(orb_surface, text_rect)
        
        # Draw game over message
        if self.game.game_over:
            game_over_text = "GAME OVER!"
            winner_text = f"Winner: {self.game.winner.value}" if self.game.winner else "Draw!"
            
            game_over_surface = self.title_font.render(game_over_text, True, self.BLACK)
            winner_surface = self.font.render(winner_text, True, self.RED if self.game.winner == Player.RED else self.BLUE)
            
            game_over_rect = game_over_surface.get_rect(center=(screen.get_width()//2, start_y + board_height + 50))
            winner_rect = winner_surface.get_rect(center=(screen.get_width()//2, start_y + board_height + 90))
            
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(winner_surface, winner_rect)
            
            # Back to menu button
            menu_text = "Press SPACE for Main Menu"
            menu_surface = self.small_font.render(menu_text, True, self.GRAY)
            menu_rect = menu_surface.get_rect(center=(screen.get_width()//2, start_y + board_height + 130))
            screen.blit(menu_surface, menu_rect)
    
    def handle_game_click(self, pos: Tuple[int, int], screen_width: int):
        """Handle clicks during gameplay"""
        if not self.game or self.game.game_over:
            return
        
        # Check if it's a human player's turn
        current_player = self.game.current_player
        if self.game_mode == GameMode.USER_VS_AI and current_player == Player.BLUE:
            return  # It's AI's turn, ignore clicks
        elif self.game_mode == GameMode.AI_VS_AI:
            return  # Both are AI, ignore clicks
        
        # Calculate board position
        board_width = self.game.cols * self.cell_size + (self.game.cols - 1) * self.margin
        start_x = (screen_width - board_width) // 2
        start_y = self.top_margin
        
        x, y = pos
        
        # Check if click is on the board
        if x < start_x or y < start_y:
            return
        
        # Calculate which cell was clicked
        col = (x - start_x) // (self.cell_size + self.margin)
        row = (y - start_y) // (self.cell_size + self.margin)
        
        if 0 <= row < self.game.rows and 0 <= col < self.game.cols:
            # Check if it's a valid move using game engine
            if self.game.is_valid_move(row, col, current_player):
                self.make_move(row, col)
    
    def calculate_screen_dimensions(self):
        """Calculate optimal screen dimensions and cell size based on grid size"""
        if not hasattr(self, 'selected_rows') or not hasattr(self, 'selected_cols'):
            return 700, 800, 80
        
        # Calculate required board dimensions
        max_cell_size = 80
        min_cell_size = 40
        
        # Try with maximum cell size first
        cell_size = max_cell_size
        board_width = self.selected_cols * cell_size + (self.selected_cols - 1) * self.margin
        board_height = self.selected_rows * cell_size + (self.selected_rows - 1) * self.margin
        
        # Calculate required screen dimensions
        screen_width = max(board_width + 100, self.min_screen_width)  # Add padding
        screen_height = board_height + self.top_margin + self.bottom_margin
        
        # If screen would be too large, reduce cell size
        max_screen_width = 1200
        max_screen_height = 900
        
        if screen_width > max_screen_width or screen_height > max_screen_height:
            # Calculate maximum possible cell size that fits in screen
            max_width_cell_size = (max_screen_width - 100 - (self.selected_cols - 1) * self.margin) // self.selected_cols
            max_height_cell_size = (max_screen_height - self.top_margin - self.bottom_margin - (self.selected_rows - 1) * self.margin) // self.selected_rows
            
            cell_size = max(min(max_width_cell_size, max_height_cell_size, max_cell_size), min_cell_size)
              # Recalculate dimensions with new cell size
            board_width = self.selected_cols * cell_size + (self.selected_cols - 1) * self.margin
            board_height = self.selected_rows * cell_size + (self.selected_rows - 1) * self.margin
            screen_width = max(board_width + 100, self.min_screen_width)
            screen_height = board_height + self.top_margin + self.bottom_margin
        
        return screen_width, screen_height, cell_size
    
    def run(self):
        """Main game loop"""
        screen = pygame.display.set_mode((700, 800))
        pygame.display.set_caption("Chain Reaction")
        clock = pygame.time.Clock()
        current_screen_size = (700, 800)
        
        running = True
        while running:
            # Check if we need to resize screen when starting a game
            if not self.in_menu and self.game:
                required_width, required_height, _ = self.calculate_screen_dimensions()
                if current_screen_size != (required_width, required_height):
                    screen = pygame.display.set_mode((required_width, required_height))
                    current_screen_size = (required_width, required_height)
            elif self.in_menu and current_screen_size != (700, 800):
                # Reset to default size for menu
                screen = pygame.display.set_mode((700, 800))
                current_screen_size = (700, 800)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.in_menu:
                        if not self.handle_menu_click(event.pos, screen.get_width()):
                            running = False
                    else:
                        self.handle_game_click(event.pos, screen.get_width())
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game and self.game.game_over:
                        self.reset_game_state()
            
            # Handle AI moves
            if not self.in_menu and self.game and not self.game.game_over:
                current_player = self.game.current_player
                should_make_ai_move = False
                
                if self.game_mode == GameMode.USER_VS_AI and current_player == Player.BLUE:
                    # AI's turn in User vs AI mode
                    if time.time() - self.last_move_time > 1.0:  # Wait 1 second
                        should_make_ai_move = True
                elif self.game_mode == GameMode.AI_VS_AI:
                    # AI vs AI mode
                    if time.time() - self.last_move_time > 1.5:  # Wait 1.5 seconds
                        should_make_ai_move = True
                
                if should_make_ai_move:
                    self.make_ai_move()
            
            # Draw
            if self.in_menu:
                self.draw_menu(screen)
            else:
                self.draw_game(screen)
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = ChainReactionGUI()
    gui.run()
