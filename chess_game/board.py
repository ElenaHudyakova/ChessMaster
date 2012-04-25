from chess_game.game import *
from chess_game.piece_factory import create_piece

class Point(object):
    def __init__(self, file = None, rank = None):
        self.file = file
        self.rank = rank


    def __setattr__(self, key, value):
        if (type(value).__name__ == "str") and (key == "file"):
            self.__dict__[key] = {
                'a': lambda: 1,
                'b': lambda: 2,
                'c': lambda: 3,
                'd': lambda: 4,
                'e': lambda: 5,
                'f': lambda: 6,
                'g': lambda: 7,
                'h': lambda: 8,
                '': lambda : None
                }[value]()
        else:
            self.__dict__[key] = value

    def __cmp__(self, other):
        if (self.file == other.file) and (self.rank == other.rank):
            return 0
        else:
            return 1

class BoardPosition(object):
    def __init__(self):
        self.active_color = None
        self.en_passant_point = None
        self._pieces = list()

    def add_piece(self, piece):
        self._pieces.append(piece)


    def __getitem__(self, key):
        try:
            point = Point(key[0], key[1])
            for piece in self._pieces:
                if piece.point == point:
                    return piece
            return None
        except :
            raise Exception("Invalid index for board_position " + str(key))

    @staticmethod
    def get_initial_board_position():
        board = BoardPosition()
        for i in range(1,9):
            board.add_piece(create_piece(PAWN, Point(i, 2), WHITE))
            board.add_piece(create_piece(PAWN, Point(i, 7), BLACK))

        board.add_piece(create_piece(ROOK, Point("a", 1), WHITE))
        board.add_piece(create_piece(KNIGHT, Point("b", 1), WHITE))
        board.add_piece(create_piece(BISHOP, Point("c", 1), WHITE))
        board.add_piece(create_piece(QUEEN, Point("d", 1), WHITE))
        board.add_piece(create_piece(KING, Point("e", 1), WHITE))
        board.add_piece(create_piece(BISHOP, Point("f", 1), WHITE))
        board.add_piece(create_piece(KNIGHT, Point("g", 1), WHITE))
        board.add_piece(create_piece(ROOK, Point("h", 1), WHITE))

        board.add_piece(create_piece(ROOK, Point("a", 8), BLACK))
        board.add_piece(create_piece(KNIGHT, Point("b", 8), BLACK))
        board.add_piece(create_piece(BISHOP, Point("c", 8), BLACK))
        board.add_piece(create_piece(QUEEN, Point("d", 8), BLACK))
        board.add_piece(create_piece(KING, Point("e", 8), BLACK))
        board.add_piece(create_piece(BISHOP, Point("f", 8), BLACK))
        board.add_piece(create_piece(KNIGHT, Point("g", 8), BLACK))
        board.add_piece(create_piece(ROOK, Point("h", 8), BLACK))

        return board

    def find_suitable_pieces(self, move):
        for piece in self._pieces:
            if (piece.type == move.piece_type) and (piece.color == move.color):
                if move.is_capture:
                    pass
                else:
                    pass


    def get_next_board_position(self, move):
        new_board_position = BoardPosition()
        pieces = self.find_suitable_pieces(move)
        if len(pieces) != 1:
            raise Exception(len(pieces) + " pieces were found suitable for move " + move.algebraic_notation)
        return new_board_position