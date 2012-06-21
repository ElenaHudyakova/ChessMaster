import os
from game.game_module import Game
from parsing.parsing_module import ChessFile
from storage.storage_module import Storage

__author__ = 'Lena'

import unittest

class MyTestCase(unittest.TestCase):

    path = os.path.dirname(__file__)

    def test_save_empty_game(self):
        storage = Storage()
        game = Game()
        storage.save_game(game)
        id = game.id
        game1 = storage.read_game(id)
        self.assertEqual(game1, game)

    def test_regular_game(self):
        storage = Storage()
        filename = os.path.join(self.path, "test_files/one_game.pgn")
        chess_file = ChessFile(filename)
        game = chess_file.next()
        game.simulate()
        storage.save_game(game)
        id = game.id
        game1 = storage.read_game(id)
        self.assertEqual(game1.moves[0].serial0, game.moves[0].serial0)
        self.assertEqual(game1, game)

    def test_read_all_games(self):
        storage = Storage()
        game_number1 = len(storage.read_all_games())
        game = Game()
        id = storage.save_game(game)
        game_number2 = len(storage.read_all_games())
        self.assertEqual(game_number1 + 1, game_number2)


if __name__ == '__main__':
    unittest.main()
