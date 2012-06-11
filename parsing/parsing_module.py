import re
from game.common import Square, PieceType
from game.game_exceptions import InvalidMoveRecordException

class MoveParser(object):
    def parse(self, move):
        is_castling = self._parse_castling_move(move)
        if not is_castling:
            try:
                m = re.match(r"(?P<piece>[BRKQN]?)(?P<from_file>[a-h]?)(?P<from_rank>[1-8]?)(?P<is_capture>x?)(?P<to_file>[a-h])(?P<to_rank>[1-8])(?P<is_promotion>=?)(?P<promotion_piece_type>[BRKQN]?)(?P<is_check>\+?)", move.notation)
                move.piece_type = self._get_piece_type(m.group("piece"))
                move.to_square = Square(m.group("to_file"), int(m.group("to_rank")))
                try:
                    move.from_square = Square(m.group("from_file"), int(m.group("from_rank")))
                except :
                    move.from_square = Square(m.group("from_file"), None)
                move.is_capture = m.group("is_capture") == "x"
                move.is_check = m.group("is_check") == "+"
                move.is_promotion = m.group("is_promotion") == "="
                if move.is_promotion:
                    move.promotion_piece_type = self._get_piece_type(m.group("promotion_piece_type"))
            except Exception as err:
                print err.message
                raise InvalidMoveRecordException(move.notation)
            
    def _parse_castling_move(self, move):
        if move.notation == "O-O":
            move.is_king_castling = True
            return True
        else:
            if move.notation == "O-O-O":
                move.is_queen_castling = True
                return True
        return False

    def _get_piece_type(self, letter):
        return {
            'B': lambda: PieceType.BISHOP,
            'R': lambda: PieceType.ROOK,
            'K': lambda: PieceType.KING,
            'Q': lambda: PieceType.QUEEN,
            'N': lambda: PieceType.KNIGHT,
            '': lambda: PieceType.PAWN,
            }[letter]()

class ChessFile(object):
    """A Class-wrapper for PGN file which allows iterating through chess games in that file"""
    START_TAG = "Event"

    def __init__(self, filename):
        self.file = open(filename)
        self._eof = False
        self._startTagLine = None

    def __iter__(self):
        return self

    def _parse_tag(self, line, game):
        line = line.lstrip()
        line = line[1:-1]
        tag_name, tag_value = line.split(" ", 1)
        tag_value = tag_value[1:-1]
        try:
            setattr(game, tag_name, tag_value)
        except :
            pass


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
                        move.color = Color.WHITE
                    else:
                        move.color = Color.BLACK
                    move.fullmove_number = move_number/2 + 1
                    game.moves.append(move)
                    move_number += 1
        game.moves.pop()


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

        if self._startTagLine:
            notation_str += self._startTagLine

        line = self.file.readline()
        if self._eof or line == "":
            raise StopIteration

        while 1:
            if line == "":
                self._eof = True
                break
            else:
                if (self.START_TAG in line) and (self.START_TAG in notation_str):
                    self._startTagLine = line
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


#
#        def get_game_header(self):
#            return "[Event \"London m5\"]\n"\
#                   "[Site \"London\"]\n"\
#                   "[Date \"1862.??.??\"]\n"\
#                   "[Round \"?\"]\n"\
#                   "[White \"Mackenzie, George Henry\"]\n"\
#                   "[Black \"Paulsen, Louis\"]\n"\
#                   "[Result \"1-0\"]\n"\
#                   "[WhiteElo \"\"]\n"\
#                   "[BlackElo \"\"]\n"\
#                   "[ECO \"C51\"]\n"
#
#    def get_game_body(self):
#        return "1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.b4 Bxb4 5.c3 Bc5 6.O-O d6 7.d4 exd4 8.cxd4 Bb6\n" +\
#               "9.Nc3 Na5 10.Bd3 Ne7 11.e5 dxe5 12.dxe5 O-O 13.Qc2 h6 14.Ba3 c5 15.Rad1 Bd7\n" +\
#               "16.e6 fxe6 17.Bh7+ Kh8 18.Ne5 Nd5 19.Nxd5 exd5 20.Rxd5 Bf5 21.Rxd8 Bxc2 22.Rxf8+ Rxf8\n" +\
#               "23.Bxc2  1-0"
#
#    def get_game_body_promotion(self):
#        return """1. e4 b6 2. d4 Bb7 3. Nc3 e6 4. Nf3 Bb4 5. Bd3 Nf6 6. Bg5 h6 7. Bxf6
#Qxf6 8. O-O Bxc3 9. bxc3 d6 10. Nd2 e5 11. f4 Qe7 12. fxe5 dxe5 13. Bb5+
#c6 14. Bc4 O-O 15. Rf5 Nd7 16. Qh5 b5 17. Bb3 c5 18. dxc5 Nf6 19. Qf3
#Bc8 20. Rxf6 Qxf6 21. Qxf6 gxf6 22. Bd5 Rb8 23. Rf1 Kg7 24. Nb3 Be6
#25. c6 Rbd8 26. Rd1 f5 27. Rd3 fxe4 28. Rg3+ Kf6 29. Bxe4 Bd5 30. c7
#Bxe4 31. cxd8=Q+ Rxd8 32. Rh3 Bxc2 33. Rxh6+ Bg6 34. Rh3 Rd6 35. Re3 Bb1
#36. Re2 Rc6 37. Rb2 Bg6 38. Na5 Rxc3 39. Rxb5 Rc1+ 40. Kf2 Rc2+ 41. Kf3
#Rxa2 42. Nc6 e4+ 43. Kg3 Ra3+ 44. Kf4 e3 45. Rb2 Bd3 46. Ne5 Bf5
#47. Ng4+ Bxg4 48. Kxg4 Ke5 49. Kf3 Kd4 50. Rb7 f5 51. g3 a5 52. Rd7+ Kc5
#53. Re7 Kd4 54. Rd7+ Ke5 55. Re7+ Kd4 1/2-1/2"""
#
#    def get_game_body_en_passant(self):
#        return "1. a4 a6 2. a5 b5 3. b6 1/2-1/2"
#
#
#    def create_file(self, filename, content):
#        file = open(filename, "w")
#        file.write(content)
#
#    def setUp(self):
#        if self.setUpResult is None:
#            self.__class__.setUpResult = 1
#            self.__class__.path = os.path.dirname(__file__)
#            filename = os.path.join(self.path, "test_files/one_game.pgn")
#            self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body())
#            test_file = ChessFile(filename)
#            self.__class__.game = test_file.next()
#
#    def test_no_file(self):
#        self.assertRaises(IOError, ChessFile, "no_file")
#
#    def test_empty_file(self):
#        filename = os.path.join(self.path, "test_files/empty.pgn")
#        self.create_file(filename, "")
#        test_file = ChessFile(filename)
#        self.assertRaises(StopIteration, test_file.next)
#
#    def test_one_game_file(self):
#        filename = os.path.join(self.path, "test_files/one_game.pgn")
#        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body())
#        test_file = ChessFile(filename)
#        test_file.next()
#        self.assertRaises(StopIteration, test_file.next)
#
#    def test_two_games_file(self):
#        filename = os.path.join(self.path, "test_files/two_games.pgn")
#        self.create_file(filename, self.get_game_header() + "\n" + self.get_game_body() + "\n\n" + self.get_game_header() + "\n" + self.get_game_body())
#        test_file = ChessFile(filename)
#        test_file.next()
#        test_file.next()
#        self.assertRaises(StopIteration, test_file.next)
#
#    def test_tags_parsing(self):
#        self.assertEqual(self.game.tags, {
#            "Event": "London m5",
#            "Site": "London",
#            "Date": "1862.??.??",
#            "Round": "?",
#            "White": "Mackenzie, George Henry",
#            "Black": "Paulsen, Louis",
#            "Result": "1-0",
#            "WhiteElo": "",
#            "BlackElo": "",
#            "ECO": "C51"
#        })
#
#    def test_shallow_moves_parsing(self):
#        self.assertEqual(45, len(self.game.moves))