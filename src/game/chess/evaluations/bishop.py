import chess
import random
from chess import Square, Piece

bishop_weight_labels = [
    "Bishop Material Weight",
    "Bishop Attacking Weight",
    "Bishop Defending Weight"
]
bishop_weight_bounds = [
    # Material
    (220, 420), # how much the bishop is worth
     # Attacking
    (0, 1000),
    # Defending
    (0, 1000),
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class BishopEvaluator:
    def __init__(self, board: chess.Board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0, 0] for _ in range(len(bishop_weight_bounds))]
        
        self.board = board
        self.adjacent_white_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.WHITE)))]
        self.adjacent_black_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.BLACK)))]

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece, attack_squares):
        if piece.piece_type == chess.BISHOP:
            self.material_evaluation(piece)
            self.king_attacking_defending_evalutation(square, piece, attack_squares)

    def material_evaluation(self, piece):
        if piece.color == chess.WHITE:
            self.scores_for_weights[0][0] += 1
        else:
            self.scores_for_weights[0][1] += 1
    
    def king_attacking_defending_evalutation(self, square: chess.Square, piece: chess.Piece, attack_squares: list[str]):
        attacking_bishop_idx = 1
        defending_bishop_idx = 2
        
        attacking_king_squares = self.adjacent_white_king_squares if piece.color == chess.BLACK else self.adjacent_black_king_squares
        defending_king_squares = self.adjacent_white_king_squares if piece.color == chess.WHITE else self.adjacent_black_king_squares
        
        score_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        
        for bishop_attack_square in attack_squares:
            # Attacking
            if bishop_attack_square in attacking_king_squares:
                self.scores_for_weights[attacking_bishop_idx][score_idx] += 1
            
            # Defending   
            if bishop_attack_square in defending_king_squares:
                self.scores_for_weights[defending_bishop_idx][score_idx] += 1