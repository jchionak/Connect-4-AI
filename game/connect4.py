"""
A representation of the classic Connect 4 game.

A graph is used to represent the board, with its vertices being the individual game pieces.
"""
from __future__ import annotations
from typing import Optional

COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G']


class _Vertex:
    """
    A single game piece.

    Instance Attributes:
        - colour: the colour of the piece (red for the red player, yellow for yellow player, grey if placeholder)
        - location: the location of this vertex on the game board
        - up, down, left, right, upleft, upright, downleft, downright: the vertices adjacent to this vertex
    """
    colour: str
    location: tuple[str, int]
    up: Optional[_Vertex] = None
    down: Optional[_Vertex] = None
    left: Optional[_Vertex] = None
    right: Optional[_Vertex] = None
    upleft: Optional[_Vertex] = None
    upright: Optional[_Vertex] = None
    downleft: Optional[_Vertex] = None
    downright: Optional[_Vertex] = None

    def __init__(self, location: tuple[str, int]):
        self.colour = 'grey'
        self.location = location

    def change_colour(self, colour: str):
        """
        Changes the colour of this game piece.

        Preconditions:
            - colour in {'red', 'yellow', 'grey'}
        """
        self.colour = colour

    def __str__(self):
        connections = []
        if self.up is not None:
            connections.append(self.up.location)
        if self.upleft is not None:
            connections.append(self.upleft.location)
        if self.upright is not None:
            connections.append(self.upright.location)
        if self.down is not None:
            connections.append(self.down.location)
        if self.downleft is not None:
            connections.append(self.downleft.location)
        if self.downright is not None:
            connections.append(self.downright.location)
        if self.right is not None:
            connections.append(self.right.location)
        if self.left is not None:
            connections.append(self.left.location)
        return f'Location: {self.location} \n' \
               f'   colour: {self.colour} \n' \
               f'   connections: {str(connections)}'

    def num_colour_horizontal(self, colour: str, visited: set[_Vertex]) -> int:
        """
        Returns the number of vertices with the specified colour that are lined up horizontally.
        """
        if self.colour != colour:
            return 0
        else:
            visited.add(self)
            total_horizontal = 1
            if self.left not in visited and self.left is not None:
                total_horizontal += self.left.num_colour_horizontal(colour, visited)
            if self.right not in visited and self.right is not None:
                total_horizontal += self.right.num_colour_horizontal(colour, visited)
            return total_horizontal

    def num_colour_vertical(self, colour: str, visited: set[_Vertex]) -> int:
        """
        Returns the number of vertices with the specified colour that are lined up vertically.
        """
        if self.colour != colour:
            return 0
        else:
            visited.add(self)
            total_vertical = 1
            if self.up not in visited and self.up is not None:
                total_vertical += self.up.num_colour_vertical(colour, visited)
            if self.down not in visited and self.down is not None:
                total_vertical += self.down.num_colour_vertical(colour, visited)
            return total_vertical

    def num_colour_right_diagonal(self, colour: str, visited: set[_Vertex]) -> int:
        """
        Returns the number of bertices with the specified colour that are lined up diagonally in this orientation: \
        """
        if self.colour != colour:
            return 0
        else:
            visited.add(self)
            total_diagonal = 1
            if self.upleft not in visited and self.upleft is not None:
                total_diagonal += self.upleft.num_colour_right_diagonal(colour, visited)
            if self.downright not in visited and self.downright is not None:
                total_diagonal += self.downright.num_colour_right_diagonal(colour, visited)
            return total_diagonal

    def num_colour_left_diagonal(self, colour: str, visited: set[_Vertex]) -> int:
        """
        Returns the number of bertices with the specified colour that are lined up diagonally in this orientation: /
        """
        if self.colour != colour:
            return 0
        else:
            visited.add(self)
            total_diagonal = 1
            if self.upright not in visited and self.upright is not None:
                total_diagonal += self.upright.num_colour_left_diagonal(colour, visited)
            if self.downleft not in visited and self.downleft is not None:
                total_diagonal += self.downleft.num_colour_left_diagonal(colour, visited)
            return total_diagonal


class Board:
    """
    A game board for Connect 4.
    Has 6 rows and 7 columns for pieces.

    Instance Attributes:
        - vertices: the vertices that make up this graph
    """
    vertices: dict[tuple[str, int], _Vertex]

    def __init__(self):
        self.vertices = {}

        for letter in COLUMNS:
            for i in range(1, 7):
                location = (letter, i)
                self.vertices[location] = _Vertex(location)

        self.connect_board()

    def add_piece(self, colour: str, column: str) -> None:
        """
        Adds a piece to the board in the specified column.
        The piece will be added to the lowest available spot in the column.
        """
        for i in range(1, 7):
            if self.vertices[(column, i)].colour == 'grey':
                self.vertices[(column, i)].colour = colour
                return
        else:
            raise ValueError

    def remove_piece(self, column: str) -> None:
        """
        Removes the last placed piece from the specfied column.
        """
        for i in range(2, 7):
            if self.vertices[(column, i)].colour == 'grey':
                self.vertices[(column, i - 1)].colour = 'grey'
                return
            elif i == 6 and self.vertices[(column, i)] != 'grey':
                self.vertices[(column, i)].colour = 'grey'
                return

    def connect_board(self):
        """
        Connects all adjacent pieces in the board.
        """
        for location in self.vertices:
            if location[1] == 1:  # first piece in a column
                self.vertices[location].up = self.vertices[(location[0], location[1] + 1)]
                if ord(location[0]) > ord('A'):  # in any column other than the first one
                    self.vertices[location].left = self.vertices[(chr(ord(location[0]) - 1), location[1])]
                    self.vertices[location].upleft = self.vertices[(chr(ord(location[0]) - 1), location[1] + 1)]
                if ord(location[0]) < ord('G'):  # in any column other than the last one
                    self.vertices[location].right = self.vertices[(chr(ord(location[0]) + 1), location[1])]
                    self.vertices[location].upright = self.vertices[(chr(ord(location[0]) + 1), location[1] + 1)]
            elif location[1] == 6:  # last piece in a column
                self.vertices[location].down = self.vertices[(location[0], location[1] - 1)]
                if ord(location[0]) > ord('A'):
                    self.vertices[location].left = self.vertices[(chr(ord(location[0]) - 1), location[1])]
                    self.vertices[location].downleft = self.vertices[(chr(ord(location[0]) - 1), location[1] - 1)]
                if ord(location[0]) < ord('G'):
                    self.vertices[location].right = self.vertices[(chr(ord(location[0]) + 1), location[1])]
                    self.vertices[location].downright = self.vertices[(chr(ord(location[0]) + 1), location[1] - 1)]
            else:  # neither first nor last piece in a column
                self.vertices[location].up = self.vertices[(location[0], location[1] + 1)]
                self.vertices[location].down = self.vertices[(location[0], location[1] - 1)]
                if ord(location[0]) > ord('A'):
                    self.vertices[location].left = self.vertices[(chr(ord(location[0]) - 1), location[1])]
                    self.vertices[location].upleft = self.vertices[(chr(ord(location[0]) - 1), location[1] + 1)]
                if ord(location[0]) < ord('G'):
                    self.vertices[location].right = self.vertices[(chr(ord(location[0]) + 1), location[1])]
                    self.vertices[location].upright = self.vertices[(chr(ord(location[0]) + 1), location[1] + 1)]
                if ord(location[0]) > ord('A'):
                    self.vertices[location].left = self.vertices[(chr(ord(location[0]) - 1), location[1])]
                    self.vertices[location].downleft = self.vertices[(chr(ord(location[0]) - 1), location[1] - 1)]
                if ord(location[0]) < ord('G'):
                    self.vertices[location].right = self.vertices[(chr(ord(location[0]) + 1), location[1])]
                    self.vertices[location].downright = self.vertices[(chr(ord(location[0]) + 1), location[1] - 1)]

    def print_board(self):
        """
        Prints a text representation of the board. Purely for debugging purposes.
        """
        for vertex in self.vertices:
            print(self.vertices[vertex])

    def check_win(self, location: tuple[str, int]) -> bool:
        """
        Checks if the last played move has resulted in a win.
        """
        vertex = self.vertices[location]
        if vertex.num_colour_vertical(vertex.colour, set()) >= 4:
            return True
        elif vertex.num_colour_horizontal(vertex.colour, set()) >= 4:
            return True
        elif vertex.num_colour_right_diagonal(vertex.colour, set()) >= 4:
            return True
        else:
            return vertex.num_colour_left_diagonal(vertex.colour, set()) >= 4

    def full_board(self) -> bool:
        """
        Returns whether the board is completely filled up or not.
        """
        return all(self.vertices[vertex].colour != 'grey' for vertex in self.vertices)
