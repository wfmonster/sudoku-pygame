import random 

EASY_DIFFICULTY = 0.3 
MEDIUM_DIFFICULTY = 0.4 
HARD_DIFFICULTY = 0.5 

import random

def generate_solved_grid():
    """Generate a complete valid Sudoku grid using backtracking."""
    grid = [[0] * 9 for _ in range(9)]
    
    def is_valid(grid, row, col, num):
        # Check row
        if num in grid[row]:
            return False

        # Check column
        if num in [grid[i][col] for i in range(9)]:
            return False
            
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if grid[i][j] == num:
                    return False
        return True
    
    def solve(grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)  # Randomize for variety
                    for num in nums:
                        if is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if solve(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True
    
    solve(grid)
    return grid


def create_puzzle(grid, difficulty=40):
    """Remove numbers from solved grid to create a puzzle.
    
    difficulty: determined by the number of cells removed from the grid.
    - Easy: 30-35 removed
    - Medium: 40-45 removed
    - Hard: 50-55 removed
    """
    puzzle = [row[:] for row in grid]  # Deep copy
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    
    for i in range(difficulty):
        row, col = cells[i]
        puzzle[row][col] = 0
    
    return puzzle


def create_puzzle_from_library():
    """
    Uses the py-sudoku library to generate puzzles.
    Docs: https://pypi.org/project/py-sudoku/
    """
    from sudoku import Sudoku 
    # initializes a puzzle with a 3x3 subgrid and given difficulty.
    puzzle = Sudoku(3).difficulty(MEDIUM_DIFFICULTY)
    solution = puzzle.solve()
    return puzzle, solution



if __name__ == "__main__":
    # solved = generate_solved_puzzle()
    # puzzle = create_puzzle(solved, difficulty=MEDIUM_DIFFICULTY*100)
    # print(puzzle)

    puzzle, solution = create_puzzle_from_library()
    print(puzzle.board)
    print(solution.board)
    puzzle.show()
    solution.show()