import random 

EASY_DIFFICULTY = 0.3 
MEDIUM_DIFFICULTY = 0.4 
HARD_DIFFICULTY = 0.5 

def generate_solved_puzzle() -> list[list[int]]:
    """Generate a solved and valid sudoku puzzle using backtracking algorithm.
     TODO: Implement this function.
    """ 

    pass 


def create_puzzle(grid:list[list[int]], difficulty:int=40) -> list[list[int]]:
    """Create a new puzzle from a solved puzzle grid with a given difficulty.
     TODO: Implement this function.
    """

    pass

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