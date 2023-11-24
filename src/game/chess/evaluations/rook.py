import chess
from chess import Square, Piece

weight_labels = [
    "Rook Material Weight",
]
weight_bounds = [
    # Material
    (0, 1000), # how much the rook is worth
]

class RookEvaluator:
    def __init__(self):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]
        # (W, B) scores for each weight
        self.scores_for_weights = [(0, 0) for _ in range(len(weight_bounds))]

    def evaluation_for_piece(self, pice):
        self.material_evaluation(piece)

    def material_evaluation(self, piece):
        if piece.piece_type == chess.ROOK:
            if piece.color == chess.WHITE:
                self.scores_for_weights[0][0] += self.weights[0]
            else:
                self.scores_for_weights[0][1] += self.weights[0]