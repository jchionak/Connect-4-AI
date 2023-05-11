"""
Provides a pygame visualization of a Connect 4 game.
"""
import pygame
from manager import *


def simulate_game_visual():
    """
    Runs a game between two random players with pygame visuals.
    """
    pygame.display.init()
    screen = pygame.display.set_mode((950, 800))
    screen.fill((0, 0, 205))
    pygame.display.set_caption('Connect 4')
    for i in range(7):
        for j in range(6):
            pygame.draw.circle(screen, (255, 255, 255), (100 + i * 125, 75 + j * 125), 50)

    pygame.display.flip()

    red_player = RandomPlayer()
    yellow_player = RandomPlayer()
    move_sequence = []

    available_columns = COLUMNS.copy()
    moves_per_column = {}
    board = Board()
    game = GameManager(red_player, yellow_player)
    for column in COLUMNS:
        moves_per_column[column] = 0

    while not board.full_board():
        if len(move_sequence) % 2 == 0:
            moving_player = 'red'
            move = red_player.make_move(available_columns, game)
            board.add_piece('red', move)
            pygame.draw.circle(screen, (220, 20, 60),
                               (100 + (ord(move) - 65) * 125, 75 + (5 - moves_per_column[move]) * 125), 50)
        else:
            moving_player = 'yellow'
            move = yellow_player.make_move(available_columns, game)
            board.add_piece('yellow', move)
            pygame.draw.circle(screen, (255, 255, 51),
                               (100 + (ord(move) - 65) * 125, 75 + (5 - moves_per_column[move]) * 125), 50)
        pygame.display.flip()
        pygame.time.delay(240 * 2)
        move_sequence.append(move)
        # print(f'{moving_player.upper()} plays {move}')
        moves_per_column[move] += 1
        if moves_per_column[move] >= 6:
            available_columns.remove(move)
        if board.check_win((move, moves_per_column[move])):
            winner = moving_player
            print(f'{moving_player.upper()} wins!')
            break

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(pygame.QUIT)
    pygame.event.wait()

    pygame.display.quit()


simulate_game_visual()
