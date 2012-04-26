import copy
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

    def __str__(self):
        return "(" + str(self.file) + ", " + str(self.rank) + ")"

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

        board.active_color = WHITE

        return board

    def find_suitable_pieces(self, move):
        suitable_pieces = list()
        for piece in self._pieces:
            if (piece.type == move.piece_type) and (piece.color == move.color):
                if move.from_point:
                        if move.is_capture:
                            if piece.motion_strategy.is_capture_possible(self, piece.point, move.to_point):
                                suitable_pieces.append(copy.copy(piece))
                        else:
                            #print "!"
                            if piece.motion_strategy.is_move_possible(self, piece.point, move.to_point):
                                suitable_pieces.append(copy.copy(piece))
        return suitable_pieces

    def _set_regular_move(self, previous_board_position, move):
        pieces = previous_board_position.find_suitable_pieces(move)

        print str(len(pieces)) + " pieces were found suitable for move " + move.algebraic_notation

        #if len(pieces) != 1:
        #    raise Exception(str(len(pieces)) + " pieces were found suitable for move " + move.algebraic_notation)

        for piece in self._pieces:
            if move.is_capture and piece.point == move.to_point:
                self._pieces.remove(piece)
            if piece.point == pieces[0].point:
                piece.point = move.to_point

    def _set_king_castling(self):
        if self.active_color == WHITE:
            rank = 1
        else:
            rank = 8
        if self[("f", rank)] is None and self[("g", rank)] is None\
                and self[("e", rank)].type == KING and self[("h", rank)].type == ROOK:
            self[("e", rank)].point = Point("g",rank)
            self[("h", rank)].point = Point("f", rank)
        else:
            raise Exception("Invalid king caslting")


    def _set_queen_castling(self):
        if self.active_color == WHITE:
            rank = 1
        else:
            rank = 8
        if self[("b", rank)] is None and self[("c", rank)] is None and self[("d", rank)] is None\
           and self[("e", rank)].type == KING and self[("a", rank)].type == ROOK:
            self[("e", rank)].point = Point("c",rank)
            self[("a", rank)].point = Point("d", rank)
        else:
            raise Exception("Invalid queen caslting")


    def get_next_board_position(self, move):
        new_board_position = copy.deepcopy(self)

        if move.is_king_castling:
            print "king castling"
            new_board_position._set_king_castling()
        else:
            if move.is_queen_castling:
                print "queen castling"
                new_board_position._set_queen_castling()
            else:
                new_board_position._set_regular_move(self, move)

        if self.active_color == WHITE:
            new_board_position.active_color = BLACK
        else:
            new_board_position.active_color = WHITE
        return new_board_position
