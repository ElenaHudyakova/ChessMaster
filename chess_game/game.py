from storage.db_connection import session
from storage.db_classes import GameDB

BLACK = 1
WHITE = 0

ROOK = 0
KNIGHT = 1
BISHOP = 2
QUEEN = 3
KING = 4
PAWN = 5

from chess_game.board import BoardState

class Game(object):
    def __init__(self):
        self.tags = dict()
        self.moves = list()
        self.board_positions = list()

    def simulate(self):
        self.board_positions.append(BoardState.get_initial_board_position())
        for i in range(len(self.moves)):
            self.board_positions.append(self.board_positions[i].get_next_board_position(self.moves[i]))

    def save(self):
        game_db = GameDB()
        game_db.black = self.tags['Black']
        game_db.white = self.tags['White']
        game_db.date = self.tags['Date']
        game_db.event = self.tags['Event']
        game_db.result = self.tags['Result']
        game_db.site = self.tags['Site']
        game_db.round = self.tags['Round']
        session.add(game_db)
        session.commit()
        return game_db.id


    def read(self, id, connection):
        pass