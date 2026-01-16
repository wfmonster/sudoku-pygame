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


def draw_puzzle(surface, puzzle_board, font):
    """Draw the puzzle numbers onto the grid."""

    margin_x, margin_y = get_board_position() 

    # draw the sudoku grid
    for row in range(NUM_CELLS):
        for col in range(NUM_CELLS): 
            value = puzzle_board[row][col] 

            # skip if it is an empty cell. 
            if value is None or value == 0:
                continue 

            # render the current number in the cell 
            text_surface = font.render(str(value), True, WHITE)
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
    
    # creates the main game loop
    # handles events, updates game state and draws the game state to the window
    while True:
        # prevents ghosting / overdraw 
        DISPLAYSURF.fill(BLACK)
        #adds the title surface to the display surface.
        DISPLAYSURF.blit(text_surface, text_rect)

        # checks for events which is an object 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        
        draw_grid(DISPLAYSURF)
        draw_puzzle(DISPLAYSURF, puzzle.board, puzzle_font)

        # draws the surface object returned by display.set_mode() to the screen
        # happens once per frame
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
