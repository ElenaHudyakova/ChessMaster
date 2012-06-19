import random
import sys
from PyQt4 import QtCore, QtGui
import math
from game.common import Square, PieceType, Color
from game.game_exceptions import InvalidSquareCoordException
from game.game_module import BoardState, Game
from parsing.parsing_module import ChessFile
from storage.storage_module import Storage


class GameItem(QtGui.QListWidgetItem):

    def __init__(self, game):
        self.content = game
        super(GameItem, self).__init__()
        if game is None:
            self.setText('No game')
        else:
            self.setText(str(game))

class MoveItem(QtGui.QListWidgetItem):

    def __init__(self, move):
        self.content = move
        super(MoveItem, self).__init__()
        if move is None:
            self.setText('No move')
        else:
            self.setText(str(move))

class BoardScene(QtGui.QGraphicsScene):

    def __init__(self, board_state = None):
        if board_state is None:
            self.board_state = BoardState()
            self.board_state.make_initial_setup()
        else:
            self.board_state = board_state
        super(BoardScene, self).__init__()
        self.piece_images = []
        self.painted_squares = []
        self.path = []
        self.initUI()

    def _get_image_filename(self, piece):
        if piece is None:
            return
        filename = 'img/'
        if piece.type == PieceType.BISHOP:
            filename += 'bishop'
        if piece.type == PieceType.KING:
            filename += 'king'
        if piece.type == PieceType.KNIGHT:
            filename += 'knight'
        if piece.type == PieceType.PAWN:
            filename += 'pawn'
        if piece.type == PieceType.QUEEN:
            filename += 'queen'
        if piece.type == PieceType.ROOK:
            filename += 'rook'
        filename+= '_'
        if piece.color == Color.WHITE:
            filename += 'white'
        else:
            filename += 'black'
        filename += '.png'
        return filename


    def initUI(self):
        self.setSceneRect(0,0, 400, 400)
        font=QtGui.QFont()
        font.setPointSize(15)

        black_brush = QtGui.QBrush(QtGui.QColor(50, 125, 215), QtCore.Qt.SolidPattern)
        white_brush = QtGui.QBrush(QtGui.QColor(255, 240, 225), QtCore.Qt.SolidPattern)

        squares = list()
        for i in range(1,9):
            row = list()
            squares.append(row)

        for i in range(1,9):
            file=QtGui.QGraphicsTextItem(Square.digit_to_file(i))
            file.setPos(40*i + 13 , 370)
            file.setFont(font)
            self.addItem(file)

            file=QtGui.QGraphicsTextItem(Square.digit_to_file(i))
            file.setPos(40*i + 13 , 8)
            file.setFont(font)
            self.addItem(file)

            rank=QtGui.QGraphicsTextItem(str(9-i))
            rank.setPos(10, 40*i + 11)
            rank.setFont(font)
            self.addItem(rank)

            rank=QtGui.QGraphicsTextItem(str(9-i))
            rank.setPos(372, 40*i + 11)
            rank.setFont(font)
            self.addItem(rank)

        for i in range(1,9):
            for j in range(1,9):
                squares[i-1].append(QtGui.QGraphicsRectItem(40*i, 400 - 40*j - 40, 40, 40, scene = self))
                if (i+j)%2 == 0:
                    squares[i-1][j-1].setBrush(black_brush)
                else:
                    squares[i-1][j-1].setBrush(white_brush)
                squares[i-1][j-1].setZValue(1.0)

                piece = self.board_state[Square(i, j)]
                if not piece is None:
                    piece_img = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self._get_image_filename(piece)), scene = self)
                    piece_img.setOffset(40*i, 400 - 40*j - 40)
                    piece_img.setZValue(2.0)
                    self.piece_images.append(piece_img)

    def _remove_path(self):
        for line in self.path:
            self.removeItem(line)
        self.path = []

    def mouseDoubleClickEvent(self, event):
        x = event.lastScenePos().x()
        y = event.lastScenePos().y()
        file = math.floor(x/40)
        rank = 9 - math.floor(y/40)
        try:
            self._remove_path()
            self._show_path(Square(int(file), int(rank)))
        except InvalidSquareCoordException as err:
            pass


    def _show_path(self, square):
        if self.board_state[square] is None:
            return
        selected_piece = self.board_state[square]
        pen = QtGui.QPen(QtGui.QColor(150, 50, 50))
        pen.setWidth(3)

        point_pen = QtGui.QPen(QtGui.QColor(150, 50, 50))
        point_pen.setWidth(10)
        point_pen.setCapStyle(QtCore.Qt.RoundCap)

        x1 = selected_piece.path[0].file * 40 + 20
        y1 = (9 - selected_piece.path[0].rank) * 40 + 20

        line = QtGui.QGraphicsLineItem(x1-0.7, y1-0.7, x1+0.7, y1+0.7, scene = self)
        line.setPen(point_pen)
        line.setZValue(3.5)
        self.path.append(line)

        for point in selected_piece.path[1:]:
            x2 = point.file * 40 + 20
            y2 = (9 - point.rank) * 40 + 20

            line = QtGui.QGraphicsLineItem(x2-0.7, y2-0.7, x2+0.7, y2+0.7, scene = self)
            line.setPen(point_pen)
            line.setZValue(3.5)
            self.path.append(line)

            line = QtGui.QGraphicsLineItem(x1, y1, x2, y2, scene = self)
            line.setPen(pen)
            line.setZValue(3.5)
            self.path.append(line)

            x1 = x2
            y1 = y2

    def redraw(self, board_state):
        self.board_state = board_state
        for item in self.piece_images:
            self.removeItem(item)
        self._remove_path()

        self.piece_images = []
        board_state.pieces.reverse()
        for piece in board_state.pieces:
            piece_img = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self._get_image_filename(piece)), scene = self)
            piece_img.setOffset(40*piece.square.file, 400 - 40*piece.square.rank - 40)
            piece_img.setZValue(2.0)
            self.piece_images.append(piece_img)

        self._draw_move()

    def _draw_move(self):
        for item in self.painted_squares:
            self.removeItem(item)
        self.painted_squares = []

        from_pen = QtGui.QPen(QtGui.QColor(255, 250, 50))
        to_pen = QtGui.QPen(QtGui.QColor(50, 255, 50))
        from_pen.setWidth(3)
        to_pen.setWidth(3)

        for piece in self.board_state.moving_pieces:
            to_square = piece.square
            self.painted_squares.append(QtGui.QGraphicsRectItem(40*to_square.file, 400 - 40*to_square.rank - 40, 40, 40, scene = self))
            self.painted_squares[-1].setPen(to_pen)
            self.painted_squares[-1].setZValue(2.5)

            from_square = piece.get_prev_square()
            self.painted_squares.append(QtGui.QGraphicsRectItem(40*from_square.file, 400 - 40*from_square.rank - 40, 40, 40, scene = self))
            self.painted_squares[-1].setPen(from_pen)
            self.painted_squares[-1].setZValue(1.5)


class MainWindow(QtGui.QWidget):

    SHIFT = 50
    BUTTON_SIZE = 20
    LABEL_DIST = 30
    UP = 350

    def __init__(self):
        self.current_game = None
        self.current_move_num = None
        super(MainWindow, self).__init__()
        try:
            self.storage = Storage()
        except :
            pass
        self.initUI()

    def _display_games(self, games):
        self.games_list.clear()
        for game in games:
            self.games_list.addItem(GameItem(game))

    def _show_all_games(self):
        games = self.storage.read_all_games(True)
        self._display_games(games)

    def _import_games(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
        if not filename:
            return
        imported_games_num = 0
        invalid_games_num = 0
        try:
            chess_file = ChessFile(filename)
            while 1:
                try:
                    game = chess_file.next()
                    if not self.import_check_box.isChecked():
                        game.simulate()
                    self.storage.save_game(game)
                    imported_games_num += 1
                except StopIteration:
                    break
                except Exception as err:
                    invalid_games_num += 1
        except :
            self.import_info_label.setText('Mistake in opening a file')


        self.import_info_label.setText('%d games were imported, %d games caused mistakes ' % (imported_games_num, invalid_games_num))
        self.import_info_label.move(self.SHIFT*2 + 350, 500)

        self._show_all_games()

    def _export_games(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Export file')
        if not filename:
            return
        exported_games_num = 0
        invalid_games_num = 0
        try:
            chess_file = ChessFile(filename)
            for game_item in self.games_list.selectedItems():
                try:
                    chess_file.add_game(game_item.content)
                    exported_games_num += 1
                except StopIteration:
                    break
                except Exception as err:
                    invalid_games_num += 1
        except :
            pass

        self.import_info_label.setText('%d games were exported, %d games caused mistakes ' % (exported_games_num, invalid_games_num))
        self.import_info_label.move(self.SHIFT*2 + 350, 500)


    def _show_game(self):
        self.current_game = self.games_list.currentItem().content
        self.current_game = self.storage.read_game(self.current_game.id)
        self.current_move_num  = -1
        try:
            self.current_game.simulate()
        except :
            pass
        self.event_label.setText('Event: \n%s' % self.current_game.event)
        self.site_label.setText('Site: \n%s' % self.current_game.site)
        self.date_label.setText('Date: \n%s' % self.current_game.date)
        self.white_label.setText('White: \n%s' % self.current_game.white)
        self.black_label.setText('Black: \n%s' % self.current_game.black)
        self.result_label.setText('Result: \n%s' % self.current_game.result)
        self.round_label.setText('Round: \n%s' % self.current_game.round)

        self.move_list.clear()
        self.move_list.addItem('')
        for move in self.current_game.moves:
            self.move_list.addItem(MoveItem(move))

        self._show_first_move()

    def _show_move(self):
        if not self.current_game is None:
            self.current_move_num = self.move_list.currentRow()
            self.board.redraw(self.current_game.board_states[self.current_move_num])

    def _show_first_move(self):
        if not self.current_game is None:
            self.current_move_num = 0
            self.move_list.setCurrentRow(self.current_move_num)

    def _show_last_move(self):
        if not self.current_game is None:
            self.current_move_num = len(self.current_game.moves)
            self.move_list.setCurrentRow(self.current_move_num)

    def _show_next_move(self):
        if not self.current_game is None:
            if self.current_move_num < len(self.current_game.moves):
                self.current_move_num += 1
                self.move_list.setCurrentRow(self.current_move_num)

    def _show_prev_move(self):
        if not self.current_game is None:
            if self.current_move_num > 0:
                self.current_move_num -= 1
                self.move_list.setCurrentRow(self.current_move_num)

    def _search_games(self):
        event = self.event_search_edit.text()
        site = self.site_search_edit.text()
        date = self.date_search_edit.text()
        white = self.white_search_edit.text()
        black = self.black_search_edit.text()
        games = self.storage.read_games(event, site, date, white, black)
        self._display_games(games)


    def _create_left_block(self):
        self.games_list = QtGui.QListWidget(self)
        self.games_list.resize(350, self.UP - self.SHIFT*1.5)
        self.games_list.move(self.SHIFT, self.SHIFT)
        self.games_list.doubleClicked.connect(self._show_game)
        self.games_list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        import_button = QtGui.QPushButton('Import PGN', self)
        import_button.resize(150, self.BUTTON_SIZE)
        import_button.move(self.SHIFT, self.UP - 10)
        import_button.clicked.connect(self._import_games)

        export_button = QtGui.QPushButton('Export to PGN', self)
        export_button.resize(150, self.BUTTON_SIZE)
        export_button.move(self.SHIFT + 50 + 150, self.UP - 10)
        export_button.clicked.connect(self._export_games)

        self.import_check_box = QtGui.QCheckBox('Quick import', self)
        self.import_check_box.move(self.SHIFT, self.UP + 17)
        self.import_check_box.setChecked(True)

        event_search_label = QtGui.QLabel('Event ', self)
        event_search_label.move(self.SHIFT, self.UP + 20 + self.LABEL_DIST)
        site_search_label = QtGui.QLabel('Site ', self)
        site_search_label.move(self.SHIFT, self.UP + 20 + self.LABEL_DIST*2)
        date_search_label = QtGui.QLabel('Date ', self)
        date_search_label.move(self.SHIFT, self.UP + 20 + self.LABEL_DIST*3)
        white_search_label = QtGui.QLabel('White ', self)
        white_search_label.move(self.SHIFT, self.UP + 20 + self.LABEL_DIST*4)
        black_search_label = QtGui.QLabel('Black ', self)
        black_search_label.move(self.SHIFT, self.UP + 20 + self.LABEL_DIST*5)

        self.event_search_edit = QtGui.QLineEdit('', self)
        self.event_search_edit.resize(300, self.BUTTON_SIZE)
        self.event_search_edit.move(self.SHIFT + 50, self.UP + 20 + self.LABEL_DIST)

        self.site_search_edit = QtGui.QLineEdit('', self)
        self.site_search_edit.resize(300, self.BUTTON_SIZE)
        self.site_search_edit.move(self.SHIFT + 50, self.UP + 20 + self.LABEL_DIST*2)

        self.date_search_edit = QtGui.QLineEdit('', self)
        self.date_search_edit.resize(300, self.BUTTON_SIZE)
        self.date_search_edit.move(self.SHIFT + 50, self.UP + 20 + self.LABEL_DIST*3)

        self.white_search_edit = QtGui.QLineEdit('', self)
        self.white_search_edit.resize(300, self.BUTTON_SIZE)
        self.white_search_edit.move(self.SHIFT + 50, self.UP + 20 + self.LABEL_DIST*4)

        self.black_search_edit = QtGui.QLineEdit('', self)
        self.black_search_edit.resize(300, self.BUTTON_SIZE)
        self.black_search_edit.move(self.SHIFT + 50, self.UP + 20 + self.LABEL_DIST*5)


        search_button = QtGui.QPushButton('Search', self)
        search_button.resize(150, self.BUTTON_SIZE)
        search_button.move(self.SHIFT, self.UP + 20 + self.LABEL_DIST*5 + 40)
        search_button.clicked.connect(self._search_games)

        all_games_button = QtGui.QPushButton('Show all games', self)
        all_games_button.resize(150, self.BUTTON_SIZE)
        all_games_button.move(self.SHIFT + 50 + 150, self.UP + 20 + self.LABEL_DIST*5 + 40)
        all_games_button.clicked.connect(self._show_all_games)

    def _create_central_block(self):
        self.board = BoardScene()
        self.chess_board = QtGui.QGraphicsView(self.board, parent = self)
        self.chess_board.resize(402, 402)
        self.chess_board.move(self.SHIFT + 350 + self.SHIFT, self.SHIFT)

        start_move_button = QtGui.QPushButton('<<', self)
        start_move_button.resize(70, self.BUTTON_SIZE)
        start_move_button.move(self.SHIFT*2 + 350 + 15, self.SHIFT + 400 + 20)
        start_move_button.clicked.connect(self._show_first_move)

        prev_move_button = QtGui.QPushButton('<', self)
        prev_move_button.resize(70, self.BUTTON_SIZE)
        prev_move_button.move(self.SHIFT*2 + 350 + 15 + 100, self.SHIFT + 400 + 20)
        prev_move_button.clicked.connect(self._show_prev_move)

        next_move_button = QtGui.QPushButton('>', self)
        next_move_button.resize(70, self.BUTTON_SIZE)
        next_move_button.move(self.SHIFT*2 + 350 + 15 + 200, self.SHIFT + 400 + 20)
        next_move_button.clicked.connect(self._show_next_move)

        last_move_button = QtGui.QPushButton('>>', self)
        last_move_button.resize(70, self.BUTTON_SIZE)
        last_move_button.move(self.SHIFT*2 + 350 + 15 + 300, self.SHIFT + 400 + 20)
        last_move_button.clicked.connect(self._show_last_move)

        self.import_info_label = QtGui.QLabel('No import yet', self)
        self.import_info_label.move(self.SHIFT*2 + 350, 500)
        self.import_info_label.resize(400, 30)


    def _create_right_block(self):

        self.move_list = QtGui.QListWidget(self)
        self.move_list.resize(100, 300)
        self.move_list.move(self.SHIFT*3 + 350 + 400, self.SHIFT)
        self.move_list.currentItemChanged.connect(self._show_move)

        self.event_label = QtGui.QLabel('Event: ', self)
        self.event_label.move(self.SHIFT*3 + 350 + 400 + 100 + 20, self.SHIFT)
        self.event_label.resize(200, 30)

        self.site_label = QtGui.QLabel('Site: ', self)
        self.site_label.move(self.SHIFT*3 + 350 + 400 + 100 + 20, self.SHIFT + self.LABEL_DIST*1.5)
        self.site_label.resize(200, 30)

        self.date_label = QtGui.QLabel('Date: ', self)
        self.date_label.move(self.SHIFT*3 + 350 + 420 + 100, self.SHIFT + self.LABEL_DIST*3)
        self.date_label.resize(200, 30)

        self.white_label = QtGui.QLabel('White: ', self)
        self.white_label.move(self.SHIFT*3 + 350 + 420 + 100, self.SHIFT + self.LABEL_DIST*4.5)
        self.white_label.resize(200, 30)

        self.black_label = QtGui.QLabel('Black: ', self)
        self.black_label.move(self.SHIFT*3 + 350 + 420 + 100, self.SHIFT + self.LABEL_DIST*6)
        self.black_label.resize(200, 30)

        self.round_label = QtGui.QLabel('Round: ', self)
        self.round_label.move(self.SHIFT*3 + 350 + 420 + 100, self.SHIFT + self.LABEL_DIST*7.5)
        self.round_label.resize(200, 30)

        self.result_label = QtGui.QLabel('Result: ', self)
        self.result_label.move(self.SHIFT*3 + 350 + 420 + 100, self.SHIFT + self.LABEL_DIST*9)
        self.result_label.resize(200, 30)

        get_statistics_button = QtGui.QPushButton('Get move statistics', self)
        get_statistics_button.resize(250, self.BUTTON_SIZE)
        get_statistics_button.move(self.SHIFT*3 + 350 + 400, self.SHIFT + 320)

        self.statistics_list = QtGui.QListWidget(self)
        self.statistics_list.resize(250, 180)
        self.statistics_list.move(self.SHIFT*3 + 350 + 400, self.SHIFT + 350)


    def initUI(self):

        self._create_left_block()
        self._create_central_block()
        self._create_right_block()

        self.resize(1220, 650)
        self.center()
        self.setWindowTitle('ChessMaster')
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():

    app = QtGui.QApplication(sys.argv)
    main_window =  MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

def main():

    app = QtGui.QApplication(sys.argv)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()