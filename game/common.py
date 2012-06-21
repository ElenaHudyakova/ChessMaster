from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BIGINT, BLOB, NUMERIC
from game_exceptions import InvalidSquareCoordException
from storage.common import Base


class Color:
    WHITE = 0
    BLACK = 1

class Square(object):

    def __init__(self, file, rank):
        self.file = file
        self.rank = rank

    def __setattr__(self, key, value):
        if type(value).__name__ == 'int':
            if (value<9) and (value>0):
                self.__dict__[key] = value
            else:
                raise InvalidSquareCoordException(str(value), key)

        if value is None or value == '':
            self.__dict__[key] = None
            return

        if (type(value).__name__ == 'str') and (key == 'file'):
            try:
                self.__dict__[key] = {
                    'a': lambda: 1,
                    'b': lambda: 2,
                    'c': lambda: 3,
                    'd': lambda: 4,
                    'e': lambda: 5,
                    'f': lambda: 6,
                    'g': lambda: 7,
                    'h': lambda: 8
                }[value]()
            except KeyError:
                raise InvalidSquareCoordException(str(value), key)

    def __cmp__(self, other):
        if (self.file == other.file) and (self.rank == other.rank):
            return 0
        else:
            return 1

    @staticmethod
    def digit_to_file(digit):
        return  {
            1: lambda: 'a',
            2: lambda: 'b',
            3: lambda: 'c',
            4: lambda: 'd',
            5: lambda: 'e',
            6: lambda: 'f',
            7: lambda: 'g',
            8: lambda: 'h',
            None: lambda: 'None'
        }[digit]()


    def __str__(self):
        file = self.digit_to_file(self.file)
        return "(" + file + ", " + str(self.rank) + ")"

class PieceType:
    KING = 4
    KNIGHT = 1
    ROOK = 0
    BISHOP = 2
    QUEEN = 3
    PAWN = 5
    NONE = 6

    def str(self, type):
        try:
            return {
                PieceType.KING: lambda: 'K',
                PieceType.KNIGHT: lambda: 'N',
                PieceType.ROOK: lambda: 'R',
                PieceType.BISHOP: lambda: 'B',
                PieceType.QUEEN: lambda: 'Q',
                PieceType.PAWN: lambda: 'P',
                PieceType.NONE: lambda: 'NONE'
            }[type]()
        except KeyError:
            raise Exception('Invalid piece type')


class Move(Base):
    __tablename__ = 'moves'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    notation = Column(String)
    fullmove_number = Column(Integer)
    color = Column(Integer)
    serial1 = Column(NUMERIC)
    serial2 = Column(NUMERIC)
    serial3 = Column(NUMERIC)
    serial0 = Column(NUMERIC)

    def __init__(self, notation = '', color = Color.WHITE):
        self.notation = notation
        self.color = color

        self.piece_type = PieceType.NONE
        self.to_square = None
        self.from_square = None
        self.is_capture = False
        self.is_check = False
        self.is_promotion = False
        self.promotion_piece_type = PieceType.NONE
        self.is_king_castling = False
        self.is_queen_castling = False

    def __cmp__(self, other):
        if (self.notation == other.notation) and (self.color == other.color):
            return 0
        else:
            return 1

    def __str__(self):
        if int(self.color) == Color.WHITE:
            return str(self.fullmove_number) + '. ' + self.notation
        else:
            return str(self.fullmove_number) + '...   ' + self.notation
