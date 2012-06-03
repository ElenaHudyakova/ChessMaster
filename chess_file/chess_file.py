import re
from chess_exceptions.chess_exceptions import InvalidMoveRecord
from moves_parse import parse_move
from chess_game.game import Game, WHITE, BLACK
from chess_game.move import Move

class ChessFile(object):
    """A Class-wrapper for PGN file which allows iterating through chess games in that file"""
    startTag = "Event"

    def __init__(self, filename):
        self.file = open(filename)
        self.eof = False
        self.startTagLine = None

    def __iter__(self):
        return self

    def _parse_tag(self, line, game):
        line = line.lstrip()
        line = line[1:-1]
        tag_name, tag_value = line.split(" ", 1)
        tag_value = tag_value[1:-1]
        game.tags[tag_name] = tag_value


    def _parse_moves(self, line, game):
        line = line.strip()
        move_number = 0
        for move_pair in re.split("\d+\.", line):
            if move_pair!="":
                move_pair = move_pair.strip()
                for move_str in re.split("\s+", move_pair):
                    move = Move()
                    move.algebraic_notation = move_str
                    if move_number % 2 == 0:
                        move.color = WHITE
                    else:
                        move.color = BLACK
                    move.move_number = move_number/2 + 1
                    game.moves.append(move)
                    move_number += 1
        game.moves.pop()
        for move in game.moves:
            try:
                parse_move(move)
            except InvalidMoveRecord as error:
                raise error


    def _parse_game(self, notation_str, game):
        notation_str = notation_str.replace("\n", " ")
        while "]" in notation_str:
            tag_line = notation_str.split("]", 1)[0] + "]"
            notation_str = notation_str.split("]", 1)[1]
            self._parse_tag(tag_line, game)
        self._parse_moves(notation_str, game)

    def next(self):
        game = Game()
        notation_str = ""

        if self.startTagLine:
            notation_str += self.startTagLine

        line = self.file.readline()
        if self.eof or line == "":
            raise StopIteration

        while 1:
            if line == "":
                self.eof = True
                break
            else:
                if (self.startTag in line) and (self.startTag in notation_str):
                    self.startTagLine = line
                    break
                else:
                    notation_str += line
            line = self.file.readline()

        try:
            self._parse_game(notation_str, game)
            game.simulate()
        except Exception as error:
            print error.message
            raise Exception("Invalid game")

        return game

