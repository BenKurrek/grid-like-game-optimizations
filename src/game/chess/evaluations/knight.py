import chess
from chess import Square, Piece

weight_labels = [
    "Knight Material Weight",
]
weight_bounds = [
    # Material
    (0, 1000), # how much the knight is worth
]

class KnightEvaluator:
    def __init__(self, board):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]
        # (W, B) scores for each weight
        self.scores_for_weights = [(0, 0) for _ in range(len(weight_bounds))]

    def evaluation_for_piece(self, piece):
        self.material_evaluation(piece)

    def material_evaluation(self, piece):
        if piece.piece_type == chess.KNIGHT:
            if piece.color == chess.WHITE:
                self.scores_for_weights[0][0] += self.weights[0]
            else:
                self.scores_for_weights[0][1] += self.weights[0]