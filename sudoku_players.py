"""..."""
from __future__ import annotations

import random
from typing import Optional

# from python_ta.contracts import check_contracts

import sudoku_setup as setup
from adversarial_sudoku import AdversarialSudoku, copy_board
from sudoku_gametree import GameTree, generate_gametree, order_cells, get_available_numbers

layer = 3


class Guesser:
    """An abstract class representing a Guesser player in Adversarial Wordle.

    This class can be subclassed to implement different strategies for the Guesser player.
    """

    def make_move(self, game: AdversarialSudoku) -> tuple[tuple[int, int], int]:
        """Return a guess given the current game.

        Preconditions:
        - game.is_guesser_turn()
        """
        raise NotImplementedError


class NormalGuesser(Guesser):
    """A Guesser player that always picks a random word that is consistent with past
    guesses and statuses.
    """

    def make_move(self, game: AdversarialSudoku) -> tuple[tuple[int, int], int]:
        """Return a guess given the current game.
        """
        moves = []
        possible_cells = order_cells(game.current_board)
        for i in range(min(len(possible_cells), 5)):
            values = get_available_numbers(game.current_board, possible_cells[i][0])
            moves += [(possible_cells[i][0], value) for value in values]
        return random.choice(list(moves))


# @check_contracts
class GreedyTreeGuesser(Guesser):
    """
    An Adversarial Guesser that plays greedily based on a given GameTree.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves. If None, then this
    #       player just makes random moves.
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree = None) -> None:
        """Initialize this player."""

        self._game_tree = game_tree

    def make_move(self, game: AdversarialSudoku) -> tuple[tuple[int, int], int]:
        """Make a move given the current game.

        Preconditions:
            - game.is_guesser_turn()
        """
        if not game.statuses:
            self._game_tree = generate_gametree(layer, None, None, game.current_board, 0, None)
        else:
            self._game_tree = generate_gametree(layer, self._game_tree.move, self._game_tree.prev_solution,
                                                game.current_board, len(game.guesses), self._game_tree)
        possible_subtrees = self._game_tree.get_subtrees()
        record_subs = [possible_subtrees[0]]
        for i in range(1, len(possible_subtrees)):
            if possible_subtrees[i].guesser_win_probability > record_subs[0].guesser_win_probability:
                record_subs = [possible_subtrees[i]]
            elif possible_subtrees[i].guesser_win_probability == record_subs[0].guesser_win_probability:
                record_subs.append(possible_subtrees[i])
        record_sub = random.choice(record_subs)
        self._game_tree = record_sub
        return self._game_tree.move


################################################################################
# Adversary player classes
################################################################################
class Adversary:
    """An abstract class representing an Adversary player in Adversarial Wordle.

    This class can be subclassed to implement different strategies for the Adversary player.
    """

    def make_move(self, game: AdversarialSudoku) -> tuple[list[list[int]], list[list[int]]]:
        """Return a status given the current game.

        Preconditions:
        - not game.is_guesser_turn()
        """
        raise NotImplementedError


class NormalAdversary(Adversary):
    """An Adversary player that always picks a random answer consistent with the previous rounds.
    Avoids picking the most recent guess whenever possible.
    """

    def make_move(self, game: AdversarialSudoku) -> tuple[list[list[int]], list[list[int]]]:
        """Return a status given the current game.
        """
        # Select a random answer and return the corresponding status
        possible_solutions = setup.find_multiple_solutions(game.current_board, len(game.current_board))
        solution_chosen = random.choice(possible_solutions)
        coord = game.guesses[-1][0]
        value = game.guesses[-1][1]
        if game.get_status_for_answer(game.guesses[-1], solution_chosen):
            new_board = copy_board(game.current_board)
            new_board[coord[0]][coord[1]] = value
            possible_cells = order_cells(new_board)
            coord = possible_cells[0][0]
            new_board[coord[0]][coord[1]] = solution_chosen[coord[0]][coord[1]]
        else:
            new_board = copy_board(game.current_board)
        return (solution_chosen, new_board)


class GreedyTreeAdversary(Adversary):
    """
    An Adversarial Adversary that plays greedily based on a given GameTree.
    """
    # Private Instance Attributes:
    #   - _game_tree:
    #       The GameTree that this player uses to make its moves.
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree | None = None) -> None:
        """Initialize this player."""

        self._game_tree = game_tree

    def make_move(self, game: AdversarialSudoku) -> tuple[list[list[int]], list[list[int]]]:
        """Make a move given the current game.

        Preconditions:
            - not game.is_guesser_turn()
        """
        if not game.statuses:
            self._game_tree = generate_gametree(layer, None, None, game.current_board, 0, None)
        else:
            self._game_tree = generate_gametree(layer, self._game_tree.move, self._game_tree.prev_solution,
                                                game.current_board, len(game.guesses), self._game_tree)
        possible_subtrees = self._game_tree.get_subtrees()
        record_subs = [possible_subtrees[0]]
        for i in range(1, len(possible_subtrees)):
            if possible_subtrees[i].adversary_lose_probability < record_subs[0].adversary_lose_probability:
                record_subs = [possible_subtrees[i]]
            elif possible_subtrees[i].adversary_lose_probability == record_subs[0].adversary_lose_probability:
                record_subs.append(possible_subtrees[i])
        record_sub = random.choice(record_subs)
        solution_chosen = record_sub.prev_solution
        if game.get_status_for_answer(game.guesses[-1], solution_chosen):
            coord = game.guesses[-1][0]
            value = game.guesses[-1][1]
            new_board = copy_board(game.current_board)
            new_board[coord[0]][coord[1]] = value
            possible_cells = order_cells(new_board)
            coord = possible_cells[0][0]
            new_board[coord[0]][coord[1]] = solution_chosen[coord[0]][coord[1]]
            self._game_tree = GameTree(new_board, record_sub.parent, game.guesses[-1], solution_chosen)
        else:
            new_board = copy_board(game.current_board)
        return (solution_chosen, new_board)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'max-nested-blocks': 10
    })
