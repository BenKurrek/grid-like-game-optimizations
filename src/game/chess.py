# src/game/chess.py

import chess
import chess.svg
import random
from .base_game import BaseGame

weight_upper_bounds = [
    # Material
    25, # pawn
    25, # knight
    25, # bishop    
    25, # rook
    25, # queen
    25, # king

    # Extra
    25, # Total Material Weight
    25, # pawn structure
    25, # piece development
    25, # king safety
    25, # control of key squares
]

piece_map = {
    'p': 0,
    'n': 1,
    'b': 2,
    'r': 3,
    'q': 4,
    'k': 5,
    'MATERIAL_WEIGHT': 6,
    'PAWN_STRUCTURE_WEIGHT': 7,
    'PIECE_DEVELOPMENT_WEIGHT': 8,
    'KING_SAFETY_WEIGHT': 9,
    'CONTROL_KEY_SQUARES_WEIGHT': 10,
}

class ChessGame(BaseGame):
    def __init__(self, meta):
        board, game_moves, board_evaluation = meta

        # Random starting genes for the chromosome
        random_weights = [random.random() * weight_upper_bounds[i] for i in range(len(weight_upper_bounds))]
        self.weights = random_weights

        self.board = board
        self.game_moves = game_moves
        self.board_evaluation = board_evaluation

    def get_weights(self):
        return self.weights
    
    def update_weights(self, weights):
        self.weights = weights
    
    def evaluate_move(self, move):
        new_board = chess.Board(self.board.fen())
        new_board.push(move)
        
         # Material count
        white_material = sum(self.weights[piece_map[piece.symbol().lower()]] for piece in new_board.piece_map().values() if piece.color == chess.WHITE)
        black_material = sum(self.weights[piece_map[piece.symbol().lower()]] for piece in new_board.piece_map().values() if piece.color == chess.BLACK)

        # Pawn structure
        white_pawn_structure = sum(1 for square in chess.SQUARES if new_board.piece_at(square) == chess.Piece(chess.PAWN, chess.WHITE))
        black_pawn_structure = sum(1 for square in chess.SQUARES if new_board.piece_at(square) == chess.Piece(chess.PAWN, chess.BLACK))

        # Piece development
        white_piece_development = sum(1 for square in chess.SQUARES if new_board.piece_at(square) and new_board.piece_at(square).color == chess.WHITE and square not in chess.BB_RANKS)
        black_piece_development = sum(1 for square in chess.SQUARES if new_board.piece_at(square) and new_board.piece_at(square).color == chess.BLACK and square not in chess.BB_RANKS)

        # King safety
        white_king_square = new_board.king(chess.WHITE)
        black_king_square = new_board.king(chess.BLACK)
        white_king_safety = sum(1 for square in chess.SQUARES if new_board.is_attacked_by(chess.BLACK, square))
        black_king_safety = sum(1 for square in chess.SQUARES if new_board.is_attacked_by(chess.WHITE, square))

        # Control of key squares
        white_control_key_squares = sum(1 for square in ['e4', 'd4', 'c4', 'e5', 'd5', 'c5'] if new_board.color_at(chess.parse_square(square)) == chess.WHITE)
        black_control_key_squares = sum(1 for square in ['e4', 'd4', 'c4', 'e5', 'd5', 'c5'] if new_board.color_at(chess.parse_square(square)) == chess.BLACK)

        # Combine features with weights
        score = (
            self.weights[piece_map['MATERIAL_WEIGHT']] * (white_material - black_material) +
            self.weights[piece_map['PAWN_STRUCTURE_WEIGHT']] * (white_pawn_structure - black_pawn_structure) +
            self.weights[piece_map['PIECE_DEVELOPMENT_WEIGHT']] * (white_piece_development - black_piece_development) +
            self.weights[piece_map['KING_SAFETY_WEIGHT']] * (white_king_safety - black_king_safety) +
            self.weights[piece_map['CONTROL_KEY_SQUARES_WEIGHT']] * (white_control_key_squares - black_control_key_squares)
        )

        return score
    
    # Fitness is defined as the average difference between the actual stockfish score and the evaluated score
    def fitness(self):
        score = 0
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            # Score from the perspective of white (from stockfish)
            actual_score = self.board_evaluation[str(move)].white()
            evaluated_score = self.evaluate_move(move)
            score -= abs(evaluated_score - actual_score.score())
        return score / len(legal_moves)
    
    def mutate(self, state):
        board = chess.Board(state)
        legal_moves = [str(move) for move in board.legal_moves]
        if legal_moves:
            move = random.choice(legal_moves)
            board.push(chess.Move.from_uci(move))
        return str(board.fen())

    def crossover(self, game2):
        child_weights = []
        for idx in range(len(self.weights)):
            # Randomly choose weights from either parent
            child_weights.append(random.choice([self.weights[idx], game2.get_weights()[idx]]))

        # Create a new ChessGame instance for the child
        child_game = ChessGame([self.board, self.game_moves, self.board_evaluation])
        child_game.update_weights(child_weights)
        return child_game

    def get_svg_content(self, state, size):
        board = chess.Board(state)
        return chess.svg.board(board=board, size=size)
