"""
Allows the user to play Connect 4 against the computer.
"""
from manager import *
from learning_player import MoveTree, LearningPlayer, run_learning_algorithm
import pygame
import sys


def get_user_mouse_position() -> tuple[int, int]:
    """
    Returns the position of the mouse when the screen is clicked by user.
    """
    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP])
    event = pygame.event.wait()

    if event.type == pygame.MOUSEBUTTONUP:
        return event.pos
    elif event.type == pygame.QUIT:
        print('Exiting Pygame window. Please restart the Python console!')
        pygame.display.quit()
        sys.exit(0)


class HumanPlayer(Player):
    """
    A human Connect 4 player. They make their moves by clicking on the pygame window.
    """
    def make_move(self, available_columns: list[str], game: GameManager) -> str:
        """
        Picks a column based on the user's mouse position.
        """
        mouse_pos = get_user_mouse_position()
        mouse_x = mouse_pos[0]

        if 0 <= mouse_x <= 150:  # ends 150
            return 'A'
        elif 175 < mouse_x <= 275:  # centre 225 radius 50
            return 'B'
        elif 300 < mouse_x <= 400:  # centre 350 radius 50
            return 'C'
        elif 425 < mouse_x <= 525:  # centre 475
            return 'D'
        elif 550 < mouse_x <= 650:  # centre 600
            return 'E'
        elif 675 < mouse_x <= 775:  # centre 725
            return 'F'
        else:
            return 'G'


def run_interactive_game():
    """
    Runs a single game where the player plays against the AI.
    """
    # first, train the AI for a while
    probabilities = []
    probabilities.extend([0.0] * 20000)
    game_tree = run_learning_algorithm(probabilities)
    game_tree = game_tree[0]

    probabilities = []
    probabilities.extend([0.5] * 30000)
    game_tree = run_learning_algorithm(probabilities, game_tree)
    game_tree = game_tree[0]

    probabilities = []
    probabilities.extend([1.0] * 50000)
    game_tree = run_learning_algorithm(probabilities, game_tree)
    game_tree = game_tree[0]

    red_player = LearningPlayer('red', game_tree, 1.0)
    yellow_player = HumanPlayer('yellow')

    pygame.display.init()
    screen = pygame.display.set_mode((950, 800))
    screen.fill((0, 0, 205))
    pygame.display.set_caption('Connect 4')
    for i in range(7):
        for j in range(6):
            pygame.draw.circle(screen, (255, 255, 255), (100 + i * 125, 75 + j * 125), 50)

    pygame.display.flip()

    available_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

    game = GameManager(red_player, yellow_player)

    while not game.board.full_board():
        if len(game.move_sequence) % 2 == 0:
            moving_player = 'red'
            move = red_player.make_move(available_columns, game)
            game.add_piece('red', move)
            pygame.draw.circle(screen, (220, 20, 60),
                               (100 + (ord(move) - 65) * 125, 75 + (5 - game.moves_per_column[move]) * 125), 50)
        else:
            moving_player = 'yellow'
            while True:
                move = yellow_player.make_move(available_columns, game)
                if move in available_columns:
                    break
            game.add_piece('yellow', move)
            pygame.draw.circle(screen, (255, 255, 51),
                               (100 + (ord(move) - 65) * 125, 75 + (5 - game.moves_per_column[move]) * 125), 50)
        pygame.display.flip()
        pygame.time.delay(240 * 2)
        game.moves_per_column[move] += 1
        if game.moves_per_column[move] >= 6:
            available_columns.remove(move)
        if game.board.check_win((move, game.moves_per_column[move])):
            winner = moving_player
            print(f'{moving_player.upper()} wins!')
            break

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.wait()

    pygame.display.quit()


if __name__ == '__main__':
    run_interactive_game()
