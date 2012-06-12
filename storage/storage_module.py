from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from game.game_exceptions import MoveSavingException
from game.game_module import Game

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
                self._save_move(game.moves[i], game.id, game.board_states[i+1])
            except :
                raise MoveSavingException()
        return game.id

    def read_game(self, id):
        game = Game()
        game = self.session.query(Game).get(id)
        print len(game.moves)

    def read_all_games(self):
        return self.session.query(Game).all()

    def read_games(self):
        pass

    def _save_move(self, move, game_id, board_state):
        move.game_id = game_id
        serial = board_state.serialize()
        move.serial0 = serial[0]
        move.serial1 = serial[1]
        move.serial2 = serial[2]
        move.serial3 = serial[3]
        self.session.add(move)
        self.session.commit()
