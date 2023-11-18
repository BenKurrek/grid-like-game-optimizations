# pawn.py

import chess
from chess import Square, Piece

class PawnEvaluator:
    def __init__(self):
        # Initialize your class variables, including self.weights and piece_map
        self.weights = {
            'PAWN_STRUCTURE_WEIGHT': 0.5,
            'PAWN_ISLANDS_WEIGHT': 0.2,
            'PAWN_CHAINS_WEIGHT': 0.3,
            'PAWN_WEAKNESS_WEIGHT': 0.4,
        }

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

    def calculate_pawn_structure(self, board, color):
        # Count the number of pawns for the given color
        pawns = [square for square in chess.SQUARES if board.piece_at(square) == chess.Piece(chess.PAWN, color)]
        return len(pawns)

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