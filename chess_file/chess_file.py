from chess_game.game import Game

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
        tag_name = ""
        i = 1
        while line[i] != " ":
            tag_name += line[i]
            i += 1
        tag_value = ""
        i += 2
        while line[i] != "\"":
            tag_value += line[i]
            i += 1
        game.tags[tag_name] = tag_value


    def _parse_moves(self, line, game):
        pass

    def _parseLine(self, line, game):
        if line[0] == "[":
            self._parse_tag(line, game)
        else:
            self._parse_moves(line, game)

    def next(self):
        game = Game()
        if self.startTagLine:
            self._parseLine(self.startTagLine, game)
        line = self.file.readline()
        if self.eof or line == "":
            raise StopIteration
        while 1:
            if line == "":
                self.eof = True
                break
            else:
                if (self.startTag in line) and (game.tags.has_key(self.startTag)):
                    self.startTagLine = line
                    break
                else:
                    self._parseLine(line, game)
            line = self.file.readline()
        return game

