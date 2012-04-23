import math
from exceptions.chess_exceptions import InvalidMoveException, InvalidCaptureException

class MotionStrategy(object):
    def move(self, game_position, from_position, to_position):
    # if move is impossible exception raised
        raise InvalidMoveException("no implementation yet")

    def capture(self, game_position, from_position, to_position):
    # if capture is impossible exception raised
        raise InvalidCaptureException("no implementation yet")

class KingMotionStrategy(MotionStyle):
    def _canMove(self, game_position, from_position, to_position):
        if (math.fabs(from_position.file-to_position.file) <= 1) and (math.fabs(from_position.rank-to_position.rank) <= 1):
            return True
        else:
            return False

    def move(self, game_position, from_position, to_position):
    # if move is impossible exception raised
        if game_position[to_position.file][to_position.rank] is None or not self._canMove(game_position, from_position, to_position):
            raise InvalidMoveException("King can not move from " + str(from_position) + " to " + str(to_position))


    def capture(self, game_position, from_position, to_position):
    # if capture is impossible exception raised
        if game_position[to_position.file][to_position.rank] is None \
                    or game_position[to_position.file][to_position.rank].color == game_position[from_position.file][from_position.rank].color \
                    or not self._canMove(game_position, from_position, to_position):
            raise InvalidCaptureException("King " + str(from_position) + " can not capture piece on " + str(to_position))


