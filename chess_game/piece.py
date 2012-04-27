from chess_game.motion_strategies import MotionStrategy

class Piece(object):
    def __init__(self, motion_strategy, point, color):
        self.motion_strategy = motion_strategy
        self.type = None
        self.point = point
        self.color = color

    def __str__(self):
        return str(self.type) + " " + str(self.point) + " " + str(self.color)