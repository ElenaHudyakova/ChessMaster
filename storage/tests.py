import unittest
import os
from chess_file.chess_file import  ChessFile
from chess_game.game import Game



class DataBaseTests(unittest.TestCase):

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
        return "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Bc5 6.O-O d6 7.d4 exd4 8.cxd4 Bb6\n" +\
               "9.Nc3 Na5 10.Bd3 Ne7 11.e5 dxe5 12.dxe5 O-O 13.Qc2 h6 14.Ba3 c5 15.Rad1 Bd7\n" +\
               "16.e6 fxe6 17.Bh7+ Kh8 18.Ne5 Nd5 19.Nxd5 exd5 20.Rxd5 Bf5 21.Rxd8 Bxc2 22.Rxf8+ Rxf8\n" +\
               "23.Bxc2  1-0"

    def create_file(self, filename, content):
        file = open(filename, "w")
        file.write(content)


    def test_simple_save_game(self):
        filename = os.path.join(os.path.dirname(__file__), "test_files/one_game.pgn")
        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body())
        test_file = ChessFile(filename)
        game = test_file.next()
        id = game.save()
        self.assertGreater(id, -1)

    def test_save_game_info(self):
        filename = os.path.join(os.path.dirname(__file__), "test_files/one_game.pgn")
        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body())
        test_file = ChessFile(filename)
        game = test_file.next()
        id = game.save()
        new_game = Game()
        new_game.read(id)
        self.assertEqual(new_game.tags["Event"], game.tags["Event"])

