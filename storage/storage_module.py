from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload
from game.common import Move
from game.game_exceptions import MoveSavingException
from game.game_module import Game
from parsing.parsing_module import MoveParser

Base = declarative_base()

class Storage(object):

    def __init__(self, host = 'localhost', port = '3306', login = 'root', password = '123', db_name = 'chess'):
#        engine = create_engine('mysql+mysqldb://root:123@localhost:3306/chess', echo=True)
        engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (login, password, host, port, db_name), echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def save_game(self, game):
        self.session.add(game)
        self.session.commit()

        for i in range(len(game.moves)):
            try:
                self._process_move(game.moves[i], game.id, game.board_states[i+1])
            except :
                try:
                    self._process_move(game.moves[i], game.id, None)
                except :
                    raise MoveSavingException()
        self.session.add_all(game.moves)
        self.session.commit()
        return game.id

    def read_game(self, id, is_shallow = False):
        game = self.session.query(Game).get(id)
        if not is_shallow:
            game.moves = list(self.read_moves(id))
        return game

    def read_all_games(self, is_shallow = False):
        games = self.session.query(Game).all()
        for i in range(len(games)):
            if not is_shallow:
                games[i].moves = list(self.read_moves(games[i].id))
        return games

    def read_games(self, event, site, date, white, black):
        games = self.session.query(Game).filter(Game.event.like('%' + event + '%'),
            Game.site.like('%' + site + '%'), Game.date.like('%' + date + '%'),
            Game.white.like('%' + white + '%'), Game.black.like('%' + black + '%'), ).all()
        for i in range(len(games)):
            games[i].moves = list(self.read_moves(games[i].id))
        return games

    def read_moves(self, game_id):
        moves = self.session.query(Move).filter(Move.game_id == game_id).all()
        for i in range(len(moves)):
            moves[i] = MoveParser().parse(input_move=moves[i])
        return moves



    def _process_move(self, move, game_id, board_state):
        move.game_id = game_id
        try:
            serial = board_state.serialize()
            move.serial0 = serial[0]
            move.serial1 = serial[1]
            move.serial2 = serial[2]
            move.serial3 = serial[3]
        except :
            move.serial0 = 0
            move.serial1 = 0
            move.serial2 = 0
            move.serial3 = 0
