import chess
import random
from chess import Square, Piece

queen_weight_labels = [
    "Queen Material Weight",
    "Queen Attacking Weight",
    "Queen Defending Weight",
    "Queen number of free spaces",
]
queen_weight_bounds = [
    (900, 1000), # how much the queen is worth
    (0, 100), # how much queens that attack the enemy king are worth
    (0, 100), # how much queens that defend your king are worth
    (0, 30), # how much the mobility of queen is worth
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class QueenEvaluator:
    def __init__(self, board: chess.Board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(queen_weight_bounds))]
        self.board = board
        self.adjacent_white_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.WHITE)))]
        self.adjacent_black_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.BLACK)))]

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece, attack_squares):
        if piece.piece_type == chess.QUEEN:
            self.material_evaluation(piece)
            self.king_attacking_defending_evalutation(attack_squares, square, piece)
            self.free_squares_evaluation(attack_squares, piece)

    def material_evaluation(self, piece):
        queen_material_idx = 0
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[queen_material_idx][color_idx] += 1
            
    def king_attacking_defending_evalutation(self, queen_attack_squares, square: chess.Square, piece: chess.Piece):
        attacking_pawn_idx = 1
        defending_pawn_idx = 2
        
        attacking_king_squares = self.adjacent_white_king_squares if piece.color == chess.BLACK else self.adjacent_black_king_squares
        defending_king_squares = self.adjacent_white_king_squares if piece.color == chess.WHITE else self.adjacent_black_king_squares
        
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        
        for queen_attack_square in queen_attack_squares:
            # Attacking
            if queen_attack_square in attacking_king_squares:
                self.scores_for_weights[attacking_pawn_idx][color_idx] += 1
            
            # Defending   
            if queen_attack_square in defending_king_squares:
                self.scores_for_weights[defending_pawn_idx][color_idx] += 1
     
    def free_squares_evaluation(self, queen_attack_squares, piece: chess.Piece):
        free_square_idx = 3
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[free_square_idx][color_idx] += len(queen_attack_squares)