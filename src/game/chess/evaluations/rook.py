import chess
import random
from chess import Square, Piece

rook_weight_labels = [
    "Rook Material Weight",
    "Rook Attacking Weight",
    "Rook Defending Weight",
    "Rook number of free spaces",
]
rook_weight_bounds = [
    # Material
    (0, 1000), # how much the rook is worth
     # Attacking
    (0, 1000),
    # Defending
    (0, 1000),
    # Free spaces
    (0, 1000),
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class RookEvaluator:    
    def __init__(self, board: chess.Board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(rook_weight_bounds))]
        self.board = board
        
        self.adjacent_white_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.WHITE)))]
        self.adjacent_black_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.BLACK)))]

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece):
        rook_attack_squares = [chess.square_name(square) for square in list(self.board.attacks(square))]
        if piece.piece_type == chess.ROOK:
            self.material_evaluation(piece)
            self.king_attacking_defending_evalutation(rook_attack_squares, square, piece)
            self.free_squares_evaluation(rook_attack_squares, piece)

    def material_evaluation(self, piece):
        rook_material_idx = 0
        score_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[rook_material_idx][score_idx] += 1
            
    def king_attacking_defending_evalutation(self, rook_attack_squares: list[str], square: chess.Square, piece: chess.Piece):
        attacking_pawn_idx = 1
        defending_pawn_idx = 2
        
        attacking_king_squares = self.adjacent_white_king_squares if piece.color == chess.BLACK else self.adjacent_black_king_squares
        defending_king_squares = self.adjacent_white_king_squares if piece.color == chess.WHITE else self.adjacent_black_king_squares
    
        score_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
    # TODO correct color calculations
        for rook_attack_square in rook_attack_squares:
            # Attacking
            if rook_attack_square in attacking_king_squares:
                self.scores_for_weights[attacking_pawn_idx][score_idx] += 1
            
            # Defending   
            if rook_attack_square in defending_king_squares:
                self.scores_for_weights[defending_pawn_idx][score_idx] += 1
                
    def free_squares_evaluation(self, rook_attack_squares, piece: chess.Piece):
        free_square_idx = 3
        score_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[free_square_idx][score_idx] = len(rook_attack_squares)
        