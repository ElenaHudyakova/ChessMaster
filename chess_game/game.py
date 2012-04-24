BLACK = 1
WHITE = 0

ROOK = 0
KNIGHT = 1
BISHOP = 2
QUEEN = 3
KING = 4
PAWN = 5

class Game(object):
    def __init__(self):
        self.tags = dict()
        self.moves = list()