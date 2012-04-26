from chess_game.game import *
from chess_game.piece import Piece
import chess_game.motion_strategies

def create_piece(type, point, color):
    motion_strategy = chess_game.motion_strategies.PawnMotionStrategy()
    if type == KING:
            motion_strategy = chess_game.motion_strategies.KingMotionStrategy()
    if type == KNIGHT:
        motion_strategy = chess_game.motion_strategies.KnightMotionStrategy()
    if type == ROOK:
        motion_strategy = chess_game.motion_strategies.PawnMotionStrategy()
    if type == BISHOP:
        motion_strategy = chess_game.motion_strategies.BishopMotionStrategy()
    if type == QUEEN:
        motion_strategy = chess_game.motion_strategies.PawnMotionStrategy()
    piece = Piece(motion_strategy, point, color)
    piece.type = type
    return piece

