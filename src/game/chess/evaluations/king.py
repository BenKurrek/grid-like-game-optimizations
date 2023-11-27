import chess
import random
from chess import Square, Piece

king_weight_labels = [
    "King Material Weight",
    "King Castle",
    "King Already Castled Weight"
]
king_weight_bounds = [
    (1.0, 1.0), # how much the king is worth
    (0,30), # how much castling is worth
    (0,100), # how much it is worth if a king has already castled
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
            # Human Readbale square
            square_name = chess.square_name(square)
            has_castled = self.has_castled(square, piece)

            self.material_evaluation(piece)
            self.king_castle_evaluation(piece)

            if has_castled:
                self.has_castled_evaluation(piece)

    def material_evaluation(self, piece):
        material_idx = 0
        if piece.color == chess.WHITE:
            self.scores_for_weights[material_idx][WHITE_SCORE_IDX] += 1
        else:
            self.scores_for_weights[material_idx][BLACK_SCORE_IDX] += 1
    
    def king_castle_evaluation(self, piece: chess.Piece):
        castling_idx = 1
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        count = int(self.board.has_kingside_castling_rights(piece.color)) + int(self.board.has_queenside_castling_rights(piece.color))
        self.scores_for_weights[castling_idx][color_idx] += count

    def has_castled_evaluation(self, piece: chess.Piece):
        castled_idx = 2
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[castled_idx][color_idx] += 1

    # UTILITY
    def has_castled(self, square, piece):
        # Check if there's a castling move involving the king
        for move in self.board.move_stack:
            if piece.color == chess.WHITE and move.uci() in {'e1g1', 'e1c1', 'e8g8', 'e8c8'}:
                return True

            if piece.color == chess.BLACK and move.uci() in {'e8g8', 'e8c8'}:
                return True

        return False