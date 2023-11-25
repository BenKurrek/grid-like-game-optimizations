# pawn.py

import chess
import random
from chess import Square, Piece

pawn_weight_labels = [
    "Pawn Material Weight",
    "Center Pawn Weight",
    "Pawn Chains Weight",
    "Passed Pawns Weight"
]
pawn_weight_bounds = [
    # Material
    (0, 1000), # how much the pawn is worth
    (0, 1000), # how much pawn islands are worth
    (0, 1000), # how much pawn chains are worth
    (0, 1000), # how much passed pawns are worth
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class PawnEvaluator:
    def __init__(self, board, weights):
        self.weights = weights
        self.board = board
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(pawn_weight_labels))]

        self.pawn_islands = 0
        self.seen_files = set()

    def get_score(self):
        white_score = 0
        black_score = 0
        for weight_index, (white_weight, black_weight) in enumerate(self.scores_for_weights):
            white_score += white_weight
            black_score += black_weight

        return (white_score, black_score)

    def evaluation_for_square(self, square, piece):
        if piece.piece_type == chess.PAWN:
            # If the square is a pawn, give it the material bonus
            self.material_evaluation(piece)

            # If the square is in the center, give it a bonus
            if square in chess.SquareSet(chess.BB_CENTER):
                self.center_pawn_evaluation(piece)

    def material_evaluation(self, piece):
        pawn_material_idx = 0
        if piece.color == chess.WHITE:
            self.scores_for_weights[pawn_material_idx][WHITE_SCORE_IDX] += self.weights[pawn_material_idx]
        else:
            self.scores_for_weights[pawn_material_idx][BLACK_SCORE_IDX] += self.weights[pawn_material_idx]

    def center_pawn_evaluation(self, piece):
        center_pawn_idx = 0
        if piece.color == chess.WHITE:
            self.scores_for_weights[center_pawn_idx][WHITE_SCORE_IDX] += self.weights[center_pawn_idx]
        else:
            self.scores_for_weights[center_pawn_idx][BLACK_SCORE_IDX] += self.weights[center_pawn_idx]
