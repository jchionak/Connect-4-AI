"""
Contains the GameManager class, which plays a game of Connect 4.
"""
from __future__ import annotations
from connect4 import *
import random
import csv


class Player:
    """
    A Connect 4 player.

    Instance Attributes:
        - colour: the colour of the pieces this player uses.
    """
    colour: str

    def __init__(self, colour: Optional[str] = None):
        self.colour = colour

    def make_move(self, available_columns: list[str], game: GameManager) -> str:
        """
        Chooses a column to drop a piece into and returns that column.
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """
    A Connect 4 player that makes their moves completely randomly.
    """

    def make_move(self, available_columns: list[str], game: GameManager) -> str:
        """
        Chooses a column to drop a piece into and returns that column.
        """
        return random.choice(available_columns)


class GameManager:
    """
    Manages a game of Connect 4.

    Instance Attributes:
        - red_player: the player who will play with the red pieces. NOTE: the red player always goes first.
        - yellow_player: the player who will play with the yellow pieces.
        - board: the board that this game is played on.
        - move_sequence: a list of all the moves played during the game.
        - winner: the colour of the player who won the game.
    """
    red_player: Player
    yellow_player: Player
    board: Board
    moves_per_column: dict[str, int]
    move_sequence: list[str]
    winner: Optional[str] = None

    def __init__(self, red_player: Player, yellow_player: Player):
        self.red_player = red_player
        self.yellow_player = yellow_player
        self.board = Board()
        self.moves_per_column = {}
        for column in COLUMNS:
            self.moves_per_column[column] = 0
        self.move_sequence = []

    def add_piece(self, colour: str, column: str):
        """
        Adds a piece to this game.
        """
        self.board.add_piece(colour, column)
        self.move_sequence.append(column)

    def run_game(self):
        """
        Runs a game between red_player and yellow_player.
        """
        available_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

        while not self.board.full_board():
            if len(self.move_sequence) % 2 == 0:
                moving_player = 'red'
                move = self.red_player.make_move(available_columns, self)
                self.board.add_piece('red', move)
            else:
                moving_player = 'yellow'
                move = self.yellow_player.make_move(available_columns, self)
                self.board.add_piece('yellow', move)
            self.move_sequence.append(move)
            # print(f'{moving_player.upper()} plays {move}')
            self.moves_per_column[move] += 1
            if self.moves_per_column[move] >= 6:
                available_columns.remove(move)
            if self.board.check_win((move, self.moves_per_column[move])):
                self.winner = moving_player
                # print(f'{moving_player.upper()} wins!')
                return

        self.winner = 'draw'


def run_games_random(num_games: int) -> dict[str, int]:
    """
    Runs the specified number of games between two RandomPlayers.
    """
    num_wins_by_colour = {'red': 0, 'yellow': 0, 'draw': 0}

    for _ in range(num_games):
        red_player = RandomPlayer()
        yellow_player = RandomPlayer()
        game = GameManager(red_player, yellow_player)
        game.run_game()
        if game.winner == 'red':
            num_wins_by_colour['red'] += 1
        elif game.winner == 'yellow':
            num_wins_by_colour['yellow'] += 1
        else:
            num_wins_by_colour['draw'] += 1

    return num_wins_by_colour


def run_games_random_for_data(num_games: int, filename: str) -> dict[str, int]:
    """
    Runs the specified number of games between two RandomPlayers, and saves the move sequence and winner of each game
    in a CSV file.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        num_wins_by_colour = {'red': 0, 'yellow': 0, 'draw': 0}

        for _ in range(num_games):
            red_player = RandomPlayer()
            yellow_player = RandomPlayer()
            game = GameManager(red_player, yellow_player)
            game.run_game()
            if game.winner == 'red':
                num_wins_by_colour['red'] += 1
            elif game.winner == 'yellow':
                num_wins_by_colour['yellow'] += 1
            else:
                num_wins_by_colour['draw'] += 1

            writer.writerow(game.move_sequence)
            if game.winner is not None:
                writer.writerow([game.winner])
            else:
                writer.writerow(['draw'])

        return num_wins_by_colour
