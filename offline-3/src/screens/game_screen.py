import pygame
from typing import Optional, Tuple, List
from src.core.interfaces import EventHandler
from src.ui.ui_renderer import UIRenderer
from src.config.enums import GameMode
from src.config.config import *
from src.core.cell import Cell
from src.ui.animation import AnimationManager

class GameBoard:
    """Represents the Chain Reaction game board with cell-based logic"""
    
    def __init__(self, rows: int = GRID_ROWS, cols: int = GRID_COLS):
        self.rows = rows
        self.cols = cols
        self.current_player = 1  # Start with player 1
        self.game_over = False
        self.winner = None
        self.player_cells = {1: 0, 2: 0}  # Track cells owned by each player
          # Create a 2D grid of Cell objects
        self.board = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        
        # Game statistics
        self.total_moves = 0
        self.explosion_chain_length = 0
        
        # Add animation manager
        self.animation_manager = AnimationManager()
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the given position is valid"""
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Get the cell at the specified position"""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def can_place_orb(self, row: int, col: int) -> bool:
        """Check if current player can place an orb at the given position"""
        if self.game_over:
            return False
            
        cell = self.get_cell(row, col)
        if cell:
            return cell.can_place_orb(self.current_player)
        return False
    
    def place_orb(self, row: int, col: int) -> bool:
        """
        Place an orb at the specified position and handle explosions.
        
        Args:
            row: Row position
            col: Column position
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        if not self.can_place_orb(row, col):
            return False
        
        cell = self.get_cell(row, col)
        if not cell:
            return False
        
        # Place the orb
        success = cell.add_orb(self.current_player)
        if not success:
            return False
            
        self.total_moves += 1
        self.player_cells[self.current_player] += 1
        
        print(f"Player {self.current_player} placed orb at ({row}, {col}), his cells : {self.player_cells[self.current_player]}")
        
        # Handle explosions if necessary
        if cell.orb_count >= cell.critical_mass:
            self._handle_explosions((row, col))
        
        # Check for game over
        self._check_game_over()
        
        # Switch to next player if game continues
        if not self.game_over:
            self._switch_player()
        
        return True
    
    def _handle_explosions(self, initial_explosion: Tuple[int, int]):
        """
        Handle chain explosions starting from initial explosion points.
        
        Args:
            initial_explosion: Cell (row, col) coordinates to explode
        """
        
        explosion_queue : List[Tuple[int,int]] = []
        explosion_queue.append(initial_explosion)
        chain_length = 0
        
        while len(explosion_queue) > 0:
            self._check_game_over()
            if self.game_over:
                print(f"Game over detected during explosion #{chain_length}, stopping chain.")
                break
            chain_length += 1
            print(f"Explosion chain #{chain_length}")
            row, col = explosion_queue.pop(0)
            
            # Process all current explosions
            cell = self.get_cell(row, col)
            print(f"Processing explosion at ({row}, {col})")            # Explode if cell is valid and has enough orbs
            if cell and cell.orb_count >= cell.critical_mass:
                
                # Get neighbors that will receive orbs
                neighbors = cell._get_neighbors()
                have_exploded = cell.explode()
                
                # Add explosion effect animation
                self.animation_manager.add_explosion_effect((row, col), duration=0.5)

                
                print(f"Cell ({row}, {col}) explosion : {have_exploded}, affecting neighbors {neighbors}")
                
                # Distribute orbs to neighbors with animation
                if have_exploded:
                    for neighbor_row, neighbor_col in neighbors:
                        # Add moving orb animation from exploding cell to neighbor
                        self.animation_manager.add_moving_orb(
                            start_cell=(row, col),
                            end_cell=(neighbor_row, neighbor_col),
                            player=self.current_player,
                            duration=1.0
                        )
                        
                        neighbor_cell = self.get_cell(neighbor_row, neighbor_col)
                        if neighbor_cell:
                            # Add orb from explosion (always from current player)
                            if neighbor_cell.player is not None and neighbor_cell.player != self.current_player:
                                self.player_cells[neighbor_cell.player] -= neighbor_cell.orb_count
                                self.player_cells[self.current_player] += neighbor_cell.orb_count
                            neighbor_cell.player = self.current_player
                            neighbor_cell.add_orb(self.current_player)
                            
                            # If neighbor will explode, add to next round
                            if neighbor_cell.orb_count >= neighbor_cell.critical_mass:
                                explosion_queue.append((neighbor_row, neighbor_col))


        
        self.explosion_chain_length = chain_length
        if chain_length > 1:
            print(f"Chain reaction completed! Length: {chain_length}")
    
    def _switch_player(self):
        """Switch to the next player"""
        self.current_player = 2 if self.current_player == 1 else 1
        print(f"Now it's Player {self.current_player}'s turn")
    
    def _check_game_over(self):
        """Check if the game is over and determine winner"""
        if self.total_moves < 2:  # Game can't end in first move
            return
        

        player1_cells = self.player_cells[1]
        player2_cells = self.player_cells[2]
                
        # Determine if game is over
        if player1_cells == 0 and player2_cells > 0 :
            self.game_over = True
            self.winner = 2
            print(f"Game Over! Player 2 wins!")
        elif player2_cells == 0 and player1_cells > 0:
            self.game_over = True
            self.winner = 1
            print(f"Game Over! Player 1 wins!")
    
    def get_game_state(self) -> dict:
        """Get current game state information"""
        player1_cells = self.player_cells[1]
        player2_cells = self.player_cells[2]
        total_orbs = self.total_moves
                
        return {
            'current_player': self.current_player,
            'total_moves': self.total_moves,
            'player1_cells': player1_cells,
            'player2_cells': player2_cells,
            'total_orbs': total_orbs,
            'game_over': self.game_over,
            'winner': self.winner,
            'last_chain_length': self.explosion_chain_length
        }
    
    def reset_game(self):
        """Reset the game to initial state"""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                cell.orb_count = 0
                cell.player = None
                cell.is_exploding = False
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.total_moves = 0
        self.explosion_chain_length = 0
        self.player_cells = {1: 0, 2: 0}
        
        # Clear all animations
        self.animation_manager.clear_all()
        
        print("Game reset!")

    def get_cell_from_mouse_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Cell]:
        """Convert mouse position to cell object"""
        mouse_x, mouse_y = mouse_pos
        
        # Check if click is within the grid
        if (GRID_X <= mouse_x <= GRID_X + GRID_WIDTH and
            GRID_Y <= mouse_y <= GRID_Y + GRID_HEIGHT):
            
            col = (mouse_x - GRID_X) // CELL_SIZE
            row = (mouse_y - GRID_Y) // CELL_SIZE
            
            if self.is_valid_position(row, col):
                return self.board[row][col]
        
        return None

class GameScreen(EventHandler):
    """Handles the game screen with Chain Reaction logic"""
    def __init__(self, ui_renderer: UIRenderer, game_mode: GameMode):
        self.ui_renderer = ui_renderer
        self.game_mode = game_mode
        self.board = GameBoard()
        self.selected_cell = None  # Track selected cell for info display
        self.is_processing_turn = False  # Prevent input during animations

    def handle_mouse_click(self, pos: tuple[int, int]) -> Optional[str]:
        """Handle mouse clicks on the game board"""
        # Don't process clicks during animations
        if self.is_processing_turn:
            return None
            
        if self.game_mode == GameMode.TWO_PLAYER:
            cell = self.board.get_cell_from_mouse_pos(pos)
            if cell:
                self.selected_cell = cell  # Store selected cell for display
                
                # Display detailed cell information
                print("\n" + "="*50)
                
                # Try to place an orb if game is not over
                if not self.board.game_over:
                    if self.board.place_orb(cell.row, cell.col):
                        # Set processing flag to prevent input during animations
                        self.is_processing_turn = True
                                            
                        # Print updated game state
                        state = self.board.get_game_state()
                        print(f"\n📊 GAME STATE:")
                        print(f"Current Player: {state['current_player']}")
                        print(f"Total Moves: {state['total_moves']}")
                        print(f"Player 1 Cells: {state['player1_cells']}")
                        print(f"Player 2 Cells: {state['player2_cells']}")
                        print(f"Total Orbs: {state['total_orbs']}")
                        
                        if state['last_chain_length'] > 1:
                            print(f"💥 Chain Reaction Length: {state['last_chain_length']}")
                        
                        if state['game_over']:
                            print(f"🎉 GAME OVER! Player {state['winner']} wins!")
                        print("="*50)
                    else:
                        print(f"❌ Cannot place orb at ({cell.row}, {cell.col}) - invalid move")
                else:
                    print(f"🎮 Game is over! Player {self.board.winner} has won!")
                
        elif self.game_mode == GameMode.HUMAN_VS_AI:
            print("Huamn vs AI mode not implemented yet!")

        elif self.game_mode == GameMode.AI_VS_AI:
            print("AI vs AI mode not implemented yet!")
        else:
            print("Unknown game mode selected!")

        return None
    
    def handle_key_press(self, key: int) -> Optional[str]:
        """Handle key presses in game screen"""
        if key == pygame.K_ESCAPE:
            return "back_to_menu"
        elif key == pygame.K_r:  # Reset game with 'R' key
            self.board.reset_game()
            self.selected_cell = None
            self.is_processing_turn = False  # Reset processing flag
            print("🔄 Game reset! Press R again anytime to reset.")
        elif key == pygame.K_i:  # Info key - show game state
            state = self.board.get_game_state()
            print("\n" + "="*40)
            print("📊 COMPLETE GAME STATE:")
            print(f"Current Player: {state['current_player']}")
            print(f"Total Moves: {state['total_moves']}")
            print(f"Player 1 Cells: {state['player1_cells']}")
            print(f"Player 2 Cells: {state['player2_cells']}")
            print(f"Total Orbs: {state['total_orbs']}")
            print(f"Game Over: {state['game_over']}")
            if state['game_over']:
                print(f"Winner: Player {state['winner']}")
            print("="*40)
        return None
    
    def draw(self, surface: pygame.Surface):
        """Draw the game screen with enhanced information"""
        surface.fill(WHITE)
        
        # Draw title with current game mode
        self.ui_renderer.draw_text(surface, f"Chain Reaction - {self.game_mode.value}", 
                                 WINDOW_WIDTH // 2, 30, "title")
        
        instruction = " --- Press R to reset | ESC to menu ---"
        # Draw instructions
        self.ui_renderer.draw_text(surface, instruction , WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30, "normal", BLACK)

        
        # Draw game state information
        state = self.board.get_game_state()
        if not state['game_over']:
            color = (255, 0, 0) if state['current_player'] == 1 else (0, 0, 255)
            self.ui_renderer.draw_text(surface, f"Player {state['current_player']}'s Turn", 
                                     WINDOW_WIDTH // 2, 60, "normal", color)
        else:
            winner_color = (255, 0, 0) if state['winner'] == 1 else (0, 0, 255)
            self.ui_renderer.draw_text(surface, f"🎉 Player {state['winner']} Wins! 🎉", 
                                     WINDOW_WIDTH // 2, 60, "title", winner_color)
        
        # Draw move counter and cell counts
        info_texts = [
                f"Move: {state['total_moves']}", 
                f"P1: {state['player1_cells']} cells", 
                f"P2: {state['player2_cells']} cells"
                ]
        
        for i, text in enumerate(info_texts):
            if i == 1:
                color = (255, 0, 0)
            elif i == 2:
                color = (0, 0, 255)
            else:
                color = GRAY
            self.ui_renderer.draw_text(surface, text, 80, WINDOW_HEIGHT - 150 + i * 30, "small", color)
          # Draw the grid
        self.ui_renderer.draw_grid(surface)
        
        # Draw cells with orbs (static state)
        self._draw_game_pieces(surface)
        
        # Draw animations on top
        self.board.animation_manager.draw(surface)
        
        # Draw selected cell info on screen
        if self.selected_cell:
            self._draw_selected_cell_info(surface)
        
        # Show animation status
        if self.is_processing_turn:
            self.ui_renderer.draw_text(surface, "Processing turn...", 
                                     WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30, "small", GRAY)
            self._draw_selected_cell_info(surface)
        
    
    def _draw_game_pieces(self, surface: pygame.Surface):
        """Draw orbs in each cell based on current game state"""
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.get_cell(row, col)
                if cell and not cell.is_empty():
                    # Calculate cell center position
                    cell_x = GRID_X + col * CELL_SIZE + CELL_SIZE // 2
                    cell_y = GRID_Y + row * CELL_SIZE + CELL_SIZE // 2
                    
                    # Choose color based on owner
                    if cell.player == 1:
                        orb_color = (255, 0, 0)  # Red for Player 1
                        text_color = (200, 0, 0)
                    else:
                        orb_color = (0, 0, 255)  # Blue for Player 2
                        text_color = (0, 0, 200)
                    
                    # Draw orbs based on count
                    orb_radius = 8
                    if cell.orb_count == 1:
                        pygame.draw.circle(surface, orb_color, (cell_x, cell_y), orb_radius)
                        pygame.draw.circle(surface, BLACK, (cell_x, cell_y), orb_radius, 2)
                    elif cell.orb_count == 2:
                        pygame.draw.circle(surface, orb_color, (cell_x - 10, cell_y), orb_radius)
                        pygame.draw.circle(surface, orb_color, (cell_x + 10, cell_y), orb_radius)
                        pygame.draw.circle(surface, BLACK, (cell_x - 10, cell_y), orb_radius, 2)
                        pygame.draw.circle(surface, BLACK, (cell_x + 10, cell_y), orb_radius, 2)
                    elif cell.orb_count == 3:
                        pygame.draw.circle(surface, orb_color, (cell_x, cell_y - 10), orb_radius)
                        pygame.draw.circle(surface, orb_color, (cell_x - 10, cell_y + 5), orb_radius)
                        pygame.draw.circle(surface, orb_color, (cell_x + 10, cell_y + 5), orb_radius)
                        pygame.draw.circle(surface, BLACK, (cell_x, cell_y - 10), orb_radius, 2)
                        pygame.draw.circle(surface, BLACK, (cell_x - 10, cell_y + 5), orb_radius, 2)
                        pygame.draw.circle(surface, BLACK, (cell_x + 10, cell_y + 5), orb_radius, 2)
                    
                    # Draw critical mass indicator
                    if cell.orb_count >= cell.critical_mass:
                        # Draw pulsing border to indicate ready to explode
                        border_color = (255, 255, 0)  # Yellow for critical
                        pygame.draw.rect(surface, border_color, 
                                       (GRID_X + col * CELL_SIZE + 2, 
                                        GRID_Y + row * CELL_SIZE + 2,
                                        CELL_SIZE - 4, CELL_SIZE - 4), 3)
                    
                    # Draw orb count number
                    font = pygame.font.Font(None, 20)
                    count_text = font.render(str(cell.orb_count), True, text_color)
                    text_rect = count_text.get_rect(center=(cell_x, cell_y + 20))
                    surface.blit(count_text, text_rect)
    
    def _draw_selected_cell_info(self, surface: pygame.Surface):
        """Draw information about the selected cell on screen"""
        if not self.selected_cell:
            return
        
        cell = self.selected_cell
        info_x = 20
        info_y = 120
        
        # Draw info panel background
        panel_width = 250
        panel_height = 140
        panel_rect = pygame.Rect(info_x - 10, info_y - 10, panel_width, panel_height)
        pygame.draw.rect(surface, (240, 240, 240), panel_rect)
        pygame.draw.rect(surface, BLACK, panel_rect, 2)

        
        # Draw cell information
        info_lines = [
            f"Selected Cell: ({cell.row}, {cell.col})",
            f"Orb Count: {cell.orb_count}",
            f"Owner: Player {cell.player if cell.player else 'None'}",
            f"Critical Mass: {cell.critical_mass}",
            f"Neighbors: {len(cell._get_neighbors())}",
            f"Can Place: {'Yes' if cell.can_place_orb(self.board.current_player) else 'No'}"
        ]
        
        for i, line in enumerate(info_lines):
            self.ui_renderer.draw_text(surface, line, info_x, info_y + i * 18, "small", BLACK, False)
