import chess
import random
from chess import Square, Piece
import random

knight_weight_labels = [
    "Knight Material Weight",
    "Knight Position Weight"
]
knight_weight_bounds = [
    # Material
    (0, 1000), # how much the knight is worth
    # Position
    (0, 100), # how much the knoght position is worth
]

POSITION_MAPPING = {
    "a1": -50, "b1": -40, "c1": -30, "d1": -30, "e1": -30, "f1": -30, "g1": -40, "h1": -50,
    "a2": -40, "b2": -20, "c2": 0, "d2": 5, "e2": 5, "f2": 0, "g2": -20, "h2": -40,
    "a3": -30, "b3": 0, "c3": 10, "d3": 15, "e3": 15, "f3": 10, "g3": 0, "h3": -30,
    "a4": -30, "b4": 5, "c4": 15, "d4": 20, "e4": 20, "f4": 15, "g4": 5, "h4": -30,
    "a5": -30, "b5": 5, "c5": 15, "d5": 20, "e5": 20, "f5": 15, "g5": 5, "h5": -30,
    "a6": -30, "b6": 0, "c6": 10, "d6": 15, "e6": 15, "f6": 10, "g6": 0, "h6": -30,
    "a7": -40, "b7": -20, "c7": 0, "d7": 5, "e7": 5, "f7": 0, "g7": -20, "h7": -40,
    "a8": -50, "b8": -40, "c8": -30, "d8": -30, "e8": -30, "f8": -30, "g8": -40, "h8": -50,
}

class KnightEvaluator:
    def __init__(self, board: chess.Board, weights):
        self.weights = weights
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(knight_weight_bounds))]

        self.board = board

    def evaluation_for_piece(self, square: chess.Square, piece: chess.Piece):
        self.material_evaluation(piece)

    def material_evaluation(self, piece: chess.Piece):
        if piece.piece_type == chess.KNIGHT:
            if piece.color == chess.WHITE:
                self.scores_for_weights[0][0] += self.weights[0]
            else:
                self.scores_for_weights[0][1] += self.weights[0]
                
    def position_evaluation(self, square: chess.Square, piece: chess.Piece):
        if piece.piece_type == chess.KNIGHT:
            square_name = chess.square_name(square)
            square_value = POSITION_MAPPING[square_name]
            
            if piece.color == chess.WHITE:
                self.scores_for_weights[1][0] += self.weights[1]*square_value
            else:
                self.scores_for_weights[1][1] += self.weights[1]*square_value
