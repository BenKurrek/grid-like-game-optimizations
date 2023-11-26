import chess
import random
from chess import Square, Piece

bishop_weight_labels = [
    "Bishop Material Weight",
    "Bishop Attacking Weight",
    "Bishop Defending Weight",
    "Bishop Free Squares Weight",
    "Bishop Pair Weight"
]
bishop_weight_bounds = [
    (220, 420), # how much the bishop is worth
    (0, 1000), # how much pawns that attack the enemy king are worth
    (0, 1000), # how much pawns that defend your king are worth
    (0, 1000), # how much the mobility of the bishop is worth
    (0, 1000), # how much bishop pairs are worth
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
            has_bishop_pair = self.has_bishop_pair(piece)

            self.material_evaluation(piece)
            self.king_attacking_defending_evalutation(square, piece, attack_squares)

    def material_evaluation(self, piece):
        bishop_material_idx = 0
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[bishop_material_idx][color_idx] += 1
    
    def king_attacking_defending_evalutation(self, square: chess.Square, piece: chess.Piece, attack_squares: list[str]):
        attacking_bishop_idx = 1
        defending_bishop_idx = 2
        
        attacking_king_squares = self.adjacent_white_king_squares if piece.color == chess.BLACK else self.adjacent_black_king_squares
        defending_king_squares = self.adjacent_white_king_squares if piece.color == chess.WHITE else self.adjacent_black_king_squares
        
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        
        for bishop_attack_square in attack_squares:
            # Attacking
            if bishop_attack_square in attacking_king_squares:
                self.scores_for_weights[attacking_bishop_idx][color_idx] += 1
            
            # Defending   
            if bishop_attack_square in defending_king_squares:
                self.scores_for_weights[defending_bishop_idx][color_idx] += 1


    def free_squares_evaluation(self, bishop_attack_squares, piece: chess.Piece):
        free_square_idx = 3
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[free_square_idx][color_idx] += len(bishop_attack_squares)

    #UTILITY
    def has_bishop_pair(self, piece):
        # Get the squares occupied by bishops of the specified color
        bishops_squares = self.board.pieces(chess.BISHOP, piece.color)
        print(bishops_squares)

        # Count the number of bishops using the popcount() function
        bishop_count = len(bishops_squares)
        print(bishop_count)

        # Check if the player has a bishop pair
        return bishop_count >= 2