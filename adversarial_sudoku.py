"""
The file for adversarial sudoku
"""

from __future__ import annotations


from typing import Optional

from math import sqrt
# from python_ta.contracts import check_contracts

import sudoku_setup as setup


# @check_contracts
class AdversarialSudoku:
    """
    A class representing the state of a game of Adversarial Sudoku.
    """
    max_guesses: int
    guesses: list[tuple[tuple[int, int], int]]  # coordinates
    statuses: list[tuple[list[list[int]], list[list[int]]]]  # chosen solution and current boards
    current_board: list[list[int]]

    def __init__(self, max_guesses: int, board_length: int, difficulty: int = 50) -> None:
        """Initialize a new Adversarial Wordle game with the given word_set and max_guesses.

        Preconditions:
        - len(word_set) > 0
        - all words in word_set have the same length
        - max_guesses >= 1
        """
        self.max_guesses = max_guesses
        self.guesses = []
        self.statuses = []
        self.current_board = setup.generate_puzzle(difficulty, board_length)

    def is_guesser_turn(self) -> bool:
        """Return whether it is the Guesser player's turn.
        """
        return len(self.guesses) == len(self.statuses)

    def record_guesser_move(self, guess: tuple[tuple[int, int], int]) -> None:
        """Record the given guess made by the Guesser player."""
        self.guesses.append(guess)

    def record_adversary_move(self, status: tuple[list[list[int]], list[list[int]]]) -> None:
        """Record the given status returned by the Adversary player."""
        self.statuses.append(status)

    def copy_and_record_guesser_move(self, guess: tuple[tuple[int, int], int]) -> AdversarialSudoku:
        """Return a copy of this game state with the given guess recorded.

        Preconditions:
        - self.is_guesser_turn()
        - len(guess) == self.word_size
        - guess in self._possible_answers
        """
        new_game = self._copy()
        new_game.record_guesser_move(guess)
        return new_game

    def _copy(self) -> AdversarialSudoku:
        """Return a copy of this game state."""
        new_game = AdversarialSudoku(self.max_guesses, int(sqrt(len(self.current_board))))
        new_game.guesses.extend(self.guesses)
        new_game.statuses.extend(self.statuses)
        new_game.current_board = copy_board(self.current_board)
        return new_game

    def get_status_for_answer(self, guess: tuple[tuple[int, int], int],
                              solution: tuple[list[list[int]], list[list[int]]]) -> bool:
        """Return the status for the most recent guess with respect to the given answer.

        Preconditions:
        - not self.is_guesser_turn()
        """
        if solution[guess[0][0]][guess[0][1]] == guess[1]:
            return True
        else:
            return False

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game ('Guesser' or 'Adversary').

        Return None if the game is not over.
        """
        n = len(self.current_board)
        if len(self.guesses) != len(self.statuses):
            # It is the Adversary's turn; no one has won yet
            return None
        elif len(self.statuses) == 0:
            # No moves have been made; no one has won yet
            return None
        elif all(self.current_board[i][j] != 0 for j in range(n) for i in range(n)):
            return 'Guesser'
        elif self.statuses[-1][0] == self.statuses[-1][1]:
            # The Adversary returned an "all correct" guess; Guesser has won
            return 'Guesser'
        elif len(self.statuses) == self.max_guesses:
            # The Guesser has no more guesses; Adversary has won
            return 'Adversary'
        else:
            # It is the Guesser's turn; no one has won yet
            return None

    def get_move_sequence(self) -> list[tuple[tuple[int, int], int] | tuple[list[list[int]], list[list[int]]]]:
        """Return the move sequence made in this game.

        The returned list alternates between guesses (str) and statuses (tuple[str, ...]):

            [self.guesses[0], self.statuses[0], self.guesses[1], self.statuses[1], ...]
        """
        moves_so_far = []
        for i in range(0, len(self.guesses)):
            moves_so_far.append(self.guesses[i])
            if i < len(self.statuses):  # self.statuses may be 1 shorter than self.guesses
                moves_so_far.append(self.statuses[i])

        return moves_so_far


def copy_board(board: list[list[int]]) -> list[list[int]]:
    """
    As list.copy will make the two nested list allianced, then we use this copy function instead
    """
    new_board = []
    for row in board:
        new_board.append(row.copy())
    return new_board


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
