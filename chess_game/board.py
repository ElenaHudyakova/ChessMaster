import copy
from chess_game.game import *
from chess_game.piece_factory import create_piece, change_piece_type

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
        except :
            try:
                if key.__class__ == Point:
                    point = key
                else:
                    raise Exception
            except :
                raise Exception("Invalid index for board_position " + str(key))
        for piece in self._pieces:
            if piece.point == point:
                return piece
        return None

    def __len__(self):
        return len(self._pieces)

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
#            if move.algebraic_notation == "cxd8=Q+" and move.move_number == 31:
#                print piece
            if (piece.type == move.piece_type) and (piece.color == move.color):
                if (move.from_point.rank and move.from_point.rank != piece.point.rank) or (move.from_point.file and move.from_point.file != piece.point.file):
                    corresponds_to_from_point = False
                else:
                    corresponds_to_from_point = True

                if corresponds_to_from_point:
                    if move.is_capture:
                        if piece.motion_strategy.is_capture_possible(self, piece.point, move.to_point):
                            suitable_pieces.append(copy.copy(piece))
                    else:
                        if piece.motion_strategy.is_move_possible(self, piece.point, move.to_point):
                            suitable_pieces.append(copy.copy(piece))
        return suitable_pieces

    def _set_regular_move(self, previous_board_position, move):
        suitable_pieces = previous_board_position.find_suitable_pieces(move)

        if len(suitable_pieces) != 1:
            for piece in suitable_pieces:
                print piece
            raise Exception(str(len(suitable_pieces)) + " pieces were found suitable for move " + str(move.move_number) + " " + move.algebraic_notation)

        if move.is_capture:
            self._pieces.remove(self[move.to_point])
        if move.is_promotion:
            change_piece_type(self[suitable_pieces[0].point], move.promotion_piece_type)
        self[suitable_pieces[0].point].point = move.to_point

        """for piece in self._pieces:
            if move.algebraic_notation == "fxe5":
                print piece
            if move.is_capture and piece.point == move.to_point:
                self._pieces.remove(piece)
            if piece.point == suitable_pieces[0].point:
                if move.algebraic_notation == "fxe5":
                    print 1
                piece.point = move.to_point"""

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
            new_board_position._set_king_castling()
        else:
            if move.is_queen_castling:
                new_board_position._set_queen_castling()
            else:
                new_board_position._set_regular_move(self, move)

        if self.active_color == WHITE:
            new_board_position.active_color = BLACK
        else:
            new_board_position.active_color = WHITE
        return new_board_position
