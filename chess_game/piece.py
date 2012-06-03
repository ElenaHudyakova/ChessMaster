
class Piece(object):
    def __init__(self, motion_strategy, point, color):
        self._motion_strategy = motion_strategy
        self.type = None
        self.point = point
        self.color = color

    def __str__(self):
        return str(self.type) + " " + str(self.point) + " " + str(self.color)

    def can_move(self, board_state, to_point):
        return self._motion_strategy.is_move_possible(board_state, self.point, to_point)

    def can_capture(self,  board_state, to_point):
        return self._motion_strategy.is_capture_possible(board_state, self.point, to_point)

    def move(self, board_state, to_point):
        self._motion_strategy.make_move(board_state, self.point, to_point)

    def capture(self, board_state, to_point):
        self._motion_strategy.make_capture(board_state, self.point, to_point)


