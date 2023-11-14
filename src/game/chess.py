# src/game/chess.py

import chess
import chess.svg
import random
from .base_game import BaseGame
from src.utility.chess_extraction import extract_random_positions

class ChessGame(BaseGame):
    def initialize(self):
        self.weights = {
            'piece_values': {
                'p': 1,  # Pawn
                'n': 3,  # Knight
                'b': 3,  # Bishop
                'r': 5,  # Rook
                'q': 9,  # Queen
                'k': 10  # King
            },
            'material': 1.0,
            'pawn_structure': 0.2,
            'piece_development': 0.3,
            'king_safety': 0.4,
            'control_key_squares': 0.1,
        }
        self.board = extract_random_positions(num_positions=1)[0]

    def update_weights(self, weights):
        self.weights = weights
    
    def get_random_next_board_state(self):
        board = chess.Board(self.starting_move)
        legal_moves = [str(move) for move in self.board.legal_moves]
        if legal_moves:
            choice = random.choice(legal_moves)
            board.push(chess.Move.from_uci(choice))
            return str(board.fen())
        return None

    def fitness(self):
        # Material count
        white_material = sum(self.weights['piece_values'][piece.symbol().lower()] for piece in self.board.piece_map().values() if piece.color == chess.WHITE)
        black_material = sum(self.weights['piece_values'][piece.symbol().lower()] for piece in self.board.piece_map().values() if piece.color == chess.BLACK)

        # Pawn structure
        white_pawn_structure = sum(1 for square in chess.SQUARES if self.board.piece_at(square) == chess.Piece(chess.PAWN, chess.WHITE))
        black_pawn_structure = sum(1 for square in chess.SQUARES if self.board.piece_at(square) == chess.Piece(chess.PAWN, chess.BLACK))

        # Piece development
        white_piece_development = sum(1 for square in chess.SQUARES if self.board.piece_at(square) and self.board.piece_at(square).color == chess.WHITE and square not in chess.BB_RANKS)
        black_piece_development = sum(1 for square in chess.SQUARES if self.board.piece_at(square) and self.board.piece_at(square).color == chess.BLACK and square not in chess.BB_RANKS)

        # King safety
        white_king_square = self.board.king(chess.WHITE)
        black_king_square = self.board.king(chess.BLACK)
        white_king_safety = sum(1 for square in chess.SQUARES if self.board.is_attacked_by(chess.BLACK, square))
        black_king_safety = sum(1 for square in chess.SQUARES if self.board.is_attacked_by(chess.WHITE, square))

        # Control of key squares
        white_control_key_squares = sum(1 for square in ['e4', 'd4', 'c4', 'e5', 'd5', 'c5'] if self.board.color_at(chess.parse_square(square)) == chess.WHITE)
        black_control_key_squares = sum(1 for square in ['e4', 'd4', 'c4', 'e5', 'd5', 'c5'] if self.board.color_at(chess.parse_square(square)) == chess.BLACK)

        # Combine features with weights
        score = (
            self.weights['material'] * (white_material - black_material) +
            self.weights['pawn_structure'] * (white_pawn_structure - black_pawn_structure) +
            self.weights['piece_development'] * (white_piece_development - black_piece_development) +
            self.weights['king_safety'] * (white_king_safety - black_king_safety) +
            self.weights['control_key_squares'] * (white_control_key_squares - black_control_key_squares)
        )

        return score
        
    def mutate(self, state):
        board = chess.Board(state)
        legal_moves = [str(move) for move in board.legal_moves]
        if legal_moves:
            move = random.choice(legal_moves)
            board.push(chess.Move.from_uci(move))
        return str(board.fen())

    def crossover(self, parent1, parent2):
        # Assume parent1 and parent2 are move sequences represented as strings
        # game is an instance of the chess game that can check move legality

        # Split the move sequences into individual moves
        moves1 = parent1.split()
        moves2 = parent2.split()

        # Choose a crossover point (could be a random index)
        crossover_point = len(moves1) // 2

        # Create a new move sequence by combining moves from both parents
        new_moves = moves1[:crossover_point]

        # Add valid moves from parent2, ensuring they are legal on the current board
        for move in moves2[crossover_point:]:
            if game.is_valid_move(move):
                new_moves.append(move)

        # Convert the list of moves back to a string
        new_offspring = ' '.join(new_moves)

        return new_offspring

    def get_svg_content(self, state, size):
        board = chess.Board(state)
        return chess.svg.board(board=board, size=size)
