import os
import sys
from tempfile import NamedTemporaryFile
import uuid
from game.common import Move, PieceType, Square, Color
from game.game_exceptions import InvalidMoveRecordException, InvalidGameException
from parsing.parsing_module import MoveParser, ChessFile

__author__ = 'Lena'

import unittest

class ParsingTestCase(unittest.TestCase):

    path = os.path.dirname(__file__)

    def create_file(self, filename, content):
        file = open(filename, "w")
        file.write(content)

    def test_parse_king_castling(self):
        move = MoveParser().parse('O-O')
        self.assertEqual(True, move.is_king_castling)

    def test_parse_queen_castling(self):
        move = MoveParser().parse('O-O-O')
        self.assertEqual(True, move.is_queen_castling)

    def test_parse_promotion_move(self):
        move = MoveParser().parse('e8=Q')
        self.assertEqual(True, move.is_promotion)
        self.assertEqual(PieceType.QUEEN, move.promotion_piece_type)

    def test_parse_simple_pawn_move(self):
        move = MoveParser().parse('e4')
        self.assertEqual(Square('e', 4), move.to_square)
        self.assertEqual(PieceType.PAWN, move.piece_type)

    def test_parse_queen_move(self):
        move = MoveParser().parse('Qf6')
        self.assertEqual(Square('f', 6), move.to_square)
        self.assertEqual(PieceType.QUEEN, move.piece_type)

    def test_parse_king_move(self):
        move = MoveParser().parse('Ke4')
        self.assertEqual(Square('e', 4), move.to_square)
        self.assertEqual(PieceType.KING, move.piece_type)

    def test_parse_knight_with_from_file(self):
        move = MoveParser().parse('Ndf3')
        self.assertEqual(Square('f', 3), move.to_square)
        self.assertEqual(Square('d', None), move.from_square)
        self.assertEqual(PieceType.KNIGHT, move.piece_type)

    def test_parse_knight_with_from_rank(self):
        move = MoveParser().parse('N4f3')
        self.assertEqual(Square('f', 3), move.to_square)
        self.assertEqual(Square(None, 4), move.from_square)
        self.assertEqual(PieceType.KNIGHT, move.piece_type)

    def test_parse_rook_move(self):
        move = MoveParser().parse('Re4')
        self.assertEqual(Square('e', 4), move.to_square)
        self.assertEqual(PieceType.ROOK, move.piece_type)

    def test_parse_bishop(self):
        move = MoveParser().parse('Bf3')
        self.assertEqual(Square('f', 3), move.to_square)
        self.assertEqual(PieceType.BISHOP, move.piece_type)

    def test_parse_invalid_move(self):
        self.assertRaises(InvalidMoveRecordException, MoveParser().parse, 'Bfx3')

    def test_parse_invalid_move2(self):
        self.assertRaises(InvalidMoveRecordException, MoveParser().parse, 'Bxc6Rxa5')

    def test_no_file(self):
        file = NamedTemporaryFile(delete=False)
        test_file = ChessFile(file.name + uuid.uuid4().hex[:16])
        self.assertRaises(StopIteration, test_file.next)

    def test_empty_file(self):
        file = NamedTemporaryFile(delete=False)
        test_file = ChessFile(file.name)
        self.assertRaises(StopIteration, test_file.next)

    def test_parse_one_game_file(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual(79, len(game.moves))
        self.assertRaises(StopIteration, test_file.next)

    def test_parse_two_games_file(self):
        filename = os.path.join(self.path, "test_files/two_games.pgn")
        test_file = ChessFile(filename)
        game1 = test_file.next()
        game2 = test_file.next()
        self.assertEqual('Ch World Yunior\'s ( under 20 )', game1.event)
        self.assertEqual('?', game2.event)
        self.assertRaises(StopIteration, test_file.next)

    def test_parse_event(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('Ch World Yunior\'s ( under 20 )', game.event)


    def test_parse_site(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('Kiev', game.site)

    def test_parse_date(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('1973.??.??', game.date)

    def test_parse_round(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('?', game.round)

    def test_parse_white(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('Kasparov Garry', game.white)

    def test_parse_black(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('Vasilienko', game.black)

    def test_parse_black(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual('1-0', game.result)

    def test_parse_invalid_game(self):
        filename = os.path.join(self.path, "test_files/invalid_game.pgn")
        test_file = ChessFile(filename)
        self.assertRaises(InvalidGameException, test_file.next)

    def test_parse_with_init(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        test_file = ChessFile(filename)
        game = test_file.next()
        test_file.init()
        game = test_file.next()
        self.assertRaises(StopIteration, test_file.next)

    def test_add_game_to_file(self):
        filename1 = os.path.join(self.path, "test_files/two_games.pgn")
        filename2 = os.path.join(self.path, "test_files/new_file.pgn")
        file = open(filename2, 'w')
        file.close()
        test_file1 = ChessFile(filename1)
        test_file2 = ChessFile(filename2)
        game1 = test_file1.next()
        game2 = test_file1.next()

        test_file2.add_game(game1)
        test_file2.add_game(game2)
        test_file2.next()
        test_file2.next()

        self.assertRaises(StopIteration, test_file2.next)

if __name__ == '__main__':
    unittest.main()
