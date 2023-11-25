import chess
import random
from chess import Square, Piece

bishop_weight_labels = [
    "Bishop Material Weight",
]
bishop_weight_bounds = [
    # Material
    (0, 1000), # how much the bishop is worth
]

class BishopEvaluator:
    def __init__(self, board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0, 0] for _ in range(len(bishop_weight_bounds))]

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece):
        if piece.piece_type == chess.BISHOP:
            self.material_evaluation(piece)

    def material_evaluation(self, piece):
        if piece.color == chess.WHITE:
            self.scores_for_weights[0][0] += 1
        else:
            self.scores_for_weights[0][1] += 1