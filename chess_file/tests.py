import unittest
import os
from chess_file.chess_file import  ChessFile

class ChessFileTests(unittest.TestCase):

    def getGameHeader(self):
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

    def getGameBody(self):
        return "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Bc5 6.O-O d6 7.d4 exd4 8.cxd4 Bb6\n" + \
                "9.Nc3 Na5 10.Bd3 Ne7 11.e5 dxe5 12.dxe5 O-O 13.Qc2 h6 14.Ba3 c5 15.Rad1 Bd7\n" + \
                "16.e6 fxe6 17.Bh7+ Kh8 18.Ne5 Nd5 19.Nxd5 exd5 20.Rxd5 Bf5 21.Rxd8 Bxc2 22.Rxf8+ Rxf8\n" + \
                "23.Bxc2  1-0"

    def create_file(self, filename, content):
        file = open(filename, "w")
        file.write(content)

    def setUp(self):
        self.path = os.path.dirname(__file__)

    def test_no_file(self):
        self.assertRaises(IOError, ChessFile, "no_file")

    def test_empty_file(self):
        filename = os.path.join(self.path, "test_files/empty.pgn")
        self.create_file(filename, "")
        test_file = ChessFile(filename)
        self.assertRaises(StopIteration, test_file.next)

    def test_one_game_file(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        self.create_file(filename, self.getGameHeader() + "\n" + self.getGameBody())
        test_file = ChessFile(filename)
        test_file.next()
        self.assertRaises(StopIteration, test_file.next)

    def test_two_games_file(self):
        filename = os.path.join(self.path, "test_files/two_games.pgn")
        self.create_file(filename, self.getGameHeader() + "\n" + self.getGameBody() + "\n\n" + self.getGameHeader() + "\n" + self.getGameBody())
        test_file = ChessFile(filename)
        test_file.next()
        test_file.next()
        self.assertRaises(StopIteration, test_file.next)

    def test_tags_parsing(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        self.create_file(filename, self.getGameHeader() + "\n" + self.getGameBody())
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual(game.tags, {
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

    def test_shallow_move_parsing(self):
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        self.create_file(filename, self.getGameHeader() + "\n" + self.getGameBody())
        test_file = ChessFile(filename)
        game = test_file.next()
        self.assertEqual(45, len(game.moves))

if __name__ == '__main__':
    unittest.main()
