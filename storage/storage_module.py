from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from game.common import Move
from game.game_exceptions import MoveSavingException
from game.game_module import Game
from parsing.parsing_module import MoveParser
from storage.common import StatisticsItem


class Storage(object):

    def __init__(self, host = 'localhost', port = '3306', login = 'root', password = '123', db_name = 'chess'):
#        engine = create_engine('mysql+mysqldb://root:123@localhost:3306/chess', echo=True)
        self.engine = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (login, password, host, port, db_name), echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def save_game(self, game):
        self.session.add(game)
        self.session.commit()

        is_quick_import = len(game.board_states)

        if len(game.moves) == 0:
            return

        for i in range(len(game.moves)):
            if is_quick_import:
                self._process_move(game.moves[i], game.id, game.board_states[i+1])
            else:
                self._process_move(game.moves[i], game.id, None)

        query = "), (".join(["%d, '%s', %d, %d, %d, %d, %d, %d" % (move.game_id, move.notation, move.fullmove_number, move.color, move.serial0, move.serial1, move.serial2, move.serial3) for move in game.moves])

        query = "INSERT INTO moves (`game_id`, `notation`, `fullmove_number`, `color`, `serial0`, `serial1`, `serial2`, `serial3`) VALUES (%s)" % query
        self.engine.execute(query)
        self.session.expire_all()
        self.session.commit()
#        return game.id

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

    def read_games(self, event = '', site = '', date = '', white = '', black = '', board_state = None):
        games = self.session.query(Game).filter(Game.event.like('%' + event + '%'),
            Game.site.like('%' + site + '%'), Game.date.like('%' + date + '%'),
            Game.white.like('%' + white + '%'), Game.black.like('%' + black + '%'), ).all()
        for i in range(len(games)):
            games[i].moves = list(self.read_moves(games[i].id))

        result = []

        if not board_state is None:
            serial = board_state.serialize()
            for i in range(len(games)):
                for move in games[i].moves:
                    if [move.serial0, move.serial1, move.serial2, move.serial3] == serial:
                        result.append(games[i])
                        break
        else:
            result = games

        return result

    def read_moves(self, game_id):
        moves = self.session.query(Move).filter(Move.game_id == game_id).all()
        for i in range(len(moves)):
            moves[i] = MoveParser().parse(input_move=moves[i])
        return moves



    def _process_move(self, move, game_id, board_state):
        move.game_id = game_id
        if board_state is None:
            move.serial0 = move.serial1 = move.serial2 = move.serial3 = 0
        else:
            serial = board_state.serialize()
            move.serial0 = serial[0]
            move.serial1 = serial[1]
            move.serial2 = serial[2]
            move.serial3 = serial[3]

    def get_staticstics(self, board_state):
        statistics = []
        serial = board_state.serialize()
        games = self.read_games(board_state = board_state)
        for game in games:
            is_found = False
            for move in game.moves:
                if is_found:
                    next_move_notation = move.notation
                    break
                if [move.serial0, move.serial1, move.serial2, move.serial3] == serial:
                    is_found = True
            white_win = game.result == '1-0'

            is_considered = False
            for statistics_item in statistics:
                if statistics_item.move_notation == next_move_notation:
                    is_considered = True
                    statistics_item.number += 1
                    if white_win:
                        statistics_item.white_win_number += 1
                    break
            if not is_considered:
                new_item = StatisticsItem()
                new_item.move_notation = next_move_notation
                new_item.number = 1
                if white_win:
                    new_item.white_win_number = 1
                else:
                    new_item.white_win_number = 0
                statistics.append(new_item)

        for statistics_item in statistics:
            statistics_item.count()

        return statistics
