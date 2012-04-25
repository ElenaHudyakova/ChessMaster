BLACK = 1
WHITE = 0

ROOK = 0
KNIGHT = 1
BISHOP = 2
QUEEN = 3
KING = 4
PAWN = 5

from chess_game.board import BoardPosition

class Game(object):
    def __init__(self):
        self.tags = dict()
        self.moves = list()
        self.board_positions = list()

    def simulate(self):
        self.board_positions.append(BoardPosition.get_initial_board_position())
        for i in range(len(self.moves)):
            self.board_positions.append(self.board_positions[i].get_next_board_position(self.moves[i]))