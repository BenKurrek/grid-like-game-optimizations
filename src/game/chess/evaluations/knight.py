import chess
import random
from chess import Square, Piece
import random

knight_weight_labels = [
    "Knight Material Weight",
    "Knight Position Weight",
    "Knight Attacking Weight",
    "Knight Defending Weight",
    "Knight number of free spaces",
    "Knight Supported By Pawn"
]
knight_weight_bounds = [
    (200, 400), # how much the knight is worth
    (0, 100), # how much the knights position is worth
    (0, 1000), # how much knights that attack the enemy king are worth
    (0, 1000), # how much knights that defend your king are worth
    (0, 100), # how much the mobility of the knight is worth
    (0, 1000), # how much knights supported by ally pawns are worth
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

WHITE_POSITION_MAPPING = {
    "a1": -50, "b1": -40, "c1": -30, "d1": -30, "e1": -30, "f1": -30, "g1": -40, "h1": -50,
    "a2": -40, "b2": -20, "c2": 0, "d2": 0, "e2": 0, "f2": 0, "g2": -20, "h2": -40,
    "a3": -30, "b3": 0, "c3": 10, "d3": 15, "e3": 15, "f3": 10, "g3": 0, "h3": -30,
    "a4": -30, "b4": 5, "c4": 15, "d4": 20, "e4": 20, "f4": 15, "g4": 5, "h4": -30,
    "a5": -30, "b5": 0, "c5": 15, "d5": 20, "e5": 20, "f5": 15, "g5": 0, "h5": -30,
    "a6": -30, "b6": 5, "c6": 10, "d6": 15, "e6": 15, "f6": 10, "g6": 5, "h6": -30,
    "a7": -40, "b7": -20, "c7": 0, "d7": 5, "e7": 5, "f7": 0, "g7": -20, "h7": -40,
    "a8": -50, "b8": -40, "c8": -30, "d8": -30, "e8": -30, "f8": -30, "g8": -40, "h8": -50,
}

BLACK_POSITION_MAPPING = {
    "a1": -50, "b1": -40, "c1": -30, "d1": -30, "e1": -30, "f1": -30, "g1": -40, "h1": -50,
    "a2": -40, "b2": -20, "c2": 0, "d2": 5, "e2": 5, "f2": 0, "g2": -20, "h2": -40,
    "a3": -30, "b3": 5, "c3": 10, "d3": 15, "e3": 15, "f3": 10, "g3": 5, "h3": -30,
    "a4": -30, "b4": 0, "c4": 15, "d4": 20, "e4": 20, "f4": 15, "g4": 0, "h4": -30,
    "a5": -30, "b5": 5, "c5": 15, "d5": 20, "e5": 20, "f5": 15, "g5": 5, "h5": -30,
    "a6": -30, "b6": 0, "c6": 10, "d6": 15, "e6": 15, "f6": 10, "g6": 0, "h6": -30,
    "a7": -40, "b7": -20, "c7": 0, "d7": 0, "e7": 0, "f7": 0, "g7": -20, "h7": -40,
    "a8": -50, "b8": -40, "c8": -30, "d8": -30, "e8": -30, "f8": -30, "g8": -40, "h8": -50,
}

class KnightEvaluator:
    def __init__(self, board: chess.Board):
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(knight_weight_bounds))]

        self.board = board
        self.adjacent_white_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.WHITE)))]
        self.adjacent_black_king_squares = [chess.square_name(square) for square in list(self.board.attacks(self.board.king(chess.BLACK)))]

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece, attack_squares):
        if piece.piece_type == chess.KNIGHT:
            is_supported = self.is_knight_supported_by_pawn(square, piece)

            self.material_evaluation(piece)
            self.position_evaluation(square, piece)
            self.king_attacking_defending_evalutation(attack_squares, piece)
            self.free_squares_evaluation(attack_squares, piece)

            if is_supported:
                self.supported_knight_evaluation(piece)

    def material_evaluation(self, piece: chess.Piece):
        knight_material_idx = 0
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[knight_material_idx][color_idx] += 1
                
    def position_evaluation(self, square: chess.Square, piece: chess.Piece):
        position_evaluation_idx = 1
        square_name = chess.square_name(square)

        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        square_value = WHITE_POSITION_MAPPING[square_name] if piece.color is chess.WHITE else BLACK_POSITION_MAPPING[square_name]
        self.scores_for_weights[position_evaluation_idx][color_idx] += square_value
                
    def king_attacking_defending_evalutation(self, knight_attack_squares, piece: chess.Piece):
        attacking_knight_idx = 2
        defending_knight_idx = 3
        
        attacking_king_squares = self.adjacent_white_king_squares if piece.color == chess.BLACK else self.adjacent_black_king_squares
        defending_king_squares = self.adjacent_white_king_squares if piece.color == chess.WHITE else self.adjacent_black_king_squares
        
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        
        for knight_attack_square in knight_attack_squares:
            # Attacking
            if knight_attack_square in attacking_king_squares:
                self.scores_for_weights[attacking_knight_idx][color_idx] += 1
            
            # Defending   
            if knight_attack_square in defending_king_squares:
                self.scores_for_weights[defending_knight_idx][color_idx] += 1
                
    def free_squares_evaluation(self, knight_attack_squares, piece: chess.Piece):
        free_square_idx = 4
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[free_square_idx][color_idx] += len(knight_attack_squares)

    def supported_knight_evaluation(self, piece: chess.Piece):
        supported_knight_idx = 5
        color_idx = WHITE_SCORE_IDX if piece.color is chess.WHITE else BLACK_SCORE_IDX
        self.scores_for_weights[supported_knight_idx][color_idx] += 1

    #UTILITY
    def is_knight_supported_by_pawn(self, square, piece):
        # Determine the direction of pawn movement based on the knight's color
        pawn_direction = 1 if piece.color == chess.WHITE else -1

        # Calculate the rank and file of the knight square
        knight_rank = chess.square_rank(square)
        knight_file = chess.square_file(square)

        # Check squares adjacent to the knight
        adjacent_squares = [
            chess.square(knight_file - 1, knight_rank + pawn_direction),
            chess.square(knight_file + 1, knight_rank + pawn_direction)
        ]

        # Check if there is an own pawn adjacent to the knight
        for adjacent_square in adjacent_squares:
            if 0 <= chess.square_file(adjacent_square) <= 7 and 0 <= chess.square_rank(adjacent_square) <= 7:
                # Ensure the square is within bounds
                if self.board.piece_at(adjacent_square) == chess.Piece(chess.PAWN, piece.color):
                    # There is an own pawn adjacent to the knight
                    return 1

        # No own pawn adjacent to the knight
        return 0
                
