import pygame
import sys

# contains constants for the pygame library
from pygame.locals import *
from constants import WHITE, SURFACE_HEIGHT, SURFACE_WIDTH, FPS
from generate_puzzle import create_puzzle_from_library

def draw_puzzle(surface, puzzle):
    """Loads a puzzle from a file"""

    # will probably need a font object to draw the numbers. 
    fontobj = pygame.font.Font('freesansbold.ttf', 32)

    # figure out where to place the numbers on the surface.
    # number should be centered in the cell.
    # based on the size of the surface, location of the board and each cell.
    return puzzle

def draw_grid(surface):
    """Draws the sudoku grid on the surface"""
    # draw a 9 by 9 sudoku grid using 25px squares with a 2px width line
    num_cells = 9
    cell_size = 30 
    board_size = cell_size * num_cells
    # calculate the margin for the board to be centered
    margin_x = (SURFACE_WIDTH - board_size)//2
    margin_y = (SURFACE_HEIGHT - board_size)//2  

    # draw the sudoku grid
    for i in range(10):
        # Use thicker lines for 3x3 box boundaries
        line_width = 4 if i % 3 == 0 else 1
        # draw a vertical line 
        x = margin_x + i * cell_size 
        pygame.draw.line(surface, WHITE, (x, margin_y), (x, margin_y + num_cells * cell_size), line_width)
        
        # draw horizontal lines
        y = margin_y + i * cell_size
        pygame.draw.line(surface, WHITE, (margin_x, y), (margin_x + num_cells * cell_size, y), line_width)


def main():
    """Main Sudoku Game Loop"""
    
    pygame.init()
    fpsClock = pygame.time.Clock() 
    # returns a surface object representing the display window
    DISPLAYSURF = pygame.display.set_mode((SURFACE_HEIGHT, SURFACE_WIDTH))

    # sets the window title bar
    pygame.display.set_caption("Lofi-Sudoku") 

    # draw the title of the game onto the surface.
    title_font = pygame.font.Font('freesansbold.ttf', 32)
    text_surface = title_font.render('Lofi-Sudoku', antialiased=True, color=WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (SURFACE_WIDTH/2, 10)
    DISPLAYSURF.blit(text_surface, text_rect)
    
    # creates the main game loop
    # handles events, updates game state and draws the game state to the window
    while True:
        #adds the title surface to the display surface.
        DISPLAYSURF.blit(text_surface, text_rect)

        # checks for events which is an object 
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        puzzle, solution = create_puzzle_from_library() 
        # draw the puzzle and solution on the surface   
        
        draw_grid(DISPLAYSURF)
        # draw_puzzle(DISPLAYSURF, puzzle.board)

        # draws the surface object returned by display.set_mode() to the screen
        # happens once per frame
        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
