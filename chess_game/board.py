import copy
from chess_exceptions.chess_exceptions import InvalidMoveException
from chess_game.game import *
from chess_game.point import Point
from chess_game.piece_factory import create_piece, change_piece_type

class BoardState(object):
    def __init__(self):
        self.active_color = None
        self.en_passant_point = None
        self.pieces = list()

    def add_piece(self, piece):
        self.pieces.append(piece)

    def serialize(self):
        blobs = [0, 0, 0, 0];
        for file in range(1,9):
            for rank in range(1,9):
                point = Point(file, rank)
                blobs[(file-1)/2] *= 16
                if not (self[point] is None):
                    blobs[(file-1)/2]  += self[point].type + self[point].color*8;
                else:
                    blobs[(file-1)/2]  += 14;
        return blobs


    def __getitem__(self, key):
        """Get piece in the appropriate point of the board"""
        try:
            point = Point(key[0], key[1])
        except :
            if key.__class__ == Point:
                point = key
            else:
                raise Exception("Invalid index for board_position " + str(key))
        for piece in self.pieces:
            if piece.point == point:
                return piece
        return None

    def __len__(self):
        return len(self.pieces)

    @staticmethod
    def get_initial_board_position():
        board = BoardState()
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
        for piece in self.pieces:
            if (piece.type == move.piece_type) and (piece.color == move.color):
                corresponds_to_from_point = not ((move.from_point.rank and move.from_point.rank != piece.point.rank) or
                                                 (move.from_point.file and move.from_point.file != piece.point.file))

                if corresponds_to_from_point:
                    if move.is_capture:
                        if piece.can_capture(self, move.to_point):
                            suitable_pieces.append(copy.copy(piece))
                    else:
                        if piece.can_move(self, move.to_point):
                            suitable_pieces.append(copy.copy(piece))
        return suitable_pieces

    def _set_regular_move(self, move):
        suitable_pieces = self.find_suitable_pieces(move)

        if len(suitable_pieces) != 1:
            raise InvalidMoveException(str(len(suitable_pieces)) + " pieces were found suitable for move " + str(move.move_number) + " " + move.algebraic_notation)

#        if move.is_capture:
#            self.pieces.remove(self[move.to_point])

#        self[suitable_pieces[0].point].point = move.to_point

        if move.is_capture:
            suitable_pieces[0].capture(self, move.to_point)
        else:
            suitable_pieces[0].move(self, move.to_point)
        if move.is_promotion:
            for i in range(len(self.pieces)):
                if self.pieces[i].point == move.to_point:
                    self.pieces[i] = change_piece_type(self[move.to_point], move.promotion_piece_type)


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
            raise InvalidMoveException("Invalid king caslting")


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
            raise InvalidMoveException("Invalid queen caslting")


    def get_next_board_position(self, move):
        new_board_position = copy.deepcopy(self)

        try:
            if move.is_king_castling:
                new_board_position._set_king_castling()
            else:
                if move.is_queen_castling:
                    new_board_position._set_queen_castling()
                else:
                    new_board_position._set_regular_move(move)
        except Exception as error:
            print error.message
            raise Exception("Can not simulate move " + move.algebraic_notation)

        if self.active_color == WHITE:
            new_board_position.active_color = BLACK
        else:
            new_board_position.active_color = WHITE
        return new_board_position
