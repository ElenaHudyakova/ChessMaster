import copy
import math
from common import PieceType, Color, Square
from game_exceptions import ImpossibleMoveException

class Piece(object):
    def __init__(self, motion_strategy, type, square, color):
        self._motion_strategy = motion_strategy
        self.type = type
        self.square = square
        self.color = color

    def __str__(self):
        return str(self.type) + " " + str(self.square) + " " + str(self.color)

    def can_move(self, to_square, board_state = None):
        return self._motion_strategy.is_move_possible(self, to_square, board_state)

    def can_capture(self, to_square,  board_state = None):
        return self._motion_strategy.is_capture_possible(self, to_square, board_state)

    def can_attack(self, to_square,  board_state):
        return self._motion_strategy.is_attack_possible(self, to_square, board_state)

    def move(self, board_state, to_square):
        self._motion_strategy.make_move(board_state, self, to_square)

    def capture(self, board_state, to_square):
        self._motion_strategy.make_capture(board_state, self, to_square)



class PieceCreator(object):
    def _get_motion_strategy(self, type):
        motion_strategy = PawnMotionStrategy()
        if type == PieceType.KING:
            motion_strategy = KingMotionStrategy()
        if type == PieceType.KNIGHT:
            motion_strategy = KnightMotionStrategy()
        if type == PieceType.ROOK:
            motion_strategy = RookMotionStrategy()
        if type == PieceType.BISHOP:
            motion_strategy = BishopMotionStrategy()
        if type == PieceType.QUEEN:
            motion_strategy = QueenMotionStrategy()
        return  motion_strategy

    def create_piece(self, type, square, color):
        return Piece(self._get_motion_strategy(type), type, square, color)

    def change_piece_type(self, piece, type):
        return Piece(self._get_motion_strategy(type), type, piece.square, piece.color)






class MotionStrategy(object):
    def _can_move(self, piece, to_square, board_state = None):
        raise NotImplementedError()

    def is_move_possible(self, piece, to_square, board_state = None):
        if not board_state is None:
            return self._can_move(piece, to_square, board_state) and (board_state[(to_square.file, to_square.rank)] is None)
        else:
            return self._can_move(piece, to_square)

    def is_capture_possible(self, piece, to_square, board_state = None):
        if not board_state is None:
            return self._can_move(piece, to_square, board_state) and not (board_state[(to_square.file, to_square.rank)] is None)\
                and board_state[(to_square.file, to_square.rank)].color != piece.color
        else:
            return self._can_move(piece, to_square)

    def is_attack_possible(self, piece, to_square, board_state):
        return self._can_move(piece, to_square, board_state)

    def make_move(self, board_state, piece, to_square):
        board_state[piece.square].square = to_square

    def make_capture(self, board_state, piece, to_square):
        board_state.pieces.remove(board_state[to_square])
        self.make_move(board_state, piece, to_square)



class KingMotionStrategy(MotionStrategy):
    def _can_move(self, piece, to_square, board_state = None):
        if (math.fabs(piece.square.file-to_square.file) <= 1)\
        and (math.fabs(piece.square.rank-to_square.rank) <= 1):
            return True
        else:
            return False


class PawnMotionStrategy(MotionStrategy):

    def _get_direction(self, color):
        if color == Color.WHITE:
            return 1
        else:
            return -1

    def _is_first_move(self, color, from_square):
        if (from_square.rank == 2 and color == Color.WHITE) or (from_square.rank == 7 and color == Color.BLACK):
            return True
        else:
            return False

    def _can_move(self, piece, to_square, board_state = None):
        direction = self._get_direction(piece.color)
        if to_square.file == piece.square.file:
            if to_square.rank == piece.square.rank + direction:
                return True
            else:
                result = self._is_first_move(board_state.active_color, piece.square) and to_square.rank == piece.square.rank + direction*2
                if not board_state is None:
                    result = result and (board_state[(to_square.file, to_square.rank-direction)] is None)
                return result
        else:
            return False

    def _can_capture(self, piece, to_square, board_state = None):
        direction = self._get_direction(piece.color)
        if math.fabs(piece.square.file-to_square.file) == 1 and piece.square.rank + direction == to_square.rank:
            return True
        else:
            return False

    def _can_en_passant(self, piece, to_square, board_state):
        if not board_state.en_passant_target_square is None:
            return to_square == board_state.en_passant_target_square
        else:
            return False

    def is_move_possible(self, piece, to_square, board_state = None):
        if not board_state is None:
            return (self._can_move(piece, to_square, board_state) and (board_state[(to_square.file, to_square.rank)] is None))\
                or self._can_en_passant(piece, to_square, board_state)
        else:
            return self._can_move(piece, to_square)

    def is_capture_possible(self, piece, to_square, board_state = None):
        if not board_state is None:
            return (self._can_capture(piece, to_square) and not (board_state[(to_square.file, to_square.rank)] is None)
            and board_state[(to_square.file, to_square.rank)].color != piece.color) \
            or (self._can_en_passant(piece, to_square, board_state))
        else:
            return self._can_capture(piece, to_square)

    def is_attack_possible(self, piece, to_square, board_state):
        return self._can_capture(piece, to_square, board_state)

    def _make_en_passant_capture(self, board_state, piece, to_square):
        if board_state.en_passant_target_square and board_state.en_passant_target_square == to_square:
            board_state.pieces.remove(board_state[(to_square.file, to_square.rank - self._get_direction(piece.color))])
        else:
            raise ImpossibleMoveException('No en passant')

    def _set_en_passant_target_square(self, board_state, piece, to_square):
        if math.fabs(to_square.rank - piece.square.rank) == 2:
            board_state.en_passant_target_square = Square(to_square.file, piece.square.rank + self._get_direction(piece.color))
            board_state.is_en_passant_for_next = True

    def make_move(self, board_state, piece, to_square):
        try:
            self._make_en_passant_capture(board_state, piece, to_square)
        except ImpossibleMoveException:
            pass
        self._set_en_passant_target_square(board_state, piece, to_square)
        board_state[piece.square].square = to_square


class KnightMotionStrategy(MotionStrategy):
    def _can_move(self, piece, to_square, board_state = None):
        from_square = piece.square
        if (math.fabs(from_square.file-to_square.file) == 2 and math.fabs(from_square.rank-to_square.rank) == 1)\
        or (math.fabs(from_square.file-to_square.file) == 1 and math.fabs(from_square.rank-to_square.rank) == 2):
            return True
        else:
            return False

class BishopMotionStrategy(MotionStrategy):
    def _is_path_clear(self, board_state, from_square, to_square):
        if from_square.file<to_square.file:
            file_direction = 1
        else:
            file_direction = -1

        if from_square.rank<to_square.rank:
            rank_direction = 1
        else:
            rank_direction = -1

        current_square = copy.copy(from_square)
        current_square.file += file_direction
        current_square.rank += rank_direction
        while current_square!=to_square:
            if not (board_state[(current_square.file, current_square.rank)] is None):
                return False
            current_square.file += file_direction
            current_square.rank += rank_direction
        return True

    def _can_move(self, piece, to_square, board_state = None):
        from_square = piece.square
        result = math.fabs(from_square.file - to_square.file) == math.fabs(from_square.rank - to_square.rank)
        if board_state is None:
            return result
        else:
            return result and self._is_path_clear(board_state, from_square, to_square)


class RookMotionStrategy(MotionStrategy):
    def _is_path_clear(self, board_state, from_square, to_square):
        if from_square.rank == to_square.rank:
            rank_direction = 0
            if from_square.file<to_square.file:
                file_direction = 1
            else:
                file_direction = -1
        else:
            file_direction = 0
            if from_square.rank<to_square.rank:
                rank_direction = 1
            else:
                rank_direction = -1

        current_square = copy.copy(from_square)
        current_square.file += file_direction
        current_square.rank += rank_direction

        while current_square!=to_square:
            if not (board_state[(current_square.file, current_square.rank)] is None):
                return False
            current_square.file += file_direction
            current_square.rank += rank_direction
        return True

    def _can_move(self, piece, to_square, board_state = None):
        from_square = piece.square
        result = (from_square.file == to_square.file or from_square.rank == to_square.rank)
        if board_state is None:
            return result
        else:
            return result and self._is_path_clear(board_state, from_square, to_square)

class QueenMotionStrategy(MotionStrategy):

    def _can_move(self, piece, to_square, board_state = None):
        rook_strategy = RookMotionStrategy()
        bishop_strategy = BishopMotionStrategy()
        return rook_strategy._can_move(piece, to_square, board_state) or bishop_strategy._can_move(piece, to_square, board_state)