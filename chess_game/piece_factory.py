from chess_game.game import *
from chess_game.piece import Piece
import chess_game.motion_strategies

def _get_motion_strategy(type):
    motion_strategy = chess_game.motion_strategies.PawnMotionStrategy()
    if type == KING:
        motion_strategy = chess_game.motion_strategies.KingMotionStrategy()
    if type == KNIGHT:
        motion_strategy = chess_game.motion_strategies.KnightMotionStrategy()
    if type == ROOK:
        motion_strategy = chess_game.motion_strategies.RookMotionStrategy()
    if type == BISHOP:
        motion_strategy = chess_game.motion_strategies.BishopMotionStrategy()
    if type == QUEEN:
        motion_strategy = chess_game.motion_strategies.QueenMotionStrategy()
    return  motion_strategy

def create_piece(type, point, color):
    piece = Piece(_get_motion_strategy(type), point, color)
    piece.type = type
    return piece

def change_piece_type(piece, type):
    new_piece = Piece(_get_motion_strategy(type), piece.point, piece.color)
    new_piece.type = type
    return new_piece
