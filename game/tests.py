import unittest
from game.common import Move
from game.game_module import BoardState, Square, Color, Game
from game.game_exceptions import InvalidSquareCoordException, InvalidBoardSquare, ImpossibleMoveException, InvalidGameException
from game.pieces import PieceCreator, PieceType
from parsing.parsing_module import MoveParser


class MyTestCase(unittest.TestCase):

    def test_impossible_square_file(self):
        self.assertRaises(InvalidSquareCoordException, Square, 't', 4)

    def test_impossible_square_rank(self):
        self.assertRaises(InvalidSquareCoordException, Square, 'a', 0)

    def test_impossible_board_square(self):
        board = BoardState()
        self.assertRaises(InvalidBoardSquare, board.__getitem__, 3)

    def test_knight_possible_move_d4_e6(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('e', 6), board))


    def test_knight_possible_move_d4_f5(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('f', 5), board))

    def test_knight_possible_move_d4_f3(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('f', 3), board))

    def test_knight_possible_move_d4_c2(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('c', 2), board))

    def test_knight_possible_move_d4_b3(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('b', 3), board))

    def test_knight_possible_move_d4_b5(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('b', 5), board))

    def test_knight_possible_move_d4_c6(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(True, board[('d', 4)].can_move(Square('c', 6), board))

    def test_knight_impossible_move_d4_f4(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(False, board[('d', 4)].can_move(Square('f', 4), board))

    def test_knight_move_to_occupied_square(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 3), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 4)].can_move(Square('f', 3), board))
        self.assertEqual(False, board[('d', 4)].can_capture(Square('f', 3), board))


    def test_knight_capture(self):
        board = BoardState()
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('d', 4), Color.WHITE)
        board.add_piece(knight)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 3), Color.BLACK)
        board.add_piece(pawn)
        self.assertEqual(True, board[('d', 4)].can_capture(Square('f', 3), board))
        self.assertEqual(False, board[('d', 4)].can_move(Square('f', 3), board))

    def test_king_move_f5_f6(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('f', 5), Color.WHITE)
        board.add_piece(king)
        self.assertEqual(True, board[('f', 5)].can_move(Square('f', 6), board))

    def test_king_move_f5_e5(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('f', 5), Color.WHITE)
        board.add_piece(king)
        self.assertEqual(True, board[('f', 5)].can_move(Square('e', 5), board))

    def test_king_move_f5_g4(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('f', 5), Color.WHITE)
        board.add_piece(king)
        self.assertEqual(True, board[('f', 5)].can_move(Square('g', 4), board))

    def test_king_impossible_move(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('f', 5), Color.WHITE)
        board.add_piece(king)
        self.assertEqual(False, board[('f', 5)].can_move(Square('a', 5), board))

    def test_king_move_to_occupied_square(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('f', 5), Color.WHITE)
        board.add_piece(king)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 4), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('f', 5)].can_move(Square('f', 4), board))
        self.assertEqual(False, board[('f', 5)].can_capture(Square('f', 4), board))

    def test_king_capture(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('f', 5), Color.WHITE)
        board.add_piece(king)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 4), Color.BLACK)
        board.add_piece(pawn)
        self.assertEqual(False, board[('f', 5)].can_move(Square('f', 4), board))
        self.assertEqual(True, board[('f', 5)].can_capture(Square('f', 4), board))

    def test_rook_move_d5_d8(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        self.assertEqual(True, board[('d', 5)].can_move(Square('d', 8), board))

    def test_rook_move_d5_d1(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        self.assertEqual(True, board[('d', 5)].can_move(Square('d', 1), board))

    def test_rook_move_d5_a5(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        self.assertEqual(True, board[('d', 5)].can_move(Square('a', 5), board))

    def test_rook_no_move_d5_a4(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        self.assertEqual(False, board[('d', 5)].can_move(Square('a', 4), board))

    def test_rook_move_d5_h5(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        self.assertEqual(True, board[('d', 5)].can_move(Square('h', 5), board))

    def test_rook_impossible_move_d5_d8(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('d', 7), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('d', 8), board))

    def test_rook_impossible_move_d5_d1(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('d', 3), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('d', 1), board))

    def test_rook_impossible_move_d5_a5(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('c', 5), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('a', 5), board))

    def test_rook_impossible_move_d5_h5(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('e', 5), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('h', 5), board))

    def test_rook_move_to_occupied_square(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('e', 5), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('e', 5), board))
        self.assertEqual(False, board[('d', 5)].can_capture(Square('e', 5), board))

    def test_rook_capture(self):
        board = BoardState()
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.WHITE)
        board.add_piece(rook)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('e', 5), Color.BLACK)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('e', 5), board))
        self.assertEqual(True, board[('d', 5)].can_capture(Square('e', 5), board))

    def test_bishop_possible_move_d5_a8(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        self.assertEqual(True, board[('d', 5)].can_move(Square('a', 8), board))

    def test_bishop_possible_move_d5_f7(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        self.assertEqual(True, board[('d', 5)].can_move(Square('f', 7), board))

    def test_bishop_possible_move_d5_a2(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        self.assertEqual(True, board[('d', 5)].can_move(Square('a', 2), board))

    def test_bishop_possible_move_d5_h1(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        self.assertEqual(True, board[('d', 5)].can_move(Square('h', 1), board))

    def test_bishop_impossible_move_d5_a8(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('b', 7), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('a', 8), board))

    def test_bishop_impossible_move_d5_f7(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('e', 6), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('f', 7), board))

    def test_bishop_impossible_move_d5_a2(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('b', 3), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('a', 2), board))

    def test_bishop_impossible_move_d5_h1(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('g', 2), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('h', 1), board))

    def test_bishop_move_to_occupied_square(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('a', 8), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 5)].can_move(Square('a', 8), board))
        self.assertEqual(False, board[('d', 5)].can_capture(Square('a', 8), board))

    def test_bishop_capture(self):
        board = BoardState()
        bishop = PieceCreator().create_piece(PieceType.BISHOP, Square('d', 5), Color.WHITE)
        board.add_piece(bishop)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('a', 8), Color.BLACK)
        board.add_piece(pawn)
        self.assertEqual(True, board[('d', 5)].can_capture(Square('a', 8), board))
        self.assertEqual(False, board[('d', 5)].can_move(Square('a', 8), board))

    def test_queen_possible_move_like_bishop(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        self.assertEqual(True, board[('d', 4)].can_move(Square('b', 6), board))

    def test_queen_possible_move_like_rook(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        self.assertEqual(True, board[('d', 4)].can_move(Square('b', 4), board))

    def test_queen_impossible_move_like_bishop(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 6), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 4)].can_move(Square('h', 8), board))

    def test_queen_impossible_move_like_rook(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('d', 2), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 4)].can_move(Square('d', 1), board))

    def test_queen_move_to_occupied_like_rook(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('d', 2), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 4)].can_move(Square('d', 2), board))

    def test_queen_move_to_occupied_like_bishop(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 6), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('d', 4)].can_move(Square('f', 6), board))

    def test_queen_capture_like_rook(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('d', 2), Color.BLACK)
        board.add_piece(pawn)
        self.assertEqual(True, board[('d', 4)].can_capture(Square('d', 2), board))
        self.assertEqual(False, board[('d', 4)].can_move(Square('d', 2), board))

    def test_queen_capture_like_bishop(self):
        board = BoardState()
        queen = PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE)
        board.add_piece(queen)
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 6), Color.BLACK)
        board.add_piece(pawn)
        self.assertEqual(True, board[('d', 4)].can_capture(Square('f', 6), board))
        self.assertEqual(False, board[('d', 4)].can_move(Square('f', 6), board))

    def test_pawn_possible_move_f2_f3(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 2), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(True, board[('f', 2)].can_move(Square('f', 3), board))

    def test_pawn_possible_move_f2_f4(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 2), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(True, board[('f', 2)].can_move(Square('f', 4), board))

    def test_pawn_possible_move_f5_f6(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 5), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(True, board[('f', 5)].can_move(Square('f', 6), board))

    def test_pawn_impossible_move_f5_f7(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 5), Color.WHITE)
        board.add_piece(pawn)
        self.assertEqual(False, board[('f', 5)].can_move(Square('f', 7), board))

    def test_pawn_impossible_move_f5_f6(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 5), Color.WHITE)
        board.add_piece(pawn)
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('f', 6), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(False, board[('f', 5)].can_move(Square('f', 6), board))

    def test_pawn_impossible_move_f2_f4(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 2), Color.WHITE)
        board.add_piece(pawn)
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('f', 3), Color.WHITE)
        board.add_piece(knight)
        self.assertEqual(False, board[('f', 2)].can_move(Square('f', 4), board))

    def test_pawn_capture(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 2), Color.WHITE)
        board.add_piece(pawn)
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('e', 3), Color.BLACK)
        board.add_piece(knight)
        self.assertEqual(False, board[('f', 2)].can_move(Square('e', 3), board))
        self.assertEqual(True, board[('f', 2)].can_capture(Square('e', 3), board))

    def test_pawn_impossible_capture(self):
        board = BoardState()
        pawn = PieceCreator().create_piece(PieceType.PAWN, Square('f', 2), Color.WHITE)
        board.add_piece(pawn)
        knight = PieceCreator().create_piece(PieceType.KNIGHT, Square('f', 3), Color.BLACK)
        board.add_piece(knight)
        self.assertEqual(False, board[('f', 2)].can_capture(Square('f', 3), board))


    def test_kingside_castling_possible(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('e', 1), Color.WHITE)
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('h', 1), Color.WHITE)
        board.add_piece(king)
        board.add_piece(rook)
        self.assertEqual(True, board.can_kingside_castling())

    def test_kingside_castling_move(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.KING, Square('e', 8), Color.BLACK))
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('h', 8), Color.BLACK))
        board = board.next(MoveParser().parse("O-O", Color.BLACK))
        self.assertEqual(PieceType.KING, board[('g', 8)].type)

    def test_queenside_castling_impossible(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('e', 8), Color.BLACK)
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('a', 7), Color.BLACK)
        board.add_piece(king)
        board.add_piece(rook)
        self.assertRaises(ImpossibleMoveException, board.next, MoveParser().parse("O-O-O", Color.BLACK))

    def test_queenside_castling_move(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('e', 8), Color.BLACK)
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('a', 8), Color.BLACK)
        board.add_piece(king)
        board.add_piece(rook)
        board = board.next(MoveParser().parse("O-O-O", Color.BLACK))
        self.assertEqual(PieceType.KING, board[('c', 8)].type)

    def test_queenside_castling(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('e', 1), Color.WHITE)
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('a', 1), Color.WHITE)
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('d', 3), Color.WHITE))
        board.add_piece(king)
        board.add_piece(rook)
        self.assertEqual(True, board.can_queenside_castling())

    def test_impossible_queenside_castling(self):
        board = BoardState()
        king = PieceCreator().create_piece(PieceType.KING, Square('e', 1), Color.WHITE)
        rook = PieceCreator().create_piece(PieceType.ROOK, Square('a', 1), Color.WHITE)
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('d', 2), Color.BLACK))
        board.add_piece(king)
        board.add_piece(rook)
        self.assertEqual(False, board.can_queenside_castling())

    def test_impossible_kingside_castling(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.KING, Square('e', 1), Color.WHITE))
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('h', 1), Color.WHITE))
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('f', 4), Color.BLACK))
        self.assertEqual(False, board.can_kingside_castling())

    def test_impossible_kingside_castling2(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.KING, Square('e', 1), Color.WHITE))
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('h', 1), Color.WHITE))
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('f', 1), Color.WHITE))
        self.assertEqual(False, board.can_kingside_castling())

    def test_en_passant_capture_possible(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('b', 7), Color.BLACK))
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('a', 5), Color.WHITE))
        board.active_color = Color.WHITE
        board = board.next(MoveParser().parse("b5", Color.BLACK))
        self.assertEqual(True, board[('a', 5)].can_capture(Square('b', 6), board))

    def test_en_passant_capture_move(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('b', 7), Color.BLACK))
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('a', 5), Color.WHITE))
        board.active_color = Color.WHITE
        board = board.next(MoveParser().parse("b5", Color.BLACK))
        board = board.next(MoveParser().parse("b6", Color.WHITE))
        self.assertEqual(None, board[('b', 5)])
        self.assertEqual(Color.WHITE, board[('b', 6)].color)

    def test_no_en_passant_capture(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('b', 7), Color.BLACK))
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('a', 4), Color.WHITE))
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('d', 7), Color.BLACK))
        board.active_color = Color.WHITE
        board = board.next(MoveParser().parse("b5", Color.BLACK))
        board = board.next(MoveParser().parse("a5", Color.WHITE))
        board = board.next(MoveParser().parse("d6", Color.BLACK))
        self.assertEqual(False, board[('a', 5)].can_capture(Square('b', 6), board))

    def test_promotion_move(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('b', 7), Color.WHITE))
        board.active_color = Color.BLACK
        board = board.next(MoveParser().parse("b8=Q", Color.WHITE))
        self.assertEqual(PieceType.QUEEN, board[('b', 8)].type)

    def test_queen_capture(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.QUEEN, Square('d', 4), Color.WHITE))
        board.add_piece(PieceCreator().create_piece(PieceType.PAWN, Square('f', 6), Color.BLACK))
        board.active_color = Color.BLACK
        board = board.next(MoveParser().parse('Qxf6', Color.WHITE))
        self.assertEqual(None, board[('d', 4)])
        self.assertEqual(PieceType.QUEEN, board[('f', 6)].type)

    def test_serialize_empty_board(self):
        board = BoardState()
        two_empty_rows_blob = ((((((((((((((14*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14
        blob = board.serialize()
        self.assertEqual([two_empty_rows_blob]*4, blob)

    def test_serialize_initial_setup(self):
        board = BoardState()
        board.make_initial_setup()
        blob = board.serialize()
        white_rows_blob = ((((((((((((((0*16+1)*16+2)*16+3)*16+4)*16+2)*16+1)*16+0)*16+5)*16+5)*16+5)*16+5)*16+5)*16+5)*16+5)*16+5
        black_rows_blob = (((((((((((((((5+8)*16+5+8)*16+5+8)*16+5+8)*16+5+8)*16+5+8)*16+5+8)*16+5+8)*16+0+8)*16+1+8)*16+2+8)*16+3+8)*16+4+8)*16+2+8)*16+1+8)*16+0+8
        two_empty_rows_blob = ((((((((((((((14*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14)*16+14
        self.assertEqual([white_rows_blob, two_empty_rows_blob, two_empty_rows_blob, black_rows_blob], blob)

    def test_no_pieces_to_move(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.BLACK))
        self.assertRaises(ImpossibleMoveException, board.next, MoveParser().parse('b7', Color.BLACK))

    def test_many_pieces_to_move(self):
        board = BoardState()
        board.add_piece(PieceCreator().create_piece(PieceType.ROOK, Square('d', 5), Color.BLACK))
        board.add_piece(PieceCreator().create_piece(PieceType.BISHOP, Square('f', 7), Color.BLACK))
        self.assertRaises(ImpossibleMoveException, board.next, Move('h5', Color.BLACK))

    def test_exception_during_game_simulation(self):
        game = Game()
        game.moves.append(MoveParser().parse('c5'))
        self.assertRaises(InvalidGameException, game.simulate)

if __name__ == '__main__':
    unittest.main()
