from chess_game.piece import Piece
import chess_game.motion_strategies

def create_piece(type):
    if type == "king":
        return Piece(chess_game.KingMotionStrategy())