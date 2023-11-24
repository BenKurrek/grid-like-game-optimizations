# pawn.py

import chess
from chess import Square, Piece

weight_labels = [
    "Pawn Material Weight",
    "Pawn Islands Weight",
    "Pawn Chains Weight",
    "Passed Pawns Weight"
]
weight_bounds = [
    # Material
    (0, 1000), # how much the pawn is worth
    (0, 1000), # how much pawn islands are worth
    (0, 1000), # how much pawn chains are worth
    (0, 1000), # how much passed pawns are worth
]

class PawnEvaluator:
    def __init__(self):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]
        # (W, B) scores for each weight
        self.scores_for_weights = [(0, 0) for _ in range(len(weight_bounds))]

    def evaluation_for_piece(self, pice):
        self.material_evaluation(piece)

    def material_evaluation(self, piece):
        if piece.piece_type == chess.PAWN:
            if piece.color == chess.WHITE:
                self.scores_for_weights[0][0] += self.weights[0]
            else:
                self.scores_for_weights[0][1] += self.weights[0]

    def pawn_structure_evaluation(self, board):
        white_pawn_structure = self.calculate_pawn_structure(board, chess.WHITE)
        black_pawn_structure = self.calculate_pawn_structure(board, chess.BLACK)

        pawn_structure_score = (
            self.weights['PAWN_STRUCTURE_WEIGHT'] * (white_pawn_structure - black_pawn_structure) +
            self.weights['PAWN_ISLANDS_WEIGHT'] * self.calculate_pawn_islands(board) +
            self.weights['PAWN_CHAINS_WEIGHT'] * self.calculate_pawn_chains(board) +
            self.weights['PAWN_WEAKNESS_WEIGHT'] * self.calculate_pawn_weakness(board)
        )

        return pawn_structure_score
        
    def calculate_pawn_islands(self, board):
        # Count the number of pawn islands
        pawn_islands = 0
        seen_files = set()

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                file = chess.square_file(square)
                if file not in seen_files:
                    pawn_islands += 1
                    seen_files.add(file)

        return pawn_islands

    def calculate_pawn_chains(self, board):
        # Count the number of pawn chains
        pawn_chains = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                if self.is_pawn_chain(board, square):
                    pawn_chains += 1

        return pawn_chains

    def is_pawn_chain(self, board, square):
        # Check if the pawn at the given square is part of a pawn chain
        file = chess.square_file(square)
        rank = chess.square_rank(square)

        # Check the adjacent squares
        for offset in [-1, 1]:
            neighbor_square = chess.square(file + offset, rank)
            if board.piece_at(neighbor_square) == chess.Piece(chess.PAWN, board.turn):
                return True

        return False

    def calculate_pawn_weakness(self, board):
        # Evaluate pawn weaknesses (isolated pawns and backward pawns)
        pawn_weakness = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN and piece.color == board.turn:
                if self.is_isolated_pawn(board, square) or self.is_backward_pawn(board, square):
                    pawn_weakness += 1

        return pawn_weakness

    def is_isolated_pawn(self, board, square):
        # Check if the pawn at the given square is isolated
        file = chess.square_file(square)

        # Check the adjacent files
        for offset in [-1, 1]:
            neighbor_square = chess.square(file + offset, chess.square_rank(square))
            if board.piece_at(neighbor_square) == chess.Piece(chess.PAWN, board.turn):
                return False

        return True

    def is_backward_pawn(self, board, square):
        # Check if the pawn at the given square is a backward pawn
        file = chess.square_file(square)
        rank = chess.square_rank(square)

        # Check the same file and adjacent files
        for offset in [-1, 0, 1]:
            neighbor_square = chess.square(file + offset, rank + 1)
            if board.piece_at(neighbor_square) == chess.Piece(chess.PAWN, board.turn):
                return False

        return True