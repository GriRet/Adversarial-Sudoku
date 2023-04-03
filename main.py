"""
The main running block of the project
"""
from __future__ import annotations
import copy
import sudoku_players as player
from adversarial_sudoku import AdversarialSudoku, copy_board
import pygame
import sys
from typing import Optional

# initializing the constructor
pygame.init()

# screen resolution
size = (650, 720)

# opens up a window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ADVERSIAL SUDOKU")

# text colors
white = (255, 255, 255)
black = (0, 0, 0)
color_light = (170, 170, 170)
color_dark = (90, 90, 90)
hover_color = (250, 250, 0)

# stores the width and height of the screen
width = screen.get_width()
height = screen.get_height()

# Define the size of the cells and the board
CELL_SIZE = 50
BOARD_SIZE = CELL_SIZE * 9

# defining a font
smallfont = pygame.font.SysFont('Arial', 35)
bigfont = pygame.font.SysFont('TimesNewRoman', 60)

# rendering a text written in this font
play_text = smallfont.render("Play", True, (255, 255, 255))
simulation_text = smallfont.render("Simulation", True, (255, 255, 255))
quit_text = smallfont.render("Quit", True, (255, 255, 255))

# Set up the positions of the texts
play_pos = (width / 2 - 30, 2 * height / 3 - 78)
simulation_pos = (width / 2 - 75, 2 * height / 3 - 18)
quit_pos = (width / 2 - 30, 2 * height / 3 + 40)

# Get the rect of each text surface
play_rect = play_text.get_rect(topleft=play_pos)
simulation_rect = simulation_text.get_rect(topleft=simulation_pos)
quit_rect = quit_text.get_rect(topleft=quit_pos)

# set the background image
background_img = pygame.image.load("blackboard.jpg")

# grid for the sudoku game
grid = prev_grid = original_grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

x = 0  # current x coordinate of the guess
y = 0  # current y coordinate of the guess
val = 0  # current guess of the user

selected = None
game_over = False
sudoku_running = False
use_solve = False

# settings of adversial sudoku game
MAX_GUESSES = 81
BOARD_LENGTH = 16
game = AdversarialSudoku(MAX_GUESSES, BOARD_LENGTH)


def update_cord(pos) -> tuple:
    """
    update the coordinate of a position in the grid and return the position as a tuple
    """
    global x
    x = (pos[0] - 100 - pos[0] % 52) // 52
    global y
    y = (pos[1] - 100 - pos[1] % 52) // 52

    return (x, y)


def highlight_box(s: screen, position: tuple):
    """
    Highlight the cell selected
    """
    if 102 < position[0] < 100 + 466 and 102 < position[1] < 102 + 466:
        pygame.draw.rect(s, color_dark,
                         (position[0] - position[0] % 52 - 2, position[1] - position[1] % 52 - 2, 50, 50))


def draw_val(value: int):
    """
    draw the value on the selected box
    """
    text = smallfont.render(str(value), True, (0, 255, 0))
    text_pos = (x * 52 + 118, y * 52 + 108)
    text_rect = text.get_rect(topleft=text_pos)
    screen.blit(text, text_rect)


def check_valid(value: int, location: tuple) -> bool:
    """
    check if the value in the coordinate is valid
    """
    for i in range(9):
        if grid[location[0]][i] == value:
            return False
        if grid[i][location[1]] == value:
            return False

    for i in range(location[0] - location[0] % 3, location[0] - location[0] % 3 + 3):
        for j in range(location[1] - location[1] % 3, location[1] - location[1] % 3 + 3):
            if grid[i][j] == value:
                return False

    return True


def draw_board(screen: screen, selected: Optional[tuple]):
    """
    draw the Sudoku board on the pygame screen and highlight the selected cell
    """
    screen.blit(background_img, (0, 0))

    pygame.draw.rect(screen, white, (100, 100, 470, 470), 2)
    pygame.draw.rect(screen, (200, 200, 200), (100 + 156, 100, 156, 156))
    pygame.draw.rect(screen, (200, 200, 200), (100, 100 + 156, 156, 156))
    pygame.draw.rect(screen, (200, 200, 200), (100 + 2 * 156, 100 + 156, 156, 156))
    pygame.draw.rect(screen, (200, 200, 200), (100 + 156, 100 + 2 * 156, 156, 156))

    for i in range(1, 9):
        play_pos = (100 + 50 * i + 2 * i, 100)
        end_pos = (100 + 50 * i + 2 * i, 100 + 470 - 2)
        pygame.draw.line(screen, white, play_pos, end_pos, 2)
    for j in range(1, 9):
        play_pos = (100, 100 + 50 * j + 2 * j)
        end_pos = (100 + 470 - 2, 100 + 50 * j + 2 * j)
        pygame.draw.line(screen, white, play_pos, end_pos, 2)

    if selected is not None:
        highlight_box(screen, selected)

    # Update the message below the sudoku board
    if sudoku_running:
        if game.get_winner() is not None:
            result_text = smallfont.render("Winner: " + game.get_winner(), True, white)
            screen.blit(result_text, (200, 600))
            ins = smallfont.render('Press Q to quit', True, white)
            screen.blit(ins, (220, 650))
        else:
            instruction = smallfont.render('Press R to regenerate', True, white)
            screen.blit(instruction, (170, 600))
            count_text = smallfont.render("Steps remaining: " + str(MAX_GUESSES - len(game.guesses)), True, white)
            screen.blit(count_text, (180, 650))
    else:
        if game.get_winner() is not None:
            result_text = smallfont.render("Winner: " + game.get_winner(), True, white)
            screen.blit(result_text, (200, 600))
            ins = smallfont.render('Press Q to quit', True, white)
            screen.blit(ins, (220, 650))
        else:
            message = smallfont.render('Simulating...', True, white)
            screen.blit(message, (250, 600))
            count_text = smallfont.render("Steps remaining: " + str(MAX_GUESSES - len(game.guesses)), True, white)
            screen.blit(count_text, (180, 650))

    # Fill grid with numbers specified
    for i in range(9):
        for j in range(9):
            if original_grid[i][j] != 0:
                text1 = smallfont.render(str(original_grid[i][j]), True, (0, 255, 0))
                screen.blit(text1, (i * 52 + 118, j * 52 + 108))
            elif grid[i][j] != 0:
                text1 = smallfont.render(str(grid[i][j]), True, (255, 255, 0))
                screen.blit(text1, (i * 52 + 118, j * 52 + 108))

    pygame.display.update()


def run_game(guesser: player.Guesser, adversary: player.Adversary, max_guesses: int, board_length: int,
             difficulty: int = 50) -> AdversarialSudoku:
    """Run an Adversarial Sudoku game between the two given players.

    Use the words in word_set_file, and use max_guesses as the maximum number of guesses.

    Return the AdversarialWordle instance after the game is complete.

    Preconditions:
    - word_set_file is a non-empty with one word per line
    - all words in word_set_file have the same length
    - max_guesses >= 1

    # >>> guesser = player.GreedyTreeGuesser()
    # >>> adversary = player.GreedyTreeAdversary()
    # >>> run_game(guesser, adversary, 81, 9, 50)
    """
    game = AdversarialSudoku(max_guesses, board_length, difficulty)

    i = 1
    while game.get_winner() is None:
        guess = guesser.make_move(game)
        game.record_guesser_move(guess)
        status = adversary.make_move(game)
        game.record_adversary_move(status)

        print(f'round{i}')
        if game.statuses[-1][0][game.guesses[-1][0][0]][game.guesses[-1][0][1]] == \
                game.statuses[-1][1][game.guesses[-1][0][0]][game.guesses[-1][0][1]]:
            print('Fail to guess the correct number')
        else:
            print('Guess correctly')
        i = i + 1

    print(f'Game Winner: {game.get_winner()}')  # . Moves: {game.get_move_sequence()}
    return game


def run_games(num_games: int,
              guesser: player.Guesser, adversary: player.Adversary,
              max_guesses: int,
              board_length: int,
              difficulty: int = 50,
              print_game: bool = True) -> dict[str, int]:
    """Run num_games games of Adversary Sudoku between the two given players.

    Optional arguments:
    - print_game: print a record of each game (default: True)
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
    # guesser = player.GreedyTreeGuesser()
    # adversary = player.NormalAdversary()
    # run_games(10, guesser, adversary, 81, 9, 10, print_game=True)

    while True:
        # load the background image
        screen.blit(background_img, (0, 0))
        # stores the (x,y) coordinates
        mouse = pygame.mouse.get_pos()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()

            # checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the button the game is terminated
                if quit_rect.collidepoint(ev.pos):
                    sys.exit()
                elif play_rect.collidepoint(ev.pos):
                    # Create the Sudoku game screen
                    sudoku_screen = pygame.display.set_mode((width, height))

                    # Sudoku game setting
                    adversary = player.GreedyTreeAdversary()
                    # Sudoku game loop
                    sudoku_running = True
                    game = AdversarialSudoku(MAX_GUESSES, BOARD_LENGTH)
                    grid = prev_grid = original_grid = game.current_board
                    game_over = False

                    while sudoku_running:

                        if game.get_winner() is not None:
                            game_over = True
                            grid = game.statuses[-1][0]

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sudoku_running = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if 102 < pos[0] < 100 + 466 and 102 < pos[1] < 102 + 466:
                                    selected = pygame.mouse.get_pos()
                                    update_cord(selected)
                            elif event.type == pygame.KEYDOWN:
                                if not game_over:
                                    if event.key == pygame.K_1:
                                        val = 1
                                    if event.key == pygame.K_2:
                                        val = 2
                                    if event.key == pygame.K_3:
                                        val = 3
                                    if event.key == pygame.K_4:
                                        val = 4
                                    if event.key == pygame.K_5:
                                        val = 5
                                    if event.key == pygame.K_6:
                                        val = 6
                                    if event.key == pygame.K_7:
                                        val = 7
                                    if event.key == pygame.K_8:
                                        val = 8
                                    if event.key == pygame.K_9:
                                        val = 9
                                    if event.key == pygame.K_r:
                                        val = 0
                                        game = AdversarialSudoku(MAX_GUESSES, BOARD_LENGTH)
                                        grid = prev_grid = original_grid = game.current_board
                                else:
                                    if game_over:
                                        if event.key == pygame.K_q:
                                            sudoku_running = False

                        if val != 0 and check_valid(val, (int(x), int(y))) and game.is_guesser_turn():
                            grid[int(x)][int(y)] = val
                            game.record_guesser_move(((int(x), int(y)), val))

                        if not game.is_guesser_turn():
                            response = adversary.make_move(game)
                            game.record_adversary_move(response)
                            if response is not str:
                                grid = response[1]
                                prev_grid = response[1]
                            else:
                                grid = response[0]

                        draw_board(sudoku_screen, selected)
                        val = 0

                        # Update the display
                        pygame.display.flip()

                elif simulation_rect.collidepoint(ev.pos):
                    # Simulation game loop
                    simulation_running = True

                    # setting the Sudoku game
                    simulation_screen = pygame.display.set_mode((width, height))
                    game_over = False
                    guesser = player.GreedyTreeGuesser()
                    adversary = player.GreedyTreeAdversary()
                    game = AdversarialSudoku(MAX_GUESSES, BOARD_LENGTH)
                    grid = prev_grid = original_grid = game.current_board

                    while simulation_running:

                        draw_board(simulation_screen, selected)

                        if game.get_winner() is not None:
                            game_over = True
                            grid = game.statuses[-1][0]

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                simulation_running = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                    simulation_running = False

                        if not game_over:
                            if game.is_guesser_turn():
                                guess = guesser.make_move(game)
                                game.record_guesser_move(guess)
                                grid[guess[0][0]][guess[0][1]] = guess[1]
                            else:
                                response = adversary.make_move(game)
                                grid = prev_grid = response[1]
                                game.record_adversary_move(response)
                                game.current_board = copy_board(game.statuses[-1][1])

                        pygame.time.delay(50)
                        pygame.display.flip()

        # Set the color of the play text based on mouse hover
        if play_rect.collidepoint(mouse):
            play_color = hover_color
        else:
            play_color = white

        # Set the color of the simulation text based on mouse hover
        if simulation_rect.collidepoint(mouse):
            simulation_color = hover_color
        else:
            simulation_color = white

        # Set the color of the quit text based on mouse hover
        if quit_rect.collidepoint(mouse):
            quit_color = hover_color
        else:
            quit_color = white

        # Render the texts with their colors
        play_text_rendered = smallfont.render("Play", True, play_color)
        simulation_text_rendered = smallfont.render("Simulation", True, simulation_color)
        quit_text_rendered = smallfont.render("Quit", True, quit_color)

        # Draw the texts on the screen
        screen.blit(play_text_rendered, play_rect)
        screen.blit(simulation_text_rendered, simulation_rect)
        screen.blit(quit_text_rendered, quit_rect)

        screen.blit(bigfont.render('Adversial Sudoku', True, white), (120, 240))

        # Update the display
        pygame.display.flip()

        # updates the frames of the game
        pygame.display.update()
