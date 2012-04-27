import copy
import math
from chess_game.game import *


class MotionStrategy(object):
    def is_move_possible(self, board_position, from_point, to_point):
        pass

    def is_capture_possible(self, board_position, from_point, to_point):
        pass

class KingMotionStrategy(MotionStrategy):
    def _can_move(self, from_point, to_point):
        if (math.fabs(from_point.file-to_point.file) <= 1) \
                and (math.fabs(from_point.rank-to_point.rank) <= 1):
            return True
        else:
            return False

    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[(to_point.file, to_point.rank)] is None \
                and  self._can_move(from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[(to_point.file, to_point.rank)] is None) \
                    and board_position[(to_point.file, to_point.rank)].color != board_position[(from_point.file, from_point.rank)].color \
                    and self._can_move(from_point, to_point):
            return True
        else:
            return False

class PawnMotionStrategy(MotionStrategy):

    def _is_first_move(self, color, from_point):
        if (from_point.rank == 2 and color == WHITE) or (from_point.rank == 7 and color == BLACK):
            return True
        else:
            return False

    def _can_move(self, color, from_point, to_point):
        if color == WHITE:
            direction = 1
        else:
            direction = -1
        if self._is_first_move(color, from_point):
            if to_point.file == from_point.file and (to_point.rank == from_point.rank + direction or to_point.rank == from_point.rank + direction*2):
                return True
            else:
                return False
        else:
            if to_point.file == from_point.file and to_point.rank == from_point.rank + direction:
                return True
            else:
                return False

    def _can_capture(self, board_position, from_point, to_point):
        if board_position.active_color == WHITE:
            direction = 1
        else:
            direction = -1
        if math.fabs(from_point.file-to_point.file) == 1 and from_point.rank + direction == to_point.rank:
            return True
        else:
            return False


    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[(to_point.file,to_point.rank)] is None\
                and  self._can_move(board_position.active_color, from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[(to_point.file, to_point.rank)] is None)\
           and board_position[(to_point.file, to_point.rank)].color != board_position[(from_point.file, from_point.rank)].color\
        and self._can_capture(board_position, from_point, to_point):
            return True
        else:
            return False

class KnightMotionStrategy(MotionStrategy):
    def _can_move(self, from_point, to_point):
        if (math.fabs(from_point.file-to_point.file) == 2 and math.fabs(from_point.rank-to_point.rank) == 1)\
                or (math.fabs(from_point.file-to_point.file) == 1 and math.fabs(from_point.rank-to_point.rank) == 2):
            return True
        else:
            return False

    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[(to_point.file,to_point.rank)] is None\
        and  self._can_move(from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[(to_point.file, to_point.rank)] is None)\
           and board_position[(to_point.file, to_point.rank)].color != board_position[(from_point.file, from_point.rank)].color\
        and self._can_move(from_point, to_point):
            return True
        else:
            return False

class BishopMotionStrategy(MotionStrategy):
    def _is_path_clear(self, board_position, from_point, to_point):
        if from_point.file<to_point.file:
            file_direction = 1
        else:
            file_direction = -1

        if from_point.rank<to_point.rank:
            rank_direction = 1
        else:
            rank_direction = -1

        #current_point = Point(from_point.file+file_direction, from_point.rank+rank_direction)
        current_point = copy.copy(from_point)
        current_point.file += file_direction
        current_point.rank += rank_direction
        while current_point!=to_point:
            if not (board_position[(current_point.file, current_point.rank)] is None):
                return False
            current_point.file += file_direction
            current_point.rank += rank_direction
        return True

    def _can_move(self, board_position, from_point, to_point):
        if math.fabs(from_point.file-to_point.file) == math.fabs(from_point.rank-to_point.rank) \
                and (self._is_path_clear(board_position, from_point, to_point)):
            return True
        else:
            return False

    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[(to_point.file,to_point.rank)] is None\
            and  self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[(to_point.file, to_point.rank)] is None)\
           and board_position[(to_point.file, to_point.rank)].color != board_position[(from_point.file,from_point.rank)].color\
        and self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False

class RookMotionStrategy(MotionStrategy):
    def _is_path_clear(self, board_position, from_point, to_point):
        if from_point.rank == to_point.rank:
            rank_direction = 0
            if from_point.file<to_point.file:
                file_direction = 1
            else:
                file_direction = -1
        else:
            file_direction = 0
            if from_point.rank<to_point.rank:
                rank_direction = 1
            else:
                rank_direction = -1

        current_point = copy.copy(from_point)
        current_point.file += file_direction
        current_point.rank += rank_direction

        while current_point!=to_point:
            if not (board_position[(current_point.file, current_point.rank)] is None):
                return False
            current_point.file += file_direction
            current_point.rank += rank_direction
        return True

    def _can_move(self, board_position, from_point, to_point):
        if (from_point.file == to_point.file or from_point.rank == to_point.rank) and (self._is_path_clear(board_position, from_point, to_point)):
            return True
        else:
            return False

    def is_move_possible(self, board_position, from_point, to_point):
        if board_position[(to_point.file,to_point.rank)] is None\
        and  self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        if not (board_position[(to_point.file, to_point.rank)] is None)\
           and board_position[(to_point.file, to_point.rank)].color != board_position[(from_point.file,from_point.rank)].color\
        and self._can_move(board_position, from_point, to_point):
            return True
        else:
            return False



class QueenMotionStrategy(MotionStrategy):

    def is_move_possible(self, board_position, from_point, to_point):
        rook_strategy = RookMotionStrategy()
        bishop_strategy = BishopMotionStrategy()
        if board_position[(to_point.file,to_point.rank)] is None\
        and (rook_strategy._can_move(board_position, from_point, to_point) or bishop_strategy._can_move(board_position, from_point, to_point)):
            return True
        else:
            return False

    def is_capture_possible(self, board_position, from_point, to_point):
        rook_strategy = RookMotionStrategy()
        bishop_strategy = BishopMotionStrategy()
        if not (board_position[(to_point.file, to_point.rank)] is None)\
           and board_position[(to_point.file, to_point.rank)].color != board_position[(from_point.file,from_point.rank)].color\
        and (rook_strategy._can_move(board_position, from_point, to_point) or bishop_strategy._can_move(board_position, from_point, to_point)):
            return True
        else:
            return False