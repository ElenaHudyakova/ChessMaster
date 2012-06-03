import re
from chess_exceptions.chess_exceptions import InvalidMoveRecord
from chess_game.game import *
from chess_game.point import Point

def _parse_castling_move(move):
    if move.algebraic_notation == "O-O":
        move.is_king_castling = True
        return True
    else:
        if move.algebraic_notation == "O-O-O":
            move.is_queen_castling = True
            return True
    return False

def _get_piece_type(letter):
    return {
        'B': lambda: BISHOP,
        'R': lambda: ROOK,
        'K': lambda: KING,
        'Q': lambda: QUEEN,
        'N': lambda: KNIGHT,
        '': lambda: PAWN,
        }[letter]()

def parse_move(move):
    is_castling = _parse_castling_move(move)
    if not is_castling:
            try:
                m = re.match(r"(?P<piece>[BRKQN]?)(?P<from_file>[a-h]?)(?P<from_rank>[1-8]?)(?P<is_capture>x?)(?P<to_file>[a-h])(?P<to_rank>[1-8])(?P<is_promotion>=?)(?P<promotion_piece_type>[BRKQN]?)(?P<is_check>\+?)", move.algebraic_notation)
                move.piece_type = _get_piece_type(m.group("piece"))
                move.to_point = Point(m.group("to_file"), int(m.group("to_rank")))
                try:
                    move.from_point = Point(m.group("from_file"), int(m.group("from_rank")))
                except :
                    move.from_point = Point(m.group("from_file"), None)
                move.is_capture = m.group("is_capture") == "x"
                move.is_check = m.group("is_check") == "+"
                move.is_promotion = m.group("is_promotion") == "="
                if move.is_promotion:
                    move.promotion_piece_type = _get_piece_type(m.group("promotion_piece_type"))
            except ValueError:
                raise InvalidMoveRecord("Invalid move record " + move.algebraic_notation + " in file")
