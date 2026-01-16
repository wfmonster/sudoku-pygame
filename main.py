#! /usr/bin/env python3

# ------------------------------------------------------------
# main.py 
# Lofi Sudoku Game 
# By: Beck Bishp 
# Last Updated: 01/16/2026
# ------------------------------------------------------------

import pygame
import sys

# contains constants for the pygame library
from pygame.locals import *
from constants import WHITE, BLACK, GRAY, SURFACE_HEIGHT, SURFACE_WIDTH, FPS
from constants import HIGHLIGHT_COLOR, PLAYER_NUMBER_COLOR, CORRECT_COLOR, INCORRECT_COLOR
from constants import NUM_CELLS, CELL_SIZE, BOARD_SIZE
from constants import EASY_DIFFICULTY, MEDIUM_DIFFICULTY, HARD_DIFFICULTY
from constants import BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, BUTTON_SELECTED_COLOR
from constants import STATE_MENU, STATE_PLAYING, STATE_GAME_OVER
from generate_puzzle import create_puzzle_from_library


# ------------------------------------------------------------
# Button Class
# ------------------------------------------------------------

class Button:
    """A clickable button for the UI."""
    
    def __init__(self, x, y, width, height, text, font, 
                 color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, 
                 text_color=BUTTON_TEXT_COLOR, selected=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.selected = selected
        self.hovered = False
    
    def draw(self, surface):
        """Draw the button on the surface."""
        # Determine button color based on state
        if self.selected:
            color = BUTTON_SELECTED_COLOR
        elif self.hovered:
            color = self.hover_color
        else:
            color = self.color
        
        # Draw button rectangle
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, width=2, border_radius=8)
        
        # Draw text centered on button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """Handle mouse events. Returns True if button was clicked."""
        if event.type == MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False


# ------------------------------------------------------------
# Game Helper Functions
# ------------------------------------------------------------

def get_board_position():
    "Calculate the top-left position of the board for centering."
    margin_x = (SURFACE_WIDTH - BOARD_SIZE) // 2
    margin_y = (SURFACE_HEIGHT - BOARD_SIZE) // 2
    return margin_x, margin_y


def is_board_complete(puzzle_board, player_board):
    """Check if all cells are filled (no empty cells remaining)."""
    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS):
            original = puzzle_board[row][col]
            player = player_board[row][col]
            if (original is None or original == 0) and (player is None or player == 0):
                return False
    return True


def check_solution(puzzle_board, player_board, solution_board):
    """Check if the player's solution is correct."""
    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS):
            original = puzzle_board[row][col]
            if original is None or original == 0:
                player_value = player_board[row][col]
                solution_value = solution_board[row][col]
                if player_value != solution_value:
                    return False
    return True


def is_cell_correct(row, col, puzzle_board, player_board, solution_board):
    """Check if a specific player's entered cell is correct."""
    original = puzzle_board[row][col]
    if original is None or original == 0:
        player_value = player_board[row][col]
        if player_value is not None and player_value != 0:
            return player_value == solution_board[row][col]
    return True


def get_cell_from_mouse(pos):
    """Convert mouse position to grid cell coordinates (row, col)."""
    margin_x, margin_y = get_board_position() 
    x, y = pos 

    if (margin_x <= x < margin_x + BOARD_SIZE and 
        margin_y <= y < margin_y + BOARD_SIZE):
        col = (x - margin_x) // CELL_SIZE 
        row = (y - margin_y) // CELL_SIZE 
        return row, col 

    return None


def fill_solution(puzzle_board, player_board, solution_board):
    """Fill the player board with the correct solution for empty cells."""
    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS):
            original = puzzle_board[row][col]
            solution_value = solution_board[row][col]
            # Only fill cells that were originally empty
            if original is None or original == 0:
                # Make sure we have a valid solution value
                if solution_value is not None:
                    player_board[row][col] = solution_value


# ------------------------------------------------------------
# Drawing Functions
# ------------------------------------------------------------

def draw_highlight(surface, selected_cell): 
    """Draw highlight around the selected cell.""" 
    if selected_cell is None:
        return 
    
    row, col = selected_cell  
    margin_x, margin_y = get_board_position()  
    x = margin_x + col * CELL_SIZE 
    y = margin_y + row * CELL_SIZE 
    pygame.draw.rect(surface, HIGHLIGHT_COLOR, (x, y, CELL_SIZE, CELL_SIZE))


def draw_puzzle(surface, puzzle_board, player_board, solution_board, font, show_hints=True):
    """Draw the puzzle numbers onto the grid."""
    margin_x, margin_y = get_board_position() 

    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS): 
            original_value = puzzle_board[row][col] 
            player_value = player_board[row][col]

            if original_value is not None and original_value != 0:
                value = original_value
                color = WHITE
            elif player_value is not None and player_value != 0:
                value = player_value
                if show_hints:
                    if is_cell_correct(row, col, puzzle_board, player_board, solution_board):
                        color = PLAYER_NUMBER_COLOR
                    else:
                        color = INCORRECT_COLOR
                else:
                    color = PLAYER_NUMBER_COLOR  # No hints - always green
            else:
                continue

            text_surface = font.render(str(value), True, color)
            text_rect = text_surface.get_rect()
            cell_center_x = margin_x + col * CELL_SIZE + CELL_SIZE // 2
            cell_center_y = margin_y + row * CELL_SIZE + CELL_SIZE // 2
            text_rect.center = (cell_center_x, cell_center_y)
            surface.blit(text_surface, text_rect)


def draw_grid(surface):
    """Draws the sudoku grid on the surface."""
    margin_x, margin_y = get_board_position() 

    for i in range(10):
        line_width = 4 if i % 3 == 0 else 1
        x = margin_x + i * CELL_SIZE 
        pygame.draw.line(surface, WHITE, (x, margin_y), (x, margin_y + BOARD_SIZE), line_width)
        
        y = margin_y + i * CELL_SIZE
        pygame.draw.line(surface, WHITE, (margin_x, y), (margin_x + BOARD_SIZE, y), line_width)


# ------------------------------------------------------------
# Scene Functions
# ------------------------------------------------------------

def draw_menu(surface, title_font, button_font, difficulty_buttons, hints_button, start_button):
    """Draw the main menu screen."""
    surface.fill(BLACK)
    
    # Draw title
    title_text = title_font.render('Lofi-Sudoku', True, WHITE)
    title_rect = title_text.get_rect(midtop=(SURFACE_WIDTH // 2, 40))
    surface.blit(title_text, title_rect)
    
    # Draw subtitle
    subtitle_text = button_font.render('Select Difficulty', True, GRAY)
    subtitle_rect = subtitle_text.get_rect(midtop=(SURFACE_WIDTH // 2, 100))
    surface.blit(subtitle_text, subtitle_rect)
    
    # Draw difficulty buttons
    for btn in difficulty_buttons:
        btn.draw(surface)
    
    # Draw hints toggle button
    hints_button.draw(surface)
    
    # Draw start button
    start_button.draw(surface)


def draw_game_over(surface, title_font, button_font, play_again_button, menu_button):
    """Draw the game over screen."""
    surface.fill(BLACK)
    
    # Draw congratulations message
    congrats_text = title_font.render('Congratulations!', True, CORRECT_COLOR)
    congrats_rect = congrats_text.get_rect(midtop=(SURFACE_WIDTH // 2, 80))
    surface.blit(congrats_text, congrats_rect)
    
    win_text = title_font.render('You Win!', True, WHITE)
    win_rect = win_text.get_rect(midtop=(SURFACE_WIDTH // 2, 140))
    surface.blit(win_text, win_rect)
    
    # Draw subtitle
    subtitle_text = button_font.render('Puzzle Completed Successfully', True, GRAY)
    subtitle_rect = subtitle_text.get_rect(midtop=(SURFACE_WIDTH // 2, 200))
    surface.blit(subtitle_text, subtitle_rect)
    
    # Draw buttons
    play_again_button.draw(surface)
    menu_button.draw(surface)


# ------------------------------------------------------------
# Main Game Function
# ------------------------------------------------------------

def main():
    """Main Lofi Sudoku Game Loop"""
    
    pygame.init()
    fpsClock = pygame.time.Clock() 
    DISPLAYSURF = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    pygame.display.set_caption("Lofi-Sudoku") 

    # Create font objects
    title_font = pygame.font.Font('freesansbold.ttf', 32)
    puzzle_font = pygame.font.Font('freesansbold.ttf', 21)
    button_font = pygame.font.Font('freesansbold.ttf', 18)

    # --- Game State ---
    game_state = STATE_MENU
    selected_difficulty = MEDIUM_DIFFICULTY
    show_hints = True
    
    # --- Menu Buttons ---
    button_width = 120
    button_height = 45
    button_y = 150
    button_spacing = 20
    total_width = 3 * button_width + 2 * button_spacing
    start_x = (SURFACE_WIDTH - total_width) // 2
    
    easy_btn = Button(start_x, button_y, button_width, button_height, "Easy", button_font)
    medium_btn = Button(start_x + button_width + button_spacing, button_y, button_width, button_height, "Medium", button_font, selected=True)
    hard_btn = Button(start_x + 2 * (button_width + button_spacing), button_y, button_width, button_height, "Hard", button_font)
    difficulty_buttons = [easy_btn, medium_btn, hard_btn]
    
    hints_btn = Button(SURFACE_WIDTH // 2 - 100, 230, 200, button_height, "Hints: ON", button_font)
    start_btn = Button(SURFACE_WIDTH // 2 - 80, 320, 160, 50, "Start Game", button_font)
    
    # --- Game Over Buttons ---
    play_again_btn = Button(SURFACE_WIDTH // 2 - 100, 280, 200, 50, "Play Again", button_font)
    menu_btn = Button(SURFACE_WIDTH // 2 - 100, 350, 200, 50, "Main Menu", button_font)
    
    # --- In-Game Buttons ---
    show_solution_btn = Button(SURFACE_WIDTH // 2 - 75, SURFACE_HEIGHT - 50, 150, 35, "Show Solution", button_font)
    new_game_btn = Button(SURFACE_WIDTH // 2 - 75, SURFACE_HEIGHT - 50, 150, 35, "New Game", button_font)
    
    # --- Game Variables (initialized when game starts) ---
    puzzle = None
    solution = None
    player_board = None
    selected_cell = None
    game_won = False
    solution_revealed = False  # Track if solution was shown
    
    # Title for game screen
    game_title_surface = title_font.render('Lofi-Sudoku', True, WHITE)
    game_title_rect = game_title_surface.get_rect(midtop=(SURFACE_WIDTH // 2, 15))

    # --- Main Game Loop ---- 
    while True:
        # --- Handle Events ---- 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # --- Menu State Events ---
            if game_state == STATE_MENU:
                # Handle difficulty button clicks
                if easy_btn.handle_event(event):
                    selected_difficulty = EASY_DIFFICULTY
                    easy_btn.selected = True
                    medium_btn.selected = False
                    hard_btn.selected = False
                elif medium_btn.handle_event(event):
                    selected_difficulty = MEDIUM_DIFFICULTY
                    easy_btn.selected = False
                    medium_btn.selected = True
                    hard_btn.selected = False
                elif hard_btn.handle_event(event):
                    selected_difficulty = HARD_DIFFICULTY
                    easy_btn.selected = False
                    medium_btn.selected = False
                    hard_btn.selected = True
                
                # Handle hints toggle
                if hints_btn.handle_event(event):
                    show_hints = not show_hints
                    hints_btn.text = "Hints: ON" if show_hints else "Hints: OFF"
                
                # Handle start button
                if start_btn.handle_event(event):
                    # Generate new puzzle and start game
                    puzzle, solution = create_puzzle_from_library(selected_difficulty)
                    player_board = [[0] * 9 for _ in range(9)]
                    selected_cell = None
                    game_won = False
                    solution_revealed = False
                    game_state = STATE_PLAYING
            
            # --- Playing State Events ---
            elif game_state == STATE_PLAYING:
                # Handle Show Solution button (only if solution not already revealed)
                if not solution_revealed:
                    if show_solution_btn.handle_event(event):
                        fill_solution(puzzle.board, player_board, solution.board)
                        solution_revealed = True
                else:
                    # Handle New Game button (only shown after solution is revealed)
                    if new_game_btn.handle_event(event):
                        puzzle, solution = create_puzzle_from_library(selected_difficulty)
                        player_board = [[0] * 9 for _ in range(9)]
                        selected_cell = None
                        game_won = False
                        solution_revealed = False
                
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cell = get_cell_from_mouse(event.pos) 
                        if cell:
                            row, col = cell 
                            if puzzle.board[row][col] is None or puzzle.board[row][col] == 0: 
                                selected_cell = cell 
                            else: 
                                selected_cell = None
                        else: 
                            selected_cell = None
                
                elif event.type == KEYDOWN:
                    # ESC to return to menu
                    if event.key == K_ESCAPE:
                        game_state = STATE_MENU
                    
                    elif selected_cell is not None:
                        row, col = selected_cell  

                        if event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9):
                            number = event.key - K_0
                            player_board[row][col] = number  
                        
                        elif event.key in (K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9):
                            number = event.key - K_KP0
                            player_board[row][col] = number  
                        
                        elif event.key in (K_DELETE, K_BACKSPACE, K_0, K_KP0):
                            player_board[row][col] = 0
            
            # --- Game Over State Events ---
            elif game_state == STATE_GAME_OVER:
                if play_again_btn.handle_event(event):
                    # Start a new game with same settings
                    puzzle, solution = create_puzzle_from_library(selected_difficulty)
                    player_board = [[0] * 9 for _ in range(9)]
                    selected_cell = None
                    game_won = False
                    solution_revealed = False
                    game_state = STATE_PLAYING
                
                elif menu_btn.handle_event(event):
                    game_state = STATE_MENU
        
        # --- Update Game State ---
        # Only check for win if solution wasn't revealed (no cheating!)
        if game_state == STATE_PLAYING and not game_won and not solution_revealed:
            if puzzle and is_board_complete(puzzle.board, player_board):
                if check_solution(puzzle.board, player_board, solution.board):
                    game_won = True
                    game_state = STATE_GAME_OVER
        
        # --- Draw Game State ---- 
        DISPLAYSURF.fill(BLACK)
        
        if game_state == STATE_MENU:
            draw_menu(DISPLAYSURF, title_font, button_font, difficulty_buttons, hints_btn, start_btn)
        
        elif game_state == STATE_PLAYING:
            draw_highlight(DISPLAYSURF, selected_cell) 
            draw_grid(DISPLAYSURF)
            draw_puzzle(DISPLAYSURF, puzzle.board, player_board, solution.board, puzzle_font, show_hints)
            DISPLAYSURF.blit(game_title_surface, game_title_rect)
            
            # Draw appropriate button based on state
            if solution_revealed:
                # Show "New Game" button and message after solution is revealed
                new_game_btn.draw(DISPLAYSURF)
                revealed_text = button_font.render("Solution Revealed", True, GRAY)
                revealed_rect = revealed_text.get_rect(midtop=(SURFACE_WIDTH // 2, SURFACE_HEIGHT - 80))
                DISPLAYSURF.blit(revealed_text, revealed_rect)
            else:
                # Show "Show Solution" button during normal play
                show_solution_btn.draw(DISPLAYSURF)
            
            # Show hint status in corner
            hint_status = button_font.render(f"Hints: {'ON' if show_hints else 'OFF'}", True, GRAY)
            DISPLAYSURF.blit(hint_status, (10, SURFACE_HEIGHT - 30))
            
            # Show ESC instruction
            esc_text = button_font.render("ESC: Menu", True, GRAY)
            DISPLAYSURF.blit(esc_text, (SURFACE_WIDTH - 100, SURFACE_HEIGHT - 30))
        
        elif game_state == STATE_GAME_OVER:
            draw_game_over(DISPLAYSURF, title_font, button_font, play_again_btn, menu_btn)

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == "__main__":
    main()
