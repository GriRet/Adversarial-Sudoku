"""set up a sudoku game.

The abbreviations and short names used in this project are:
    - n: presenting the initiated number
    - b: the short for the base number of the initiated number
    - r: the short for the row
    - c: the short for the column
    - g: presenting the block; the short for a grid which may be used to describe a block
    - d: the digit in a cell; the digit in a row; the digit in a coloumn; the digit in a block
    - p: the short for the position of a cell
"""
import math  # we used math.isqrt and math.sqrt
import random  # We used random.sample

# import List from typing  # may use List[List[int]]

# import sudoku_solution as sol  # may be used for testing solutions
# import StartMenu as sm  # may be used for testing visualising


################################################################################
# Constants that may be called
################################################################################
# will be used for setting up the game
UNFILLED = 0  # the unfilled digit in cells

# will be used for printing
EMPTY_MARK = '.'  # only used when call `print` for view and test purpose in console

# may be used as constants for testing
INITIATED_NUMBER = 9  # by using `get_initiated_number(9)`
BASE = 3  # by using `get_base_number(9)`, the sudoku game's base number or initiated number


################################################################################
# Generating numbers
################################################################################
def get_initiated_number(n: int | float) -> int:
    """
    Find the initiate number for a board_size n.
    """
    if is_initiated_number(n):
        return n
    else:
        b = get_base_number(n)
        return b * b


def get_base_number(n: int | float) -> int:
    """
    Find the sqrt of n if n can be expressed as a^2 where a belongs to N
    """
    return round(math.isqrt(n))


################################################################################
# Tool functions
################################################################################
# This is a new function.
def find_empty(puzzle: list[list[int]]) -> tuple[int, int] | None:
    """
    Find the first empty cell in the puzzle board
    """
    for r in range(len(puzzle)):  # row
        for c in range(len(puzzle[0])):  # column
            if puzzle[r][c] == 0:  # 0 means empty cell
                return (r, c)  # return the position of the empty cell

    return None  # if no empty cell is found


# # This is a new function.
def solve(puzzle: list[list[int]], n: int = 9) -> bool:
    """Return whether or not a puzzle has at least one solution.
    The function `find_multiple_solutions` is used for seeking multiple solutions.

    Returns:
        - False: if no digit can be filled in the cell.
        - True: fill the first appeared digit in the range of (1, n + 1) in the cell.

    Preconditions:
        - n > 0
    """
    # n = ...

    empty = find_empty(puzzle)
    if not empty:
        return True
    else:
        r, c = empty

    for d in range(1, n + 1):  # d is digit
        if is_position_valid((r, c), puzzle, d):
            puzzle[r][c] = d  # if the digit is valid, then fill in the cell

            if solve(puzzle):  # early return after filled in
                return True

            puzzle[r][c] = 0  # if the digit is not valid, reset to 0 (empty)

    return False  # no digit can be filled in


# This is a new function.
# Here the solutions may be designed as a set, but for now it is a list.
def find_multiple_solutions(puzzle: list[list[int]], n: int = 9) -> list[list[list[int]]]:
    """Return all possible solutions, with the use of a helper _solve_recursive.
    """
    # n = ...
    solutions = []
    _solve_recursive(puzzle, solutions, n)

    # print solutions for easily view
    # for i, solution in enumerate(solutions):  # i is the number of current solution
    #     print(f"Solution {i + 1}:")
    #     for row in solution:
    #         print(row)
    #     print()  # empty line

    return solutions


# This is a new function.
def _solve_recursive(puzzle, solutions, n: int = 9) -> None:
    """A helper function for find_multiple_solutions that gives a solution by checking wether
    an empty cell on the board.
    """

    # Find the first empty cell in the puzzle
    for row in range(n):
        for col in range(n):
            if puzzle[row][col] == 0:
                # Try all possible values for the cell
                for val in range(1, n + 1):
                    puzzle[row][col] = val
                    # Check if the value is valid and continue recursively
                    if is_position_valid((row, col), puzzle, n):
                        _solve_recursive(puzzle, solutions, n)
                # Reset the value of the cell if no valid value was found
                puzzle[row][col] = 0
                return

    # If no empty cell was found, add the solved puzzle to the list of solutions
    solutions.append([row[:] for row in puzzle])


################################################################################
# Checker functions
################################################################################
def is_initiated_number(n: int | float = 9) -> bool:
    """Return whether the given number can be used to create a sudoku game.

    Variables:
        - The `n` is a positive integer or a positive float that can be input by the sudoku user.
    Returns:
        - return `True` if the given number `n` can be used for a sudoku game
        - return `False` if the given number `n` can *not* be used for a sudoku game

    Preconditions:
        - n > 0
    """
    # n = ...
    if type(n) == int and math.isqrt(n) == math.sqrt(n):
        return True
    else:
        print("The given number can not be used to create a sudoku game.")
        # f'You may consider using {get_initiated_number(n)} as a initiated number.'
        return False


# These functions may not be used.
# def is_digit_valid(n: int, d: int, puzzle: list[list[int]], r, c) -> bool:
#     """Check if digit is applicable in corresponding row, column and block.
#     If the digit is applicable, then it can be safely filled in the corresponding **cell**.
#
#     Variables:
#         - n is the initiated number
#         - d is the digit that need to be checked if applicable
#         - puzzle is a game board (also works for an answer/solution board)
#         - r is the corresponding row
#         - c is the corresponding column
#
#     Returns:
#         - Return `True` if the digit is applicable in corresponding row, column and block
#         - Return `False` if the digit is *not* applicable in **either** corresponding row, column and block
#
#     Preconditions:
#         - n > 0
#         - d in range(1, n + 1)
#         - r in range(1, n + 1)
#         - c in range(1, n + 1)
#     """
#     if not _is_digit_row_valid(d, puzzle, r):
#         print('the digit appears in same row')
#         return False
#     elif not _is_digit_column_valid(n, d, puzzle, c):
#         print('the digit appears in same column')
#         return False
#     elif not _is_digit_block_valid(n, d, puzzle, r, c):
#         print('the digit appears in same block')
#         return False
#     else:
#         return True
#
#
# def _is_digit_row_valid(d: int, puzzle: list[list[int]], r) -> bool:
#     """Check if digit is applicable in corresponding row, column and block.
#     If the digit is applicable, then it can be safely filled in the corresponding row.
#
#     Variables:
#         - d: the digit that need to be checked if applicable
#         - puzzle: a game board (also works for an answer/solution board)
#         - r: the corresponding row
#
#     Returns:
#         - Return `True` if the digit *not* appears in same row
#         - Return `False` if digit appears in same row
#
#     Preconditions:
#         - d in range(1, INITIATED_NUMBER + 1)
#         - r in range(1, INITIATED_NUMBER + 1)
#     """
#     if d in puzzle[r]:
#         print('the digit appears in same row')
#         return False
#     else:
#         return True
#
#
# def _is_digit_column_valid(n: int, d: int, puzzle: list[list[int]], c) -> bool:
#     """Check if digit is applicable in corresponding row, column and block.
#     If the digit is applicable, then it can be safely filled in the corresponding column.
#
#     Variables:
#         - d is the digit that need to be checked if applicable
#         - puzzle is a game board (also works for an answer/solution board)
#         - c is the corresponding column
#
#     Returns:
#         - Return `True` if the digit *not* appears in same column
#         - Return `False` if the digit appears in same column
#
#     Preconditions:
#         - n > 0
#         - d in range(1, INITIATED_NUMBER + 1)
#         - c in range(1, INITIATED_NUMBER + 1)
#     """
#     if d in [puzzle[i][c] for i in range(n)]:
#         print('the digit appears in same column')
#         return False
#     else:
#         return True
#
#
# def _is_digit_block_valid(n: int, d: int, puzzle: list[list[int]], r, c) -> bool:
#     """Check if the given digit is applicable in corresponding row, column and block.
#     If the digit is applicable, then it can be safely filled in the corresponding block.
#
#     Variables:
#         - d is the digit that need to be checked if applicable
#         - puzzle is a game board (also works for an answer/solution board)
#         - r is the corresponding row
#         - c is the corresponding column
#
#     Returns:
#         - Return `True` if the digit *not* appears in same block
#         - Return `False` if the digit appears in same block
#
#     Preconditions:
#         - n > 0
#         - d in range(1, n + 1)
#         - r in range(1, n + 1)
#         - c in range(1, n + 1)
#     """
#     b = get_base_number(n)
#     subgrid_row = (r // b) * b
#     subgrid_col = (c // b) * b
#
#     for i in range(b):
#         for j in range(b):
#             if puzzle[subgrid_row + i][subgrid_col + j] == d:
#                 print('the digit appears in same block')
#                 return False
#     else:
#         return True


# This is a new function.
def is_position_valid(p: tuple[int, int], puzzle: list[list[int]], n: int = 9) -> bool:
    """
    Check if the position is a valid position
    """
    r, c = p

    # Check if the value in the cell is valid (between 1 and n)
    if puzzle[r][c] < 1 or puzzle[r][c] > n:
        return False

    # Check if the value in the cell is already present in the same row
    for i in range(n):
        if i != c and puzzle[r][i] == puzzle[r][c]:
            return False

    # Check if the value in the cell is already present in the same column
    for i in range(n):
        if i != r and puzzle[i][c] == puzzle[r][c]:
            return False

    # Check if the value in the cell is already present in the same block
    b = get_base_number(n)
    block_r = (r // b) * b
    block_c = (c // b) * b
    for i in range(block_r, block_r + b):
        for j in range(block_c, block_c + b):
            if (i, j) != p and puzzle[i][j] == puzzle[r][c]:
                return False

    # If none of the checks failed, then the position is valid
    return True


def is_valid_solution(puzzle: list[list[int]], n: int = 9) -> bool:
    """
    Check if the solution has any contradiction with
    """
    # Check each row
    for row in range(n):
        if len(set(puzzle[row])) != n:
            return False

    # Check each column
    for col in range(n):
        if len(set([puzzle[row][col] for row in range(n)])) != n:
            return False

    # Check each block
    b = get_base_number(n)
    for block_r in range(b):
        for block_c in range(b):
            if len(set([puzzle[row][col] for row in range(block_r * b, (block_r + 1) * b)
                        for col in range(block_c * b, (block_c + 1) * b)])) != n:
                return False

    # If all checks pass, then the solution is valid
    return True


################################################################################
# Generating sudoku game
################################################################################
def generate_sudoku(n: int = 9) -> list[list[int]]:
    """
    Generate an appropriate sudoku with board length n
    """
    if not is_initiated_number(n):
        raise ValueError("The given number can not be used to create a sudoku game.")

    b = get_base_number(n)
    rows = [d * b + r for d in _shuffle(range(b)) for r in _shuffle(range(b))]
    cols = [d * b + c for d in _shuffle(range(b)) for c in _shuffle(range(b))]
    nums = _shuffle(range(1, n + 1))

    # produce board using randomized baseline pattern
    board = [[nums[_pattern(r, c, n)] for c in cols] for r in rows]
    return board


def _pattern(r: int, c: int, n: int = 9) -> int:
    """A helper function for `generate_sudoku`, TODO
    Preconditions:
        - n > 0
        - r > 0
        - c > 0
    """
    b = get_base_number(n)
    return (b * (r % b) + r // b + c) % n


def _shuffle(s: any) -> list:
    """A helper function for `generate_sudoku`, generating ranodm digits.

    Preconditions:
        - s >= 0
    """
    return random.sample(s, len(s))


def generate_puzzle(percentage: int | float = 50, n: int = 9) -> list[list[int]]:
    """Genreate a sudoku puzzle for playing. The percentage reflecting the difficulty of the puzzle.
    Percentage can be changed for a difficulty level.

    Variables:
        - n: the initiated number
        - percentage: the percentage of **empty cells**

    Returns:
        - a sudoku puzzle in the form `list[list[int]]`

    Preconditions:
        - n > 0
        - percentage >= 0 and percentage <= 1
    """
    board = generate_sudoku(n)
    total_cells = n * n
    # percentage = ...  # percentage of empty cells

    empties = round(total_cells * percentage * 0.01)  # total empty cells
    # print(empties)  # used for check the number of empty cells

    # Randomly generate empty cells
    for empty_position in random.sample(range(total_cells), empties):
        board[empty_position // n][empty_position % n] = 0  # 商是行数，余数是列数

    # Print the puzzle to view
    num_size = len(str(n))
    for row in board:
        print(*(f"{n or '.':{num_size}} " for n in row))

    return board


if __name__ == "__main__":
    pass
