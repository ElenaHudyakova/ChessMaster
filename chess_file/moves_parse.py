import re
from chess_game.game import *
from chess_game.board import Point

def parse_move(move):
    if move.algebraic_notation == "O-O":
        move.is_king_castling = True
        move.is_queen_castling = False
    else:
        if move.algebraic_notation == "O-O-O":
            move.is_king_castling = False
            move.is_queen_castling = True
        else:
            try:
                m = re.match(r"(?P<piece>[BRKQN]?)(?P<from_file>[a-h]?)(?P<from_rank>[1-8]?)(?P<is_capture>x?)(?P<to_file>[a-h])(?P<to_rank>[1-8])(?P<is_check>\+?)", move.algebraic_notation)
                move.piece = {
                    'B': lambda: BISHOP,
                    'R': lambda: ROOK,
                    'K': lambda: KING,
                    'Q': lambda: QUEEN,
                    'N': lambda: KNIGHT,
                     '': lambda: PAWN,
                    }[m.group("piece")]()
                move.to_point = Point(m.group("to_file"), int(m.group("to_rank")))
                try:
                    move.from_point = Point(m.group("from_file"), int(m.group("from_rank")))
                except :
                    move.from_point = Point(m.group("from_file"), None)
                if m.group("is_capture") == "x":
                    move.is_capture = True
                else:
                    move.is_capture = False
                if m.group("is_check") == "+":
                    move.is_check = True
                else:
                    move.is_check = False
            except :
                raise Exception("Panic! Not implemented exception " + move.algebraic_notation)
