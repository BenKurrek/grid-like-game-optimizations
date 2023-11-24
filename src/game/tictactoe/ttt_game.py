# src/game/chess.py
import chess
import chess.svg
import random
from src.game.base_game import BaseGame
import json

weight_labels = [
    "Pawn Weight",
    "Knight Weight",
    "Bishop Weight",
    "Rook Weight",
    "Queen Weight",
    "King Weight",
    "Total Material Weight",
    "Pawn Structure Weight",
    "Piece Development Weight",
    "King Safety Weight",
    "Control of Key Squares Weight"
]
weight_bounds = [
    # Material
    (0, 1000), # pawn
    (0, 1000), # knight
    (0, 1000), # bishop    
    (0, 1000), # rook
    (0, 1000), # queen
    (1, 1), # king

    # Extra
    (1, 1), # Total Material Weight
    (0, 0), # pawn structure
    (0, 0), # piece development
    (0, 0), # king safety
    (0, 0), # control of key squares
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

class tttGame(BaseGame):
    def __init__(self, meta):
        board, game_moves, move_sequences, ranked_moves = meta

        self.board = board
        self.game_moves = game_moves
        self.move_sequences = move_sequences
        self.ranked_moves = ranked_moves

        self.turn = "White" if self.board.turn == chess.WHITE else "Black"
        self.stockfish_move = self.move_sequences['stockfish']['move']
        self.stockfish_score = self.move_sequences['stockfish']['score']
        self.gm_move = self.game_moves[0]

        self.initialize_random_weights()

    # Random starting genes for the chromosome based on lower and upper bounds
    def initialize_random_weights(self):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]

    def get_board_data(self):
        return [self.board, self.game_moves, self.move_sequences, self.ranked_moves]

    def rank_move(self, move):
        return (self.ranked_moves[str(move)], len(list(self.board.legal_moves)))

    def get_weights(self):
        return self.weights
    
    def get_weight_bounds(self):
        return weight_bounds
    
    def get_weight_labels(self): 
        return weight_labels
    
    def update_weights(self, weights):
        self.weights = weights
    
    def evaluate_move(self, move):
        new_board = self.board.copy()
        initial_score = (
            self.material_evaluation(new_board)
            # self.pawn_structure_evaluation(new_board) +
            # self.piece_development_evaluation(new_board) +
            # self.king_safety_evaluation(new_board) +
            # self.control_key_squares_evaluation(new_board)
        )

        # Push the desired moves and then also the move that stockfish would make in retaliation
        for next_move in self.move_sequences[str(move)]['next_moves']:
            new_board.push(chess.Move.from_uci(next_move.uci()))
    
        final_score = (
            self.material_evaluation(new_board)
            # self.pawn_structure_evaluation(new_board) +
            # self.piece_development_evaluation(new_board) +
            # self.king_safety_evaluation(new_board) +
            # self.control_key_squares_evaluation(new_board)
        )
        
        # DEBUGGING
        #if move == self.stockfish_move:
            #print(f"Evaluation of stockfish move: {move} -> Score: {score}")
        #if move == self.gm_move:
            #print(f"Evaluation of gm move: {move} -> Score: {score}")

        #print(f"Turn: {self.turn}, Move: {move.uci()} Initial Score: {initial_score}, Final Score: {final_score}, Difference: {final_score - initial_score}\n")

        return final_score - initial_score
    
    def material_evaluation(self, board):
        # board_pieces = {
        #     # P, N, B, R, Q, K
        #     'WHITE': [0, 0, 0, 0, 0, 0],
        #     'BLACK': [0, 0, 0, 0, 0, 0]
        # }

        # for piece in board.piece_map().values():
        #     color = 'WHITE' if piece.color == chess.WHITE else 'BLACK'
        #     board_pieces[color][piece_map[piece.symbol().lower()]] += 1

        # # Print JSON Stringified Board Pieces
        # print(f"Board Pieces: {json.dumps(board_pieces)}")

        white_material = sum(self.weights[piece_map[piece.symbol().lower()]] for piece in board.piece_map().values() if piece.color == chess.WHITE)
        black_material = sum(self.weights[piece_map[piece.symbol().lower()]] for piece in board.piece_map().values() if piece.color == chess.BLACK)
        evaluation = self.weights[piece_map['MATERIAL_WEIGHT']] * (white_material - black_material)
        return evaluation

    def pawn_structure_evaluation(self, board):
        white_pawn_structure = sum(1 for square in chess.SQUARES if board.piece_at(square) == chess.Piece(chess.PAWN, chess.WHITE))
        black_pawn_structure = sum(1 for square in chess.SQUARES if board.piece_at(square) == chess.Piece(chess.PAWN, chess.BLACK))
        return self.weights['PAWN_STRUCTURE_WEIGHT'] * (white_pawn_structure - black_pawn_structure)

    def piece_development_evaluation(self, board):
        white_piece_development = sum(1 for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.WHITE and square not in chess.BB_RANKS)
        black_piece_development = sum(1 for square in chess.SQUARES if board.piece_at(square) and board.piece_at(square).color == chess.BLACK and square not in chess.BB_RANKS)
        return self.weights['PIECE_DEVELOPMENT_WEIGHT'] * (white_piece_development - black_piece_development)

    def king_safety_evaluation(self, board):
        white_king_safety = sum(1 for square in chess.SQUARES if board.is_attacked_by(chess.BLACK, square))
        black_king_safety = sum(1 for square in chess.SQUARES if board.is_attacked_by(chess.WHITE, square))
        return self.weights['KING_SAFETY_WEIGHT'] * (white_king_safety - black_king_safety)

    def control_key_squares_evaluation(self, board):
        key_squares = ['e4', 'd4', 'c4', 'e5', 'd5', 'c5']
        white_control_key_squares = sum(1 for square in key_squares if board.color_at(chess.parse_square(square)) == chess.WHITE)
        black_control_key_squares = sum(1 for square in key_squares if board.color_at(chess.parse_square(square)) == chess.BLACK)
        return self.weights['CONTROL_KEY_SQUARES_WEIGHT'] * (white_control_key_squares - black_control_key_squares)
    
    # Fitness is defined as the average difference between the actual stockfish score and the evaluated score
    def fitness(self):
        score = 0
        legal_moves = list(self.board.legal_moves)
        
        best_move = best_score = None
        
        for move in legal_moves:
            # Score from the perspective of whose turn it is (from stockfish)
            actual_score = 0

            # Keep track of the best move and score
            evaluated_score = self.evaluate_move(move)
            if best_score is None:
                best_score = evaluated_score
                best_move = move
            elif self.board.turn == chess.WHITE and evaluated_score > best_score:
                best_score = evaluated_score
                best_move = move
            elif self.board.turn == chess.BLACK and evaluated_score < best_score:
                best_score = evaluated_score
                best_move = move

            actual_score = self.move_sequences[str(move)]['score'].relative.score(mate_score=2000)
            score -= abs(evaluated_score - actual_score)
        
        # Interpolate the score based on its rank
        rank = self.ranked_moves[str(best_move)]
        # https://www.desmos.com/calculator/4envqidilb
        score += (len(legal_moves) / rank - 8) * 10

        #print(f"TURN: {self.turn}, Chosen Move: {best_move} With Score: {best_score}\nGM Move: {self.gm_move} Stockfish Move: {self.stockfish_move}, With Stockfish Evaluation: {self.stockfish_score}\n\n")
        return (score / len(legal_moves), best_move, best_score)

    def get_best_move(self):
        best_score = None
        legal_moves = list(self.board.legal_moves)
        for move in legal_moves:
            evaluated_score = self.evaluate_move(move)
            if best_score is None:
                best_score = evaluated_score
                best_move = move
            elif self.board.turn == chess.WHITE and evaluated_score > best_score:
                best_score = evaluated_score
                best_move = move
            elif self.board.turn == chess.BLACK and evaluated_score < best_score:
                best_score = evaluated_score
                best_move = move            
        return best_move

    def visualize_best_move(self, img_size):
        best_move = self.get_best_move()
        return chess.svg.board(
            board=self.board, 
            arrows=[
                chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#FF0000cc"),  # Red for our move
                chess.svg.Arrow(self.game_moves[0].from_square, self.game_moves[0].to_square, color="#00cc00cc"),  # Green for actual move
                chess.svg.Arrow(self.stockfish_move.from_square, self.stockfish_move.to_square, color="#0000ccFF")  # Blue for Stockfish move
                ],
            size=img_size
            )
