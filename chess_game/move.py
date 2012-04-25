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
        self.is_king_castling = None
        self.is_queen_castling = None
