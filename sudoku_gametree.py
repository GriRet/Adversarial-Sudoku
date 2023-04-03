"""
The gametree for the sudoku algorithm.
This file contains a generation function and corresponding helper functions to generate a n layer gametree of the
current sudoku board
"""
from __future__ import annotations
from typing import Optional
from math import sqrt
# from python_ta.contracts import check_contracts

import sudoku_setup as setup
from adversarial_sudoku import copy_board

MAX_STEP = 81


# @check_contracts
class GameTree:
    """
    The gametree for the sudoku algorithm

    Representation Invariants:
    - parent is None or self in self.parent.subtrees
    """
    move: Optional[tuple[tuple[int, int], int]]
    prev_solution: Optional[list[list[int]]]
    parent: Optional[GameTree]
    guesser_win_probability: float = -1.0
    adversary_lose_probability: float = 2
    subtrees: list[GameTree]
    current_board: list[list[int]]

    def __init__(self, board: list[list[int]],
                 parent: GameTree = None,
                 move: tuple[tuple[int, int], int] = None,
                 solution: list[list[int]] = None) -> None:
        """Initialize a new GameTree"""
        self.subtrees = []
        self.parent = parent
        self.move = move
        self.prev_solution = solution
        self.current_board = copy_board(board)

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self.subtrees

    def __len__(self) -> int:
        """Return the number of items in this tree."""
        # Note: no "empty tree" base case is necessary here.
        # Instead, the only implicit base case is when there are no subtrees (sum returns 0).
        return 1 + sum(subtree.__len__() for subtree in self.subtrees)


def generate_gametree(layer: int, move: tuple[tuple[int, int], int] | None, solution: list[list[int]] | None,
                      board_old: list[list[int]], step: int, parent: GameTree | None = None) -> GameTree:
    """This function generate the gametree with fixed layer"""
    board = copy_board(board_old)
    game_tree = GameTree(board, parent, move, solution)
    if layer > 0:
        # Find possible cells and values for the guesser
        moves = []
        possible_cells = order_cells(board)
        for i in range(min(len(possible_cells), 5)):
            values = get_available_numbers(board, possible_cells[i][0])
            moves += [(possible_cells[i][0], value) for value in values]

        # Find possible solutions for the adversary
        possible_solutions = setup.find_multiple_solutions(board, len(board))
        score_solution = [0 for _ in range(len(possible_solutions))]
        score_move = [0 for _ in range(len(moves))]
        for i in range(len(possible_solutions)):
            for j in range(len(moves)):
                if moves[j][1] == possible_solutions[i][moves[j][0][0]][moves[j][0][1]]:
                    score_solution[i] += 1
                    score_move[j] += 1
                    new_board = copy_board(board)
                    new_board[moves[j][0][0]][moves[j][0][1]] = moves[j][1]
                    possible_cells = order_cells(new_board)
                    coord = possible_cells[0][0]
                    new_board[coord[0]][coord[1]] = possible_solutions[i][coord[0]][coord[1]]
                    game_tree.subtrees.append(generate_gametree(layer - 1, moves[j], possible_solutions[i],
                                                                new_board, step + 1, game_tree))
        total = sum(score_solution)
        if game_tree.subtrees:
            for subtree in game_tree.subtrees:
                if subtree.subtrees:
                    sub_sol_prob = 0
                    sub_move_prob = 0
                    sub_length = len(subtree.subtrees)
                    for subsubtree in subtree.subtrees:
                        sub_sol_prob += subsubtree.adversary_lose_probability
                        sub_move_prob += subsubtree.guesser_win_probability
                    ave_sol = sub_sol_prob / sub_length
                    ave_move = sub_move_prob / sub_length
                else:
                    ave_sol, ave_move = 1, 1
                for i in range(len(score_solution)):
                    if subtree.prev_solution == possible_solutions[i]:
                        subtree.adversary_lose_probability = (score_solution[i] / total) * ave_sol
                for j in range(len(score_move)):
                    if subtree.move == moves[j]:
                        subtree.guesser_win_probability = (score_move[j] / total) * ave_move
    return game_tree


def order_cells(board: list[list[int]]) -> list[tuple[tuple[int, int], int]]:
    """
    Order the empty cells by their degree from lowest to highest
    degree = number of empty cells in the same row + column + block
    """
    unordered = []
    index = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                unordered.append(((i, j), find_degree(board, (i, j))))
                index += 1

    unordered.sort(key=lambda tup: tup[1])
    return unordered


def find_degree(board: list[list[int]], position: tuple[int, int]) -> int:
    """
    Find the degree of the given cell
    """
    count = 0
    for k in range(len(board)):
        if board[position[0]][k] == 0:
            count += 1
        if board[k][position[1]] == 0:
            count += 1

    block_length = int(sqrt(len(board)))
    start_r = position[0] // block_length
    start_c = position[1] // block_length

    for i in range(start_r, start_r + block_length):
        for j in range(start_c, start_c + block_length):
            if board[i][j] == 0:
                count += 1

    return count


def get_available_numbers(board: list[list[int]], position: tuple[int, int]) -> set[int]:
    """helper function to check row, column and block avaliability"""
    number_set = set(range(1, len(board) + 1))

    for i in range(len(board)):
        num = board[i][position[1]]
        if num in number_set:
            number_set.remove(num)
    for j in range(len(board)):
        num = board[position[0]][j]
        if num in number_set:
            number_set.remove(num)

    block_length = int(sqrt(len(board)))
    start_r = block_length * (position[0] // block_length)
    start_c = block_length * (position[1] // block_length)

    for i in range(start_r, start_r + block_length):
        for j in range(start_c, start_c + block_length):
            num = board[i][j]
            if num in number_set:
                number_set.remove(num)

    return number_set

# if __name__ == '__main__':
#     import doctest
#
#     doctest.testmod(verbose=True)
#
#     import python_ta
#
#     python_ta.check_all(config={
#         'max-line-length': 120,
#         'max-nested-blocks': 10
#     })
