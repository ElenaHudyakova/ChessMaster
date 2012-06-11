import os
from game.common import Move, PieceType, Square
from game.game_exceptions import InvalidMoveRecordException
from parsing.parsing_module import MoveParser, ChessFile

__author__ = 'Lena'

import unittest

class MyTestCase(unittest.TestCase):

    path = os.path.dirname(__file__)

    def create_file(self, filename, content):
        file = open(filename, "w")
        file.write(content)

    def test_parse_king_castling(self):
        move = Move('O-O')
        move.parse(MoveParser())
        self.assertEqual(True, move.is_king_castling)

    def test_parse_queen_castling(self):
        move = Move('O-O-O')
        move.parse(MoveParser())
        self.assertEqual(True, move.is_queen_castling)

    def test_parse_promotion_move(self):
        move = Move('e8=Q')
        move.parse(MoveParser())
        self.assertEqual(True, move.is_promotion)
        self.assertEqual(PieceType.QUEEN, move.promotion_piece_type)

    def test_parse_simple_pawn_move(self):
        move = Move('e4')
        move.parse(MoveParser())
        self.assertEqual(Square('e', 4), move.to_square)
        self.assertEqual(PieceType.PAWN, move.piece_type)

    def test_parse_queen_move(self):
        move = Move('Qf6')
        move.parse(MoveParser())
        self.assertEqual(Square('f', 6), move.to_square)
        self.assertEqual(PieceType.QUEEN, move.piece_type)

    def test_parse_king_move(self):
        move = Move('Ke4')
        move.parse(MoveParser())
        self.assertEqual(Square('e', 4), move.to_square)
        self.assertEqual(PieceType.KING, move.piece_type)

    def test_parse_knight_with_from_file(self):
        move = Move('Ndf3')
        move.parse(MoveParser())
        self.assertEqual(Square('f', 3), move.to_square)
        self.assertEqual(Square('d', None), move.from_square)
        self.assertEqual(PieceType.KNIGHT, move.piece_type)

    def test_parse_knight_with_from_rank(self):
        move = Move('N4f3')
        move.parse(MoveParser())
        self.assertEqual(Square('f', 3), move.to_square)
        self.assertEqual(Square(None, 4), move.from_square)
        self.assertEqual(PieceType.KNIGHT, move.piece_type)

    def test_parse_rook_move(self):
        move = Move('Re4')
        move.parse(MoveParser())
        self.assertEqual(Square('e', 4), move.to_square)
        self.assertEqual(PieceType.ROOK, move.piece_type)

    def test_parse_bishop(self):
        move = Move('Bf3')
        move.parse(MoveParser())
        self.assertEqual(Square('f', 3), move.to_square)
        self.assertEqual(PieceType.BISHOP, move.piece_type)

    def test_parse_invalid_move(self):
        move = Move('Bfx3')
        self.assertRaises(InvalidMoveRecordException, move.parse, MoveParser())

    def test_no_file(self):
        self.assertRaises(IOError, ChessFile, "no_file")

    def test_empty_file(self):
        filename = os.path.join(self.path, "test_files/empty.pgn")
        self.create_file(filename, "")
        test_file = ChessFile(filename)
        self.assertRaises(StopIteration, test_file.next)

if __name__ == '__main__':
    unittest.main()
