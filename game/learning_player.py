"""
Implements a player that 'learns' from past games to improve their performance.
"""
from __future__ import annotations
from manager import *
import random

GAME_START_MOVE = '*'


class MoveTree:
    """
    A tree implementation designed to keep track of Connect 4 game move sequences.

    Instance Attributes:
        - root: the move that was played on this turn
        - win_probability: ranges from -1.0 to 1.0, -1.0 for a yellow win, 0.0 for a draw, 1.0 for a red win, otherwise
        the average of subtree's win_probability
        - subtrees: the possible moves following this move
    """
    root: str
    win_probability: float = 0
    subtrees: dict[str, MoveTree]

    def __init__(self, root: str, win_probability: float = 0):
        self.root = root
        self.win_probability = win_probability
        self.subtrees = {}

    def is_empty(self) -> bool:
        """
        Returns whether this tree is empty.
        """
        return self.root is None

    def is_leaf(self) -> bool:
        """
        Returns whether this tree is a leaf (has no subtrees).
        """
        return self.subtrees == {}

    def calculate_win_probability(self):
        """
        Calculates and updates the win_probability of this tree.

        win_probability of a tree is defined as the average win_probabilities of its subtrees.
        """
        self.win_probability = sum(self.subtrees[subtree].win_probability for subtree in self.subtrees) / len(
            self.subtrees)

    def find_subtree_by_move(self, move: str) -> Optional[MoveTree]:
        """
        Return the subtree corresponding to the given move.

        Return None is no subtree corresponds to that move.
        """
        if move in self.subtrees:
            return self.subtrees[move]
        else:
            return None

    def insert_move_sequence(self, sequence: list[str], win_probability: float):
        """
        Inserts the given sequence of moves into the MoveTree.
        """
        self._insert_move_sequence_index(sequence, win_probability, 0)

    def _insert_move_sequence_index(self, sequence: list[str], win_probability: float, index: int):
        """
        Inserts the given sequence of moves into the MoveTree starting at the given index.
        """
        if index >= len(sequence):
            return
        else:
            move_to_insert = sequence[index]

        if move_to_insert not in self.subtrees and index == len(sequence) - 1:  # a leaf not already in the tree
            self.subtrees[move_to_insert] = MoveTree(move_to_insert, win_probability)
        elif move_to_insert in self.subtrees and index == len(sequence) - 1:  # a leaf that is already in the tree
            self.subtrees[move_to_insert].win_probability = win_probability
        elif move_to_insert not in self.subtrees:  # not a leaf and not already in the tree
            self.subtrees[move_to_insert] = MoveTree(move_to_insert)

        self.subtrees[move_to_insert]._insert_move_sequence_index(sequence, win_probability, index + 1)
        self.calculate_win_probability()


class LearningPlayer(Player):
    """
    A player that can learn from their previous games.

    Instance Attributes:
        - colour: the colour of the pieces this player uses.
        - past_games: a tree with previous game move sequences.
        - exploration_probability: the likelihood that the player will play a random move (0.0 for always random, 1.0
        for never random)
    """
    colour: str
    past_games: Optional[MoveTree]
    exploration_probability: float

    def __init__(self, colour: str, past_games: MoveTree, exploration_probability: float):
        Player.__init__(self, colour)
        self.past_games = past_games
        self.exploration_probability = exploration_probability

    def check_for_winning_moves(self, available_columns: list[str], game: GameManager) -> Optional[str]:
        """
        Checks all possible moves to see if there is a move that will immediately lead to a win for the player.

        Returns the column where the first discovered win is.
        """
        for column in available_columns:
            game.board.add_piece(self.colour, column)
            if game.board.check_win((column, game.moves_per_column[column] + 1)):
                game.board.remove_piece(column)
                return column
            else:
                game.board.remove_piece(column)

        return None

    def check_for_losing_moves(self, available_columns: list[str], game: GameManager) -> Optional[str]:
        """
        Checks all possible moves to see if there is a move that will immediately lead to a loss for the player.

        Returns the column where the first discovered loss is.
        """
        if self.colour == 'red':
            opponent_colour = 'yellow'
        else:
            opponent_colour = 'red'

        for column in available_columns:
            game.board.add_piece(opponent_colour, column)
            if game.board.check_win((column, game.moves_per_column[column] + 1)):
                game.board.remove_piece(column)
                return column
            else:
                game.board.remove_piece(column)

        return None

    def make_move(self, available_columns: list[str], game: GameManager) -> str:
        """
        Makes a move by either choosing the move that provides the highest possible win_probability, or chooses a random
        move to expand its knowledge of possible moves.
        """
        if len(game.move_sequence) != 0 and self.past_games is not None:
            last_move = game.move_sequence[-1]
            self.past_games = self.past_games.find_subtree_by_move(last_move)

        if len(game.move_sequence) >= 6:
            winning_move = self.check_for_winning_moves(available_columns, game)
            if winning_move is not None:
                return winning_move
            losing_move = self.check_for_losing_moves(available_columns, game)
            if losing_move is not None:
                return losing_move

        if self.past_games is not None and not self.past_games.is_leaf():
            explore = random.uniform(0.0, 1.0)
            if explore <= self.exploration_probability:
                max_win_prob_so_far = -1.0
                best_subtree = available_columns[0]
                for subtree in self.past_games.subtrees.values():
                    if max_win_prob_so_far < subtree.win_probability and subtree.root in available_columns:
                        max_win_prob_so_far = subtree.win_probability
                        best_subtree = subtree.root
                if max_win_prob_so_far > 0.0:  # only follow the tree if there is a move that is winning
                    return best_subtree
                else:
                    return random.choice(available_columns)
            else:
                next_move = random.choice(available_columns)
                if next_move not in self.past_games.subtrees:
                    self.past_games = None
                return next_move
        else:
            return random.choice(available_columns)

    def insert_games_from_csv(self, filename: str):
        """
        Inserts games from the given csv file into the past_games tree.
        """
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                move_sequence = row
                winning_colour = next(reader)
                if winning_colour[0] == self.colour:
                    self.past_games.insert_move_sequence(move_sequence, 1.0)
                else:
                    self.past_games.insert_move_sequence(move_sequence, -1.0)


def run_learning_algorithm(exploration_probabilities: list[float], past_games: Optional[MoveTree] = None) -> tuple:
    """
    Plays the specified number of Connect 4 games with the red player learning from each game.
    """
    if past_games is None:
        game_tree_so_far = MoveTree(GAME_START_MOVE)
    else:
        game_tree_so_far = past_games
    yellow_player = RandomPlayer()

    stats = {'red': 0, 'yellow': 0, 'draw': 0}
    results = []

    num_games = len(exploration_probabilities)

    for i in range(num_games):
        red_player = LearningPlayer('red', game_tree_so_far, exploration_probabilities[i])
        game = GameManager(red_player, yellow_player)
        game.run_game()
        winner = game.winner

        stats[winner] += 1
        results.append(winner)

        # print(f'Game {i} Winner: {winner}. Moves: {game.move_sequence}')

        move_sequence = game.move_sequence

        if winner == 'red':
            game_tree_so_far.insert_move_sequence(move_sequence, 1.0)
        elif winner == 'yellow':
            game_tree_so_far.insert_move_sequence(move_sequence, -1.0)
        else:
            game_tree_so_far.insert_move_sequence(move_sequence, 0.0)

    # for stat in stats:
    #     print(f'{stat}: {stats[stat]}')
    #
    # results_for_graph = [2 if result == 'red' else 1 if result == 'draw' else 2 for result in results]
    # plt.plot(results_for_graph, 'ro')
    # plt.ylabel('Outcome (2 = Red, 1 = Draw, 0 = Yellow)')
    # plt.xlabel('Game Number')
    # plt.show()

    return game_tree_so_far, stats


def learning_algorithm_example():
    """
    Runs the learning algorithm 4000 times.
    """
    probabilities = []
    probabilities.extend([0.0] * 20000)

    learn_algo = run_learning_algorithm(probabilities)
    explored_game_tree = learn_algo[0]
    stats = learn_algo[1]

    probabilities = []
    probabilities.extend([1.0] * 20000)

    new_learn_algo = run_learning_algorithm(probabilities, explored_game_tree)
    new_stats = new_learn_algo[1]

    print('\nOld Stats: \n')

    for stat in stats:
        print(f'{stat}: {stats[stat]}')

    print('\nWin Percentages\n')
    print(f"Old: {(stats['red'] / 20000) * 100}\n")
    print(f"New: {(new_stats['red'] / 20000) * 100}")
