import pygame
import sys

# contains constants for the pygame library
from pygame.locals import *
from constants import WHITE, SURFACE_HEIGHT, SURFACE_WIDTH


def draw_grid(surface):
    # draw a 9 by 9 sudoku grid using 25px squares with a 2px width line
    num_cells = 9
    cell_size = 30 
    board_size = cell_size * num_cells
    margin_x = (SURFACE_WIDTH - board_size)//2
    margin_y = (SURFACE_HEIGHT - board_size)//2  

    # Use thicker lines for 3x3 box boundaries
    for i in range(10):
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
    # returns a surface object representing the display window
    DISPLAYSURF = pygame.display.set_mode((SURFACE_HEIGHT, SURFACE_WIDTH))

    # sets the window title bar
    pygame.display.set_caption("Sudoku") 
    
    # creates the main game loop
    # handles events, updates game state and draws the game state to the window
    while True:
        # checks for events which is an object 
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        draw_grid(DISPLAYSURF)

        # draws the surface object returned by display.set_mode() to the screen
        # happens once per frame
        pygame.display.update()

if __name__ == "__main__":
    main()
