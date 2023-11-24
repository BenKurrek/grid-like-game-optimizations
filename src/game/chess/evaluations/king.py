import chess
from chess import Square, Piece

weight_labels = [
    "King Material Weight",
]
weight_bounds = [
    # Material
    (1, 1), # how much the king is worth
]

class KingEvaluator:
    def __init__(self, board):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]
        # (W, B) scores for each weight
        self.scores_for_weights = [(0, 0) for _ in range(len(weight_bounds))]

    def evaluation_for_piece(self, piece):
        self.material_evaluation(piece)

    def material_evaluation(self, piece):
        if piece.piece_type == chess.KING:
            if piece.color == chess.WHITE:
                self.scores_for_weights[0][0] += self.weights[0]
            else:
                self.scores_for_weights[0][1] += self.weights[0]