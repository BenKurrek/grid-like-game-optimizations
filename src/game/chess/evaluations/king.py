import chess
import random
from chess import Square, Piece

king_weight_labels = [
    "King Material Weight",
    "King Castle"
]
king_weight_bounds = [
    # Material TODO why is the king bounded at 1?
    (1.0, 1.0), # how much the king is worth
    # Weight of a king being able to castle.
    (0,100),
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class KingEvaluator:
    def __init__(self, board: chess.Board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(king_weight_bounds))]
        self.board = board

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece):
        if piece.piece_type == chess.KING:
            self.material_evaluation(piece)

    def material_evaluation(self, piece):
        material_idx = 0
        if piece.color == chess.WHITE:
            self.scores_for_weights[material_idx][WHITE_SCORE_IDX] += 1
        else:
            self.scores_for_weights[material_idx][BLACK_SCORE_IDX] += 1
    
    def king_castle_evaluation(self, piece: chess.Piece):
        castling_idx = 1
        score_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        count = int(self.board.has_kingside_castling_rights(piece.color)) + int(self.board.has_queenside_castling_rights(piece.color))
        self.scores_for_weights[castling_idx][score_idx] = count