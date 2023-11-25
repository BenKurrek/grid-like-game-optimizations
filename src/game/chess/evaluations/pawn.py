# pawn.py

import chess
import random
from chess import Square, Piece

pawn_weight_labels = [
    "Pawn Material Weight",
    "Center Pawn Weight",
    "Double Pawn Weight",
    "Iso Pawn Weight",
    "Passed Pawn Weight",
]
pawn_weight_bounds = [
    # Material
    (0, 1000), # how much the pawn is worth
    (0, 1000), # how center pawns are worth
    (0, 1000), # how much doubled pawns are penalized
    (0, 1000), # how much isolated pawns are penalized
    (0, 1000), # how much passed pawns are worth
]

WHITE_SCORE_IDX = 0
BLACK_SCORE_IDX = 1

class PawnEvaluator:
    def __init__(self, board):
        self.board = board
        # (W, B) scores for each weight
        self.scores_for_weights = [[0.0, 0.0] for _ in range(len(pawn_weight_labels))]

        self.pawn_islands = 0
        self.seen_files = set()

    def get_scores_for_weights(self):
        return self.scores_for_weights

    def evaluation_for_square(self, square, piece):
        if piece.piece_type == chess.PAWN:
            is_double_pawn, is_passed_pawn = self.check_file_data(square, piece)

            # If the square is a pawn, give it the material bonus
            self.material_evaluation(piece)

            # If the square is in the center, give it a bonus
            if square in chess.SquareSet(chess.BB_CENTER):
                self.center_pawn_evaluation(piece)

            # If the square is a double pawn, give it a penalty
            if is_double_pawn:
                self.double_pawn_evaluation(piece)

            # If the square is a passed pawn, give it a bonus
            if is_passed_pawn:
                self.passed_pawn_evaluation(piece)

            # If the square is an isolated pawn, give it a penalty
            if self.is_isolated_pawn(square, piece):
                self.isolated_pawn_evaluation(piece)

    # Add the weight for a pawn
    def material_evaluation(self, piece):
        pawn_material_idx = 0
        if piece.color == chess.WHITE:
            self.scores_for_weights[pawn_material_idx][WHITE_SCORE_IDX] += 1
        else:
            self.scores_for_weights[pawn_material_idx][BLACK_SCORE_IDX] += 1

    # Add the weight for a center pawn
    def center_pawn_evaluation(self, piece):
        center_pawn_idx = 1
        if piece.color == chess.WHITE:
            self.scores_for_weights[center_pawn_idx][WHITE_SCORE_IDX] += 1
        else:
            self.scores_for_weights[center_pawn_idx][BLACK_SCORE_IDX] += 1

    # Subtract the weight for a double pawn
    def double_pawn_evaluation(self, piece):
        double_pawn_idx = 2
        if piece.color == chess.WHITE:
            self.scores_for_weights[double_pawn_idx][WHITE_SCORE_IDX] -= 1
        else:
            self.scores_for_weights[double_pawn_idx][BLACK_SCORE_IDX] -= 1

    def check_file_data(self, square, piece):
        is_double_pawn = False
        is_passed_pawn = True
        
        file = chess.square_file(square)
        
        # go through other squares in the same file
        for rank in range(8):
            left_file_idx = file - 1
            right_file_idx = file + 1

            left_file_square = chess.square(left_file_idx, rank)
            cur_file_square = chess.square(file, rank)
            right_file_square = chess.square(right_file_idx, rank)

            cur_file_piece = self.board.piece_at(cur_file_square)
            left_file_piece = None
            right_file_piece = None
            
            # Make sure files are in bounds
            if left_file_idx >= 0:
                left_file_piece = self.board.piece_at(left_file_square)
            if right_file_idx <= 7: 
                right_file_piece = self.board.piece_at(right_file_square)

            # Check for double pawn (if same color in same file)
            if cur_file_piece is not None and cur_file_piece.piece_type == chess.PAWN and cur_file_piece.color == piece.color and cur_file_square != square:
                is_double_pawn = True

            # Check for enemy pawn on left side
            if left_file_piece is not None and left_file_piece.piece_type == chess.PAWN and left_file_piece.color != piece.color:
                is_passed_pawn = False

            # Check for enemy pawn on right side
            if right_file_piece is not None and right_file_piece.piece_type == chess.PAWN and right_file_piece.color != piece.color:
                is_passed_pawn = False
            
            # Check for enemy pawn in same file
            if cur_file_piece is not None and cur_file_piece.piece_type == chess.PAWN and cur_file_piece.color != piece.color:
                is_passed_pawn = False

        return is_double_pawn, is_passed_pawn

    # Subtract the weight for an isolated pawn
    def isolated_pawn_evaluation(self, piece):
        isolated_pawn_idx = 3
        if piece.color == chess.WHITE:
            self.scores_for_weights[isolated_pawn_idx][WHITE_SCORE_IDX] -= 1
        else:
            self.scores_for_weights[isolated_pawn_idx][BLACK_SCORE_IDX] -= 1

    def is_isolated_pawn(self, square, piece):
        file = chess.square_file(square)
        rank = chess.square_rank(square)

        # Check all adjacent squares
        for rank_offset in [-1, 0, 1]:
            for file_offset in [-1, 0, 1]:
                if rank_offset == 0 and file_offset == 0:
                    continue  # Skip the current square

                # Calculate neighboring square
                neighbor_file = file + file_offset
                neighbor_rank = rank + rank_offset

                # Check if the neighboring square is within the valid file and rank range
                if (
                    1 <= neighbor_file <= 8 and
                    1 <= neighbor_rank <= 8 and
                    self.board.piece_at(chess.square(neighbor_file, neighbor_rank)) == chess.Piece(chess.PAWN, piece.color)
                ):
                    return False

        return True

    # Add the weight for a passed pawn
    def passed_pawn_evaluation(self, piece):
        if piece.color == chess.WHITE:
            ranks_until_promotion = 7 - chess.square_rank(piece.square())
        else:
            ranks_until_promotion = chess.square_rank(piece.square())
            
        passed_pawn_idx = 4
        if piece.color == chess.WHITE:
            self.scores_for_weights[passed_pawn_idx][WHITE_SCORE_IDX] += ranks_until_promotion
        else:
            self.scores_for_weights[passed_pawn_idx][BLACK_SCORE_IDX] += ranks_until_promotion