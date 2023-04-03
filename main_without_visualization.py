"""
The main running block of the project
"""
from __future__ import annotations

import copy
# from python_ta.contracts import check_contracts

import sudoku_players as player
from adversarial_sudoku import AdversarialSudoku, copy_board


def run_game(guesser: player.Guesser, adversary: player.Adversary, max_guesses: int, board_length: int,
             difficulty: int = 50) -> AdversarialSudoku:
    """Run an Adversarial Sudoku game between the two given players.

    Use the words in word_set_file, and use max_guesses as the maximum number of guesses.

    Return the AdversarialWordle instance after the game is complete.

    Preconditions:
    - word_set_file is a non-empty with one word per line
    - all words in word_set_file have the same length
    - max_guesses >= 1

    >>> guesser = player.GreedyTreeGuesser()
    >>> adversary = player.GreedyTreeAdversary()
    >>> run_game(guesser, adversary, 81, 9, 60)
    """
    game = AdversarialSudoku(max_guesses, board_length, difficulty)

    i = 1
    while game.get_winner() is None:
        guess = guesser.make_move(game)
        game.record_guesser_move(guess)
        status = adversary.make_move(game)
        game.record_adversary_move(status)
        print(f'round{i}')
        if game.current_board == game.statuses[-1][1]:
            print('Fail to guess the correct number')
        else:
            print('Guess Correctly')
        game.current_board = copy_board(game.statuses[-1][1])
        i += 1

    print(f'Game Winner: {game.get_winner()}')  # . Moves: {game.get_move_sequence()}
    return game


def run_games(num_games: int,
              guesser: player.Guesser, adversary: player.Adversary,
              max_guesses: int,
              board_length: int,
              difficulty: int = 50,
              print_game: bool = True) -> dict[str, int]:
    """Run num_games games of Adversary Wordle between the two given players.

    Use the given word_set_file and max_guesses (these parameters are the same as
    in run_game).

    Optional arguments:
    - print_game: print a record of each game (default: True)
    - show_stats: use Plotly to display statistics for the game runs (default: False)

    Preconditions:
        - num_games >= 1
        - same preconditions for word_set_file and max_guesses as run_game
    """
    stats = {'Guesser': 0, 'Adversary': 0}
    results = []
    for i in range(0, num_games):
        guesser_copy = copy.copy(guesser)
        adversary_copy = copy.copy(adversary)

        game = run_game(guesser_copy, adversary_copy, max_guesses, board_length, difficulty)
        winner = game.get_winner()
        stats[winner] += 1
        results.append(winner)

        if print_game:
            print(f'Game {i} winner: {winner}')

    print(stats)
    return stats


if __name__ == '__main__':
    guesser = player.GreedyTreeGuesser()
    adversary = player.GreedyTreeAdversary()
    # run_games(10, guesser, adversary, 81, 9, 70)
    run_game(guesser, adversary, 81, 9, 56)
