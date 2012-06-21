import re
from game.common import Square, PieceType, Move, Color
from game.game_exceptions import InvalidMoveRecordException, InvalidGameException
from game.game_module import Game

class MoveParser(object):
    def parse(self, notation = '', color = Color.WHITE, input_move = None):
        if input_move is None:
            move = Move()
            move.color = color
            move.notation = notation
        else:
            move = input_move
        is_castling = self._parse_castling_move(move)
        if not is_castling:
            try:
                m = re.match(r"^(?P<piece>[BRKQN]?)(?P<from_file>[a-h]?)(?P<from_rank>[1-8]?)(?P<is_capture>x?)(?P<to_file>[a-h])(?P<to_rank>[1-8])((?P<is_promotion>=)(?P<promotion_piece_type>[BRKQN]))?(?P<is_check>\+?)$", move.notation)
                move.piece_type = self._get_piece_type(m.group("piece"))
                move.to_square = Square(m.group("to_file"), int(m.group("to_rank")))
                try:
                    move.from_square = Square(m.group("from_file"), int(m.group("from_rank")))
                except :
                    move.from_square = Square(m.group("from_file"), None)
                move.is_capture = m.group("is_capture") == "x"
                move.is_check = m.group("is_check") == "+"
                move.is_promotion = m.group("is_promotion") == "="
                if move.is_promotion:
                    move.promotion_piece_type = self._get_piece_type(m.group("promotion_piece_type"))
            except Exception as err:
                raise InvalidMoveRecordException(move.notation)
        return move


    def _parse_castling_move(self, move):
        if move.notation == "O-O":
            move.is_king_castling = True
        else:
            move.is_king_castling = False
        if move.notation == "O-O-O":
            move.is_queen_castling = True
        else:
            move.is_queen_castling = False

        return move.is_king_castling or move.is_queen_castling

    def _get_piece_type(self, letter):
        return {
            'B': lambda: PieceType.BISHOP,
            'R': lambda: PieceType.ROOK,
            'K': lambda: PieceType.KING,
            'Q': lambda: PieceType.QUEEN,
            'N': lambda: PieceType.KNIGHT,
            '': lambda: PieceType.PAWN,
            }[letter]()

class ChessFile(object):
    """A Class-wrapper for PGN file which allows iterating through chess games in that file"""
    START_TAG = "Event"

    def __init__(self, filename):
        try:
            self.file = open(filename)
        except IOError:
            self.file = open(filename, "w")
            self.file = open(filename, 'r')

        self.filename = filename
        self._eof = False
        self._startTagLine = None

    def __iter__(self):
        return self

    def _parse_tag(self, line, game):
        line = line.lstrip()
        line = line[1:-1]
        tag_name, tag_value = line.split(" ", 1)
        tag_value = tag_value[1:-1]
        try:
            setattr(game, tag_name.lower(), tag_value)
        except :
            pass

    def _parse_moves(self, line, game):
        line = line.strip()
        move_number = 0
        for move_pair in re.split("\d+\.", line):
            if move_pair:
                move_pair = move_pair.strip()
                for move_str in re.split("\s+", move_pair):
                        if move_str == '1-0' or move_str == '0-1' or move_str == '1/2-1/2':
                            break
                        move = MoveParser().parse(move_str)
                        if move_number % 2 == 0:
                            move.color = Color.WHITE
                        else:
                            move.color = Color.BLACK
                        move.fullmove_number = move_number/2 + 1
                        game.moves.append(move)
                        move_number += 1


    def _parse_game(self, notation_str, game):
        notation_str = notation_str.replace("\n", " ")
        while "]" in notation_str:
            tag_line = notation_str.split("]", 1)[0] + "]"
            notation_str = notation_str.split("]", 1)[1]
            self._parse_tag(tag_line, game)
        self._parse_moves(notation_str, game)

    def init(self):
        self.file = open(self.filename, 'r')
        self.file.seek(0)
        self._eof = False
        self._startTagLine = ''

    def next(self):
        game = Game()
        notation_str = ""

        if self._startTagLine:
            notation_str += self._startTagLine

        line = self.file.readline()
        if self._eof or not len(line):
            raise StopIteration

        while 1:
            if not len(line):
                self._eof = True
                break
            else:
                if (self.START_TAG in line) and (self.START_TAG in notation_str):
                    self._startTagLine = line
                    break
                else:
                    notation_str += line
            line = self.file.readline()

        try:
            self._parse_game(notation_str, game)
        except InvalidMoveRecordException:
            raise InvalidGameException()

        return game

    def _get_tag_line(self, tag_name, value):
        if value == '':
            return '[%s "?"]\n' % tag_name
        else:
            return '[%s "%s"]\n' % (tag_name, value)

    def _get_PGN_notation(self, game):
        game_notation = ''
        game_notation += '\n'
        game_notation += self._get_tag_line('Event', game.event)
        game_notation += self._get_tag_line('Site', game.site)
        game_notation += self._get_tag_line('Date', game.date)
        game_notation += self._get_tag_line('Round', game.round)
        game_notation += self._get_tag_line('White', game.white)
        game_notation += self._get_tag_line('Black', game.black)
        game_notation += self._get_tag_line('Result', game.result)

        game_notation += '\n'

        for move in game.moves:
            if move.color == Color.WHITE:
                game_notation += '%s.%s ' % (str(move.fullmove_number), move.notation)
            else:
                game_notation += '%s ' % move.notation
                if move.fullmove_number % 4 == 0:
                    game_notation += '\n'

        game_notation += game.result
        game_notation += '\n\n'

        return game_notation

    def add_game(self, game):
        self.file = open(self.filename, 'a')
        self.file.write(self._get_PGN_notation(game))
        self.init()