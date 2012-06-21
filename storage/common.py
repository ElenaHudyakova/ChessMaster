from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StatisticsItem():
    def __init__(self, move_notation = None, number = None, white_win_number = None, white_win = None):
        self.move_notation = move_notation
        self.number = number
        self.white_win_number = white_win_number
        self.white_win = white_win

    def count(self):
        self.white_win = 1.0 * self.white_win_number / self.number * 100