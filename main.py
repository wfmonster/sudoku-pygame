import pygame
import sys

# contains constants for the pygame library
from pygame.locals import *
from constants import WHITE, BLACK, SURFACE_HEIGHT, SURFACE_WIDTH, FPS
from generate_puzzle import create_puzzle_from_library

# grid constants 
NUM_CELLS = 9 
CELL_SIZE = 36 
BOARD_SIZE = CELL_SIZE * NUM_CELLS 

# colors for highlighting and player numbers
HIGHLIGHT_COLOR = (70, 130, 180) 
PLAYER_NUMBER_COLOR = (100, 200, 100)  


def get_board_position():
    "Calculate the top-left position of the board for centering."

    margin_x = (SURFACE_WIDTH - BOARD_SIZE)//2
    margin_y = (SURFACE_HEIGHT - BOARD_SIZE)//2
    return margin_x, margin_y

def get_cell_from_mouse(pos):
    """Convert mouse position to grid cell coordinates (row, col).
    Returns none if click is outside of the board grid.
    """ 
    margin_x, margin_y = get_board_position() 
    x, y = pos 

    # check if click is within the board grid. 
    if (margin_x <= x < margin_x + BOARD_SIZE and 
        margin_y <= y < margin_y + BOARD_SIZE):
        col = (x - margin_x) // CELL_SIZE 
        row = (y - margin_y) // CELL_SIZE 
        return row, col 

    return None

def draw_highlight(surface, selected_cell): 
    """Draw highlight around the selected cell.""" 

    if selected_cell is None:
        return 
    
    row, col = selected_cell  
    margin_x, margin_y = get_board_position()  

    # calculate the cell rectangle. 
    x = margin_x + col * CELL_SIZE 
    y = margin_y + row * CELL_SIZE 

    # Draw filled rectangle around the cell. 
    pygame.draw.rect(surface, HIGHLIGHT_COLOR, (x, y, CELL_SIZE, CELL_SIZE))



def draw_puzzle(surface, puzzle_board, player_board, font):
    """Draw the puzzle numbers onto the grid."""

    margin_x, margin_y = get_board_position() 

    # draw the sudoku grid
    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS): 
            original_value = puzzle_board[row][col] 
            player_value = player_board[row][col]

            # Determine what to display and what color
            if original_value is not None and original_value != 0:
                # Original puzzle number (not editable)
                value = original_value
                color = WHITE
            elif player_value is not None and player_value != 0:
                # Player-entered number
                value = player_value
                color = PLAYER_NUMBER_COLOR
            else:
                continue  # Empty cell

            # render the current number in the cell 
            text_surface = font.render(str(value), True, color)
            text_rect = text_surface.get_rect()

            # Center the number inside of the cell. 
            cell_center_x = margin_x + col * CELL_SIZE + CELL_SIZE // 2
            cell_center_y = margin_y + row * CELL_SIZE + CELL_SIZE // 2
            text_rect.center = (cell_center_x, cell_center_y)
            surface.blit(text_surface, text_rect)
 

def draw_grid(surface):
    """Draws the sudoku grid on the surface"""
   
    margin_x, margin_y = get_board_position() 

    for i in range(10):
        # Use thicker lines for 3x3 box boundaries
        line_width = 4 if i % 3 == 0 else 1
        # draw a vertical line 
        x = margin_x + i * CELL_SIZE 
        pygame.draw.line(surface, WHITE, (x, margin_y), (x, margin_y + BOARD_SIZE), line_width)
        
        # draw horizontal lines
        y = margin_y + i * CELL_SIZE
        pygame.draw.line(surface, WHITE, (margin_x, y), (margin_x + BOARD_SIZE, y), line_width)


def main():
    """Main Lofi Sudoku Game Loop"""
    
    pygame.init()
    fpsClock = pygame.time.Clock() 
    # returns a surface object representing the display window
    DISPLAYSURF = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))
    # sets the window title bar
    pygame.display.set_caption("Lofi-Sudoku") 

    # create font objects for the title and puzzle
    title_font = pygame.font.Font('freesansbold.ttf', 32)
    puzzle_font = pygame.font.Font('freesansbold.ttf', 21)

    # draw the title of the game onto the surface.
    text_surface = title_font.render('Lofi-Sudoku', True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (SURFACE_WIDTH//2, 5)

    # Generate a puzzle and solution
    puzzle, solution = create_puzzle_from_library() 

    # create an representation of the players board.  
    player_board = [[0] * 9 for _ in range(9)]

    # track the currently selected cell. 
    selected_cell = None
    
    # creates the main game loop
    # handles events, updates game state and draws the game state to the window
    while True:
        # clears screen and prevents ghosting / overdraw 
        DISPLAYSURF.fill(BLACK)
    
        # --- Handle Events ---- 
        # checks for events which is an object 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # handles mouse clicks for selecting cells. 
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1: # left mouse click 
                    cell = get_cell_from_mouse(event.pos) 
                    if cell:
                        row, col = cell 
                        if puzzle.board[row][col] is None or puzzle.board[row][col] == 0: 
                            selected_cell = cell 
                        else: 
                            selected_cell = None # user clicked on a fixed cell. 
                    else: 
                        selected_cell = None # user clicked outside of the board.
            elif event.type == KEYDOWN:
                if selected_cell is not None:
                    row, col = selected_cell  

                    # handle number keys 1-9 
                    if event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9):
                        number = event.key - K_0 # convert key to number. 
                        # print(number)
                        player_board[row][col] = number  
                    
                    # handles numberpad keys 1-9 
                    elif event.key in (K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9):
                        number = event.key - K_KP0 # convert key to number. 
                        player_board[row][col] = number  
                    
                    # handles backspace key 
                    elif event.key in (K_DELETE, K_BACKSPACE, K_0, K_KP0):
                        player_board[row][col] = 0  
                    
        # --- Draw Game State ---- 
        draw_highlight(DISPLAYSURF, selected_cell) 
        draw_grid(DISPLAYSURF)
        draw_puzzle(DISPLAYSURF, puzzle.board, player_board, puzzle_font)
        #adds the title surface to the display surface.
        DISPLAYSURF.blit(text_surface, text_rect)

        # draws the surface object returned by display.set_mode() to the screen
        # happens once per frame
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
