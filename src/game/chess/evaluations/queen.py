import chess
import random
from chess import Square, Piece

queen_weight_labels = [
    "Queen Material Weight",
]
queen_weight_bounds = [
    # Material
    (0, 1000), # how much the queen is worth
]

class QueenEvaluator:
    def __init__(self, board, weights):
        self.weights = weights
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(queen_weight_bounds))]
        self.board = board

    def get_score(self):
        white_score = 0
        black_score = 0
        for weight_index, (white_weight, black_weight) in enumerate(self.scores_for_weights):
            white_score += white_weight
            black_score += black_weight

        return (white_score, black_score)

    def evaluation_for_square(self, square, piece):
        if piece.piece_type == chess.QUEEN:
            self.material_evaluation(piece)

    def material_evaluation(self, piece):
        if piece.color == chess.WHITE:
            self.scores_for_weights[0][0] += self.weights[0]
        else:
            self.scores_for_weights[0][1] += self.weights[0]