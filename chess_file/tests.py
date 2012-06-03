import unittest
import os
from chess_file.chess_file import  ChessFile
from chess_game.point import Point
from chess_game.game import *

class ChessFileTests(unittest.TestCase):

    setUpResult = None

    def get_game_header(self):
        return "[Event \"London m5\"]\n"\
               "[Site \"London\"]\n"\
               "[Date \"1862.??.??\"]\n"\
               "[Round \"?\"]\n"\
               "[White \"Mackenzie, George Henry\"]\n"\
               "[Black \"Paulsen, Louis\"]\n"\
               "[Result \"1-0\"]\n"\
               "[WhiteElo \"\"]\n"\
               "[BlackElo \"\"]\n"\
               "[ECO \"C51\"]\n"

    def get_game_body(self):
        return "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Bc5 6.O-O d6 7.d4 exd4 8.cxd4 Bb6\n" + \
                "9.Nc3 Na5 10.Bd3 Ne7 11.e5 dxe5 12.dxe5 O-O 13.Qc2 h6 14.Ba3 c5 15.Rad1 Bd7\n" + \
                "16.e6 fxe6 17.Bh7+ Kh8 18.Ne5 Nd5 19.Nxd5 exd5 20.Rxd5 Bf5 21.Rxd8 Bxc2 22.Rxf8+ Rxf8\n" + \
                "23.Bxc2  1-0"

    def get_game_body_promotion(self):
        return """1. e4 b6 2. d4 Bb7 3. Nc3 e6 4. Nf3 Bb4 5. Bd3 Nf6 6. Bg5 h6 7. Bxf6
Qxf6 8. O-O Bxc3 9. bxc3 d6 10. Nd2 e5 11. f4 Qe7 12. fxe5 dxe5 13. Bb5+
c6 14. Bc4 O-O 15. Rf5 Nd7 16. Qh5 b5 17. Bb3 c5 18. dxc5 Nf6 19. Qf3
Bc8 20. Rxf6 Qxf6 21. Qxf6 gxf6 22. Bd5 Rb8 23. Rf1 Kg7 24. Nb3 Be6
25. c6 Rbd8 26. Rd1 f5 27. Rd3 fxe4 28. Rg3+ Kf6 29. Bxe4 Bd5 30. c7
Bxe4 31. cxd8=Q+ Rxd8 32. Rh3 Bxc2 33. Rxh6+ Bg6 34. Rh3 Rd6 35. Re3 Bb1
36. Re2 Rc6 37. Rb2 Bg6 38. Na5 Rxc3 39. Rxb5 Rc1+ 40. Kf2 Rc2+ 41. Kf3
Rxa2 42. Nc6 e4+ 43. Kg3 Ra3+ 44. Kf4 e3 45. Rb2 Bd3 46. Ne5 Bf5
47. Ng4+ Bxg4 48. Kxg4 Ke5 49. Kf3 Kd4 50. Rb7 f5 51. g3 a5 52. Rd7+ Kc5
53. Re7 Kd4 54. Rd7+ Ke5 55. Re7+ Kd4 1/2-1/2"""

    def get_game_body_en_passant(self):
        return "1. a4 a6 2. a5 b5 3. b6 1/2-1/2"


    def create_file(self, filename, content):
        file = open(filename, "w")
        file.write(content)

    def setUp(self):
        if self.setUpResult is None:
            self.__class__.setUpResult = 1
            self.__class__.path = os.path.dirname(__file__)
            filename = os.path.join(self.path, "test_files/one_game.pgn")
            self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body())
            test_file = ChessFile(filename)
            self.__class__.game = test_file.next()

    def test_no_file(self):
        self.assertRaises(IOError, ChessFile, "no_file")

    def test_empty_file(self):
        filename = os.path.join(self.path, "test_files/empty.pgn")
        self.create_file(filename, "")
        test_file = ChessFile(filename)
        self.assertRaises(StopIteration, test_file.next)

    def test_one_game_file(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body())
        test_file = ChessFile(filename)
        test_file.next()
        self.assertRaises(StopIteration, test_file.next)

    def test_two_games_file(self):
        filename = os.path.join(self.path, "test_files/two_games.pgn")
        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body() + "\n\n" + self.get_game_header() + "\n" + self.get_game_body())
        test_file = ChessFile(filename)
        test_file.next()
        test_file.next()
        self.assertRaises(StopIteration, test_file.next)

    def test_tags_parsing(self):
        self.assertEqual(self.game.tags, {
            "Event": "London m5",
            "Site": "London",
            "Date": "1862.??.??",
            "Round": "?",
            "White": "Mackenzie, George Henry",
            "Black": "Paulsen, Louis",
            "Result": "1-0",
            "WhiteElo": "",
            "BlackElo": "",
            "ECO": "C51"
            })

    def test_shallow_moves_parsing(self):
        self.assertEqual(45, len(self.game.moves))

    def test_mid_moves_parsing(self):
        self.assertEqual(23, self.game.moves[44].move_number)
        self.assertEqual(WHITE, self.game.moves[44].color)
        self.assertEqual("Bxc2", self.game.moves[44].algebraic_notation)

    def test_deep_moves_parsing_Bxc2(self):
        self.assertEqual(BISHOP, self.game.moves[44].piece_type)#Bxc2
        self.assertEqual(Point("c", 2), self.game.moves[44].to_point)
        self.assertEqual(Point(), self.game.moves[44].from_point)
        self.assertEqual(True, self.game.moves[44].is_capture)

    def test_deep_moves_parsing_exd5(self):
        self.assertEqual(PAWN, self.game.moves[37].piece_type)#exd5
        self.assertEqual(Point("d", 5), self.game.moves[37].to_point)
        self.assertEqual(Point("e", None), self.game.moves[37].from_point)
        self.assertEqual(True, self.game.moves[37].is_capture)

    def test_deep_moves_parsing_e4(self):
        self.assertEqual(PAWN, self.game.moves[0].piece_type)#e4
        self.assertEqual(Point("e", 4), self.game.moves[0].to_point)
        self.assertEqual(Point(), self.game.moves[0].from_point)
        self.assertEqual(False, self.game.moves[0].is_capture)

    def test_deep_moves_parsing_Rad1(self):
        self.assertEqual(ROOK, self.game.moves[28].piece_type)#Rad1
        self.assertEqual(Point("d", 1), self.game.moves[28].to_point)
        self.assertEqual(Point("a", None), self.game.moves[28].from_point)
        self.assertEqual(False, self.game.moves[28].is_capture)

    def test_deep_moves_parsing_O_O(self):
        self.assertEqual(True, self.game.moves[10].is_king_castling)
        self.assertEqual(None, self.game.moves[10].piece_type)#O-O

    def test_deep_moves_parsing_Bh7_check(self):
        self.assertEqual(True, self.game.moves[32].is_check)


    def test_game_simulation_e4(self):
        self.assertEqual(PAWN, self.game.board_positions[0][("e", 2)].type)
        self.assertEqual(PAWN, self.game.board_positions[1][("e", 4)].type)
        self.assertEqual(None, self.game.board_positions[1][("e", 2)])

    def test_game_simulation_e5(self):
        self.assertEqual(PAWN, self.game.board_positions[1][("e", 7)].type)
        self.assertEqual(PAWN, self.game.board_positions[2][("e", 5)].type)
        self.assertEqual(None, self.game.board_positions[2][("e", 7)])

    def test_game_simulation_Nf3(self):
        self.assertEqual(KNIGHT, self.game.board_positions[2][("g", 1)].type)
        self.assertEqual(KNIGHT, self.game.board_positions[3][("f", 3)].type)
        self.assertEqual(None, self.game.board_positions[3][("g", 1)])

    def test_game_simulation_Nc6(self):
        self.assertEqual(KNIGHT, self.game.board_positions[3][("b", 8)].type)
        self.assertEqual(KNIGHT, self.game.board_positions[4][("c", 6)].type)
        self.assertEqual(None, self.game.board_positions[4][("b", 8)])

    def test_game_simulation_Bc4(self):
        self.assertEqual(BISHOP, self.game.board_positions[4][("f", 1)].type)
        self.assertEqual(BISHOP, self.game.board_positions[5][("c", 4)].type)
        self.assertEqual(None, self.game.board_positions[5][("f", 1)])

    def test_game_simulation_Bc5(self):
        self.assertEqual(BISHOP, self.game.board_positions[5][("f", 8)].type)
        self.assertEqual(BISHOP, self.game.board_positions[6][("c", 5)].type)
        self.assertEqual(None, self.game.board_positions[6][("f", 8)])

    def test_game_simulation_Bxb4(self):
        self.assertEqual(BISHOP, self.game.board_positions[7][("c", 5)].type)
        self.assertNotEqual(None, self.game.board_positions[7][("b", 4)])
        self.assertEqual(BISHOP, self.game.board_positions[8][("b", 4)].type)
        self.assertEqual(None, self.game.board_positions[8][("c", 5)])

    def test_game_simulation_O_O(self):
        self.assertEqual(KING, self.game.board_positions[10][("e", 1)].type)
        self.assertEqual(ROOK, self.game.board_positions[10][("h", 1)].type)
        self.assertEqual(KING, self.game.board_positions[11][("g", 1)].type)
        self.assertEqual(ROOK, self.game.board_positions[11][("f", 1)].type)
        self.assertEqual(None, self.game.board_positions[11][("e", 1)])
        self.assertEqual(None, self.game.board_positions[11][("h", 1)])

    def test_game_simulation_d6(self):
        self.assertEqual(PAWN, self.game.board_positions[11][("d", 7)].type)
        self.assertEqual(PAWN, self.game.board_positions[12][("d", 6)].type)
        self.assertEqual(None, self.game.board_positions[12][("d", 7)])

    def test_game_simulation_exd4(self):
        self.assertEqual(PAWN, self.game.board_positions[13][("e", 5)].type)
        self.assertNotEqual(None, self.game.board_positions[13][("d", 4)])
        self.assertEqual(PAWN, self.game.board_positions[14][("d", 4)].type)
        self.assertEqual(None, self.game.board_positions[14][("e", 5)])

    def test_game_simulation_Qc2(self):
        self.assertEqual(QUEEN, self.game.board_positions[24][("d", 1)].type)
        self.assertEqual(QUEEN, self.game.board_positions[25][("c", 2)].type)
        self.assertEqual(None, self.game.board_positions[25][("d", 1)])

    def test_game_simulation_Rad1(self):
        self.assertEqual(ROOK, self.game.board_positions[28][("a", 1)].type)
        self.assertEqual(ROOK, self.game.board_positions[29][("d", 1)].type)
        self.assertEqual(None, self.game.board_positions[29][("a", 1)])

    def test_game_simulation_Kh8(self):
        self.assertEqual(KING, self.game.board_positions[33][("g", 8)].type)
        self.assertEqual(KING, self.game.board_positions[34][("h", 8)].type)
        self.assertEqual(None, self.game.board_positions[34][("g", 8)])

    def test_game_simulation_Nxd5(self):
        self.assertEqual(KNIGHT, self.game.board_positions[36][("c", 3)].type)
        self.assertNotEqual(None, self.game.board_positions[37][("d", 5)])
        self.assertEqual(KNIGHT, self.game.board_positions[37][("d", 5)].type)
        self.assertEqual(None, self.game.board_positions[37][("c", 3)])

    def test_game_simulation_Rxf8(self):
        self.assertEqual(ROOK, self.game.board_positions[42][("d", 8)].type)
        self.assertNotEqual(None, self.game.board_positions[43][("f", 8)])
        self.assertEqual(ROOK, self.game.board_positions[43][("f", 8)].type)
        self.assertEqual(None, self.game.board_positions[43][("d", 8)])

    def test_game_simulation_promotion(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body_promotion())
        test_file = ChessFile(filename)
        self.game = test_file.next()

        self.assertEqual(PAWN, self.game.board_positions[60][("c", 7)].type)
        self.assertEqual(QUEEN, self.game.board_positions[61][("d", 8)].type)

    def test_game_simulation_en_passant(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body_en_passant())
        test_file = ChessFile(filename)
        self.game = test_file.next()

        self.assertEqual(PAWN, self.game.board_positions[4][("b", 5)].type)
        self.assertEqual(PAWN, self.game.board_positions[4][("a", 5)].type)
        self.assertEqual(PAWN, self.game.board_positions[5][("b", 6)].type)
        self.assertEqual(None, self.game.board_positions[5][("b", 5)])


if __name__ == '__main__':
    unittest.main()
