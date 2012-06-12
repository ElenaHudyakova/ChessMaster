import copy
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer
from common import Color, Square, PieceType
from game_exceptions import InvalidGameException
from pieces import PieceCreator
from game_exceptions import InvalidBoardSquare, ImpossibleMoveException
from storage.storage import session, Base

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String, default = '')
    date = Column(String, default = '')
    site = Column(String, default = '')
    result = Column(String, default = '')
    white = Column(String, default = '')
    black = Column(String, default = '')
    round = Column(String, default = '')

    def __init__(self):
        self.moves = list()
        self.board_states = list()

    def simulate(self):
        initial_setup = BoardState()
        initial_setup.make_initial_setup()
        self.board_states.append(initial_setup)
        for i in range(len(self.moves)):
            try:
                self.board_states.append(self.board_states[i].next(self.moves[i]))
            except :
                raise InvalidGameException('Error in the simulation on the %s halfmove' % str(i+1))

    def __cmp__(self, other):
        if self.event != other.event:
            return 1
        if self.site != other.site:
            return 1
        if self.date != other.date:
            return 1
        if self.round != other.round:
            return 1
        if self.white != other.white:
            return 1
        if self.black != other.black:
            return 1
        if self.result != other.result:
            return 1
        if self.moves != other.moves:
            return 1
        return 0


class BoardState(object):
    def __init__(self):
        self.active_color = Color.WHITE
        self.en_passant_target_square = None
        self.is_en_passant_for_next = None
        self.pieces = list()
        self.fullmove_number = 0

    def add_piece(self, piece):
        self.pieces.append(piece)

    def serialize(self):
        blobs = [0, 0, 0, 0]
        for rank in range(1,9):
            for file in range(1,9):
                square = Square(file, rank)
                blobs[(rank-1)/2] *= 16
                if not (self[square] is None):
                    blobs[(rank-1)/2] += self[square].type + self[square].color * 8
                else:
                    blobs[(rank-1)/2] += 14
        return blobs

    def __getitem__(self, key):
        """Get piece in the appropriate square of the board"""
        try:
            square = Square(key[0], key[1])
        except :
            if key.__class__ == Square:
                square = key
            else:
                raise InvalidBoardSquare("Invalid index for square in board_state " + str(key))
        for piece in self.pieces:
            if piece.square == square:
                return piece
        return None

    def __len__(self):
        return len(self.pieces)


    def can_kingside_castling(self):
        if self.active_color == Color.WHITE:
            rank = 1
        else:
            rank = 8

        if self[("f", rank)] is None and self[("g", rank)] is None\
           and self[("e", rank)] and self[("e", rank)].type == PieceType.KING \
           and self[("h", rank)] and self[("h", rank)].type == PieceType.ROOK:
                return not self.square_is_under_attack(Square('e', rank)) and\
                       not self.square_is_under_attack(Square('f', rank)) and\
                       not self.square_is_under_attack(Square('g', rank))
        else:
                return False


    def can_queenside_castling(self):
        if self.active_color == Color.WHITE:
            rank = 1
        else:
            rank = 8
        if self[("b", rank)] is None and self[("c", rank)] is None and self[("d", rank)] is None\
           and self[("e", rank)] and self[("e", rank)].type == PieceType.KING \
           and self[("a", rank)] and self[("a", rank)].type == PieceType.ROOK:
            return not self.square_is_under_attack(Square('c', rank)) and\
                   not self.square_is_under_attack(Square('d', rank)) and\
                   not self.square_is_under_attack(Square('e', rank))
        else:
            return False

    def square_is_under_attack(self, square):
        for piece in self.pieces:
            if piece.color != self.active_color and piece.can_attack(square, self):
                return True
        return False


    def make_initial_setup(self):
        for i in range(1,9):
            self.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square(i, 2), Color.WHITE))
            self.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square(i, 7), Color.BLACK))

        self.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('a', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.KNIGHT, Square('b', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.BISHOP, Square('c', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.QUEEN, Square('d', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.KING, Square('e', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.BISHOP, Square('f', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.KNIGHT, Square('g', 1), Color.WHITE))
        self.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('h', 1), Color.WHITE))

        self.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('a', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.KNIGHT, Square('b', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.BISHOP, Square('c', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.QUEEN, Square('d', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.KING, Square('e', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.BISHOP, Square('f', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.KNIGHT, Square('g', 8), Color.BLACK))
        self.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('h', 8), Color.BLACK))

        self.active_color = Color.BLACK

    def _set_kingside_castling(self):
        if self.can_kingside_castling():
            if self.active_color == Color.WHITE:
                rank = 1
            else:
                rank = 8

            self[("e", rank)].square = Square("g",rank)
            self[("h", rank)].square = Square("f", rank)


    def _set_queenside_castling(self):
        if self.can_queenside_castling():
            if self.active_color == Color.WHITE:
                rank = 1
            else:
                rank = 8

            self[("e", rank)].square = Square("c",rank)
            self[("a", rank)].square = Square("d", rank)

    def _set_regular_move(self, move):
        suitable_pieces = self._find_suitable_pieces(move)

        if len(suitable_pieces) != 1:
            raise ImpossibleMoveException(str(len(suitable_pieces)) + " pieces were found suitable for move " + str(move.fullmove_number) + " " + move.notation)
        else:
            moving_piece = suitable_pieces[0]

        if move.is_capture:
            moving_piece.capture(self, move.to_square)
        else:
            moving_piece.move(self, move.to_square)

        if move.is_promotion:
            for i in range(len(self.pieces)):
                if self.pieces[i].square == move.to_square:
                    self.pieces[i] = PieceCreator().change_piece_type(self[move.to_square], move.promotion_piece_type)

    def _find_suitable_pieces(self, move):
        suitable_pieces = list()
        for piece in self.pieces:
            if (piece.type == move.piece_type) and (piece.color == move.color):
                corresponds_to_from_square = not ((move.from_square.rank and move.from_square.rank != piece.square.rank) or
                                                 (move.from_square.file and move.from_square.file != piece.square.file))

                if corresponds_to_from_square:
                    if move.is_capture:
                        if piece.can_capture(move.to_square, self):
                            suitable_pieces.append(copy.copy(piece))
                    else:
                        if piece.can_move(move.to_square, self):
                            suitable_pieces.append(copy.copy(piece))
        return suitable_pieces

    def next(self, move):
        new_board = copy.deepcopy(self)

        if self.active_color == Color.WHITE:
            new_board.active_color = Color.BLACK
        else:
            new_board.fullmove_number += 1
            new_board.active_color = Color.WHITE

        if not self.is_en_passant_for_next is None:
            if self.is_en_passant_for_next == True:
                new_board.is_en_passant_for_next = False
            else:
                new_board.en_passant_target_square = None

        if move.is_king_castling:
            if new_board.can_kingside_castling():
                new_board._set_kingside_castling()
            else:
                raise ImpossibleMoveException(move.notation)

        if move.is_queen_castling:
            if new_board.can_queenside_castling():
                new_board._set_queenside_castling()
            else:
                raise ImpossibleMoveException(move.notation)

        if not move.is_king_castling and not move.is_queen_castling:
                new_board._set_regular_move(move)

        return new_board


