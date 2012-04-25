import math
from chess_exceptions.chess_exceptions import *


class MotionStrategy(object):
    def move(self, board_position, from_point, to_point):
    # if move is impossible exception raised
        raise InvalidMoveException("no implementation")

    def capture(self, board_position, from_point, to_point):
    # if capture is impossible exception raised
        raise InvalidCaptureException("no implementation")

class KingMotionStrategy(MotionStrategy):
    def _can_move(self, game_point, from_point, to_point):
        if (math.fabs(from_point.file-to_point.file) <= 1) \
                and (math.fabs(from_point.rank-to_point.rank) <= 1):
            return True
        else:
            return False

    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[to_point.file][to_point.rank] is None \
                and  self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[to_point.file][to_point.rank] is None) \
                    and board_position[to_point.file][to_point.rank].color != board_position[from_point.file][from_point.rank].color \
                    and self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False

class PawnMotionStrategy(MotionStrategy):

    def _is_first_move(self, from_point):
        if from_point.rank == 2:
            return True
        else:
            return False

    def _can_move(self, game_point, from_point, to_point):
        pass

    def _can_capture(self, game_point, from_point, to_point):
        pass

    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[to_point.file][to_point.rank] is None\
                and  self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[to_point.file][to_point.rank] is None)\
           and board_position[to_point.file][to_point.rank].color != board_position[from_point.file][from_point.rank].color\
        and self._can_capture(board_position, from_point, to_point):
            return True
        else:
            return False

