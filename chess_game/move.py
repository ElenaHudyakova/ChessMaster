from storage.db_classes import MoveDB
from storage.db_connection import session

class Move(object):
    def __init__(self):
        self.move_number = None
        self.color = None
        self.algebraic_notation = None
        self.piece_type = None
        self.to_point = None
        self.from_point = None
        self.is_capture = None
        self.is_check = None
        self.is_promotion = None
        self.promotion_piece_type = None
        self.is_king_castling = None
        self.is_queen_castling = None

    def save(self, game_id, board_state):
        move_db = MoveDB()
        move_db.color = self.color
        move_db.game_id = game_id
        move_db.notation = self.algebraic_notation
        move_db.number = self.move_number
        serial = board_state.serialize()
        move_db.serial0 = serial[0]
        move_db.serial1 = serial[1]
        move_db.serial2 = serial[2]
        move_db.serial3 = serial[3]

        session.add(move_db)
        session.commit()

    def read(self, id):
        pass


