import sys
from PyQt4 import QtCore, QtGui
from game.common import Square, PieceType, Color
from game.game_module import BoardState

class BoardScene(QtGui.QGraphicsScene):

    def __init__(self, board_state = None):
        if board_state is None:
            self.board_state = BoardState()
            self.board_state.make_initial_setup()
        else:
            self.board_state = board_state
        super(BoardScene, self).__init__()
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
        font=QtGui.QFont('White Rabbit')
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

                piece = self.board_state[Square(i, j)]
                if not piece is None:
                    piece_img = QtGui.QGraphicsPixmapItem(QtGui.QPixmap(self._get_image_filename(piece)), scene = self)
#                    piece_img = QtGui.QGraphicsPixmapItem(QtGui.QPixmap('img/king_black.png'), scene = self)
                    piece_img.setOffset(40*i, 400 - 40*j - 40)


class MainWindow(QtGui.QWidget):

    SHIFT = 50
    BUTTON_SIZE = 20
    LABEL_DIST = 30
    UP = 350

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def _create_left_block(self):
        self.games_list = QtGui.QListWidget(self)
        self.games_list.resize(350, self.UP - self.SHIFT*1.5)
        self.games_list.move(self.SHIFT, self.SHIFT)

        import_button = QtGui.QPushButton('Import PGN', self)
        import_button.resize(150, self.BUTTON_SIZE)
        import_button.move(self.SHIFT, self.UP)

        export_button = QtGui.QPushButton('Export to PGN', self)
        export_button.resize(150, self.BUTTON_SIZE)
        export_button.move(self.SHIFT + 50 + 150, self.UP)

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

        clear_button = QtGui.QPushButton('Clear', self)
        clear_button.resize(150, self.BUTTON_SIZE)
        clear_button.move(self.SHIFT + 50 + 150, self.UP + 20 + self.LABEL_DIST*5 + 40)

    def _create_central_block(self):
        self.board = BoardScene()
        self.chess_board = QtGui.QGraphicsView(self.board, parent = self)
        self.chess_board.resize(402, 402)
        self.chess_board.move(self.SHIFT + 350 + self.SHIFT, self.SHIFT)

        start_move_button = QtGui.QPushButton('<<', self)
        start_move_button.resize(70, self.BUTTON_SIZE)
        start_move_button.move(self.SHIFT*2 + 350 + 15, self.SHIFT + 400 + 20)

        prev_move_button = QtGui.QPushButton('<', self)
        prev_move_button.resize(70, self.BUTTON_SIZE)
        prev_move_button.move(self.SHIFT*2 + 350 + 15 + 100, self.SHIFT + 400 + 20)

        next_move_button = QtGui.QPushButton('>', self)
        next_move_button.resize(70, self.BUTTON_SIZE)
        next_move_button.move(self.SHIFT*2 + 350 + 15 + 200, self.SHIFT + 400 + 20)

        last_move_button = QtGui.QPushButton('>>', self)
        last_move_button.resize(70, self.BUTTON_SIZE)
        last_move_button.move(self.SHIFT*2 + 350 + 15 + 300, self.SHIFT + 400 + 20)


    def _create_right_block(self):

        self.move_list = QtGui.QListWidget(self)
        self.move_list.resize(100, 300)
        self.move_list.move(self.SHIFT*3 + 350 + 400, self.SHIFT)

        self.event_label = QtGui.QLabel('Event: ', self)
        self.event_label.move(self.SHIFT*3 + 350 + 400 + 100 + 30, self.SHIFT)
        self.site_label = QtGui.QLabel('Site: ', self)
        self.site_label.move(self.SHIFT*3 + 350 + 400 + 100 + 30, self.SHIFT + self.LABEL_DIST*1.5)
        self.date_label = QtGui.QLabel('Date: ', self)
        self.date_label.move(self.SHIFT*3 + 350 + 430 + 100, self.SHIFT + self.LABEL_DIST*3)
        self.white_label = QtGui.QLabel('White: ', self)
        self.white_label.move(self.SHIFT*3 + 350 + 430 + 100, self.SHIFT + self.LABEL_DIST*4.5)
        self.black_label = QtGui.QLabel('Black: ', self)
        self.black_label.move(self.SHIFT*3 + 350 + 430 + 100, self.SHIFT + self.LABEL_DIST*6)
        self.round_label = QtGui.QLabel('Round: ', self)
        self.round_label.move(self.SHIFT*3 + 350 + 430 + 100, self.SHIFT + self.LABEL_DIST*7.5)
        self.result_label = QtGui.QLabel('Result: ', self)
        self.result_label.move(self.SHIFT*3 + 350 + 430 + 100, self.SHIFT + self.LABEL_DIST*9)

        get_statistics_button = QtGui.QPushButton('Get move statistics', self)
        get_statistics_button.resize(240, self.BUTTON_SIZE)
        get_statistics_button.move(self.SHIFT*3 + 350 + 400, self.SHIFT + 320)

        self.statistics_list = QtGui.QListWidget(self)
        self.statistics_list.resize(240, 180)
        self.statistics_list.move(self.SHIFT*3 + 350 + 400, self.SHIFT + 350)


    def initUI(self):

        self._create_left_block()
        self._create_central_block()
        self._create_right_block()

        self.resize(1200, 650)
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