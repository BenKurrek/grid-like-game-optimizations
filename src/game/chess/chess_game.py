# src/game/chess.py
import chess
import chess.svg
import random
from src.game.base_game import BaseGame

from src.game.chess.evaluations.queen import QueenEvaluator, queen_weight_bounds, queen_weight_labels
from src.game.chess.evaluations.rook import RookEvaluator, rook_weight_bounds, rook_weight_labels
from src.game.chess.evaluations.knight import KnightEvaluator, knight_weight_bounds, knight_weight_labels
from src.game.chess.evaluations.pawn import PawnEvaluator, pawn_weight_bounds, pawn_weight_labels
from src.game.chess.evaluations.bishop import BishopEvaluator, bishop_weight_bounds, bishop_weight_labels
from src.game.chess.evaluations.king import KingEvaluator, king_weight_bounds, king_weight_labels

import json

class ChessGame(BaseGame):
    def __init__(self, meta):
        board, game_moves, move_sequences, ranked_moves, eval_count_cache = meta

        self.board = board
        self.game_moves = game_moves
        self.move_sequences = move_sequences
        self.ranked_moves = ranked_moves

        self.turn = "White" if self.board.turn == chess.WHITE else "Black"
        self.stockfish_move = self.move_sequences['stockfish']['move']
        self.stockfish_score = self.move_sequences['stockfish']['score']
        self.gm_move = self.game_moves[0]

        self.initialize_random_weights()

        self.eval_count_cache = eval_count_cache
        self.eval_count_from_cache(self.board)

    # Random starting genes for the chromosome based on lower and upper bounds
    def initialize_random_weights(self):
        self.weight_for_eval_counts = [
            [random.uniform(float(lower), float(upper)) for lower, upper in queen_weight_bounds],
            [random.uniform(float(lower), float(upper)) for lower, upper in rook_weight_bounds],
            [random.uniform(float(lower), float(upper)) for lower, upper in knight_weight_bounds],
            [random.uniform(float(lower), float(upper)) for lower, upper in bishop_weight_bounds],
            [random.uniform(float(lower), float(upper)) for lower, upper in king_weight_bounds],
            [random.uniform(float(lower), float(upper)) for lower, upper in pawn_weight_bounds],
        ]

    def get_board_data(self):
        return [self.board, self.game_moves, self.move_sequences, self.ranked_moves, self.eval_count_cache]

    def rank_move(self, move):
        return (self.ranked_moves[str(move)], len(list(self.board.legal_moves)))

    def get_weights(self):
        # concatenate all the weights into a single list
        concatenated_weights = []
        for sublist in self.weight_for_eval_counts:
            concatenated_weights.extend(sublist)

        return concatenated_weights

    def get_weight_bounds(self):
        return queen_weight_bounds + rook_weight_bounds + knight_weight_bounds + bishop_weight_bounds + king_weight_bounds + pawn_weight_bounds
    
    def get_weight_labels(self):
        return queen_weight_labels + rook_weight_labels + knight_weight_labels + bishop_weight_labels + king_weight_labels + pawn_weight_labels
    
    def update_weights(self, weights):
        queen_weights = weights[:len(queen_weight_bounds)]
        rook_weights = weights[len(queen_weight_bounds):len(queen_weight_bounds) + len(rook_weight_bounds)]
        knight_weights = weights[len(queen_weight_bounds) + len(rook_weight_bounds):len(queen_weight_bounds) + len(rook_weight_bounds) + len(knight_weight_bounds)]
        bishop_weights = weights[len(queen_weight_bounds) + len(rook_weight_bounds) + len(knight_weight_bounds):len(queen_weight_bounds) + len(rook_weight_bounds) + len(knight_weight_bounds) + len(bishop_weight_bounds)]
        king_weights = weights[len(queen_weight_bounds) + len(rook_weight_bounds) + len(knight_weight_bounds) + len(bishop_weight_bounds):len(queen_weight_bounds) + len(rook_weight_bounds) + len(knight_weight_bounds) + len(bishop_weight_bounds) + len(king_weight_bounds)]
        pawn_weights = weights[len(queen_weight_bounds) + len(rook_weight_bounds) + len(knight_weight_bounds) + len(bishop_weight_bounds) + len(king_weight_bounds):]

        self.weight_for_eval_counts = [queen_weights, rook_weights, knight_weights, bishop_weights, king_weights, pawn_weights]
    
    def eval_count_from_cache(self, board):
        if self.eval_count_cache.get(str(board)) is not None:
            return self.eval_count_cache.get(str(board))

        

        # Instantiate the evaluators and update their scores for each square in the board
        # At the end, the score will be the sum of all the evaluations
        queen_evaluator = QueenEvaluator(board)
        rook_evaluator = RookEvaluator(board)
        knight_evaluator = KnightEvaluator(board)
        bishop_evaluator = BishopEvaluator(board)
        king_evaluator = KingEvaluator(board)
        pawn_evaluator = PawnEvaluator(board)

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                # Get the squares that the piece is attacking
                attack_squares = [chess.square_name(square) for square in list(board.attacks(square))]
                
                queen_evaluator.evaluation_for_square(square, piece, attack_squares)
                rook_evaluator.evaluation_for_square(square, piece, attack_squares)
                knight_evaluator.evaluation_for_square(square, piece, attack_squares)
                bishop_evaluator.evaluation_for_square(square, piece, attack_squares)
                pawn_evaluator.evaluation_for_square(square, piece, attack_squares)
                king_evaluator.evaluation_for_square(square, piece)

        # Add the scores for each evaluator to the total score
        queen_scores_for_weights = queen_evaluator.get_scores_for_weights()
        rook_scores_for_weights = rook_evaluator.get_scores_for_weights()
        knight_scores_for_weights = knight_evaluator.get_scores_for_weights()
        bishop_scores_for_weights = bishop_evaluator.get_scores_for_weights()
        king_scores_for_weights = king_evaluator.get_scores_for_weights()
        pawn_scores_for_weights = pawn_evaluator.get_scores_for_weights()

        eval_count_for_weight = [queen_scores_for_weights, rook_scores_for_weights, knight_scores_for_weights, bishop_scores_for_weights, king_scores_for_weights, pawn_scores_for_weights]

        self.eval_count_cache[str(board)] = eval_count_for_weight
        return eval_count_for_weight

    def score_board_state(self, board):
        eval_count_for_weight = self.eval_count_from_cache(board)

        white_score = 0
        black_score = 0
        # Sum the scores for each weight
        for piece_type, eval_counts in enumerate(eval_count_for_weight):
            piece_weights = self.weight_for_eval_counts[piece_type]

            for weight_idx, eval_count_for_weight in enumerate(eval_counts):
                weight = piece_weights[weight_idx]

                white_score += weight * eval_count_for_weight[0]
                black_score += weight * eval_count_for_weight[1]

        return white_score - black_score

    def evaluate_move(self, move):
        new_board = self.board.copy()
        initial_score = self.score_board_state(new_board)

        # Push the desired moves and then also the move that stockfish would make in retaliation
        for next_move in self.move_sequences[str(move)]['next_moves']:
            new_board.push(chess.Move.from_uci(next_move.uci()))
    
        final_score = self.score_board_state(new_board)
        
        # DEBUGGING
        #if move == self.stockfish_move:
            #print(f"Evaluation of stockfish move: {move} -> Score: {score}")
        #if move == self.gm_move:
            #print(f"Evaluation of gm move: {move} -> Score: {score}")

        #print(f"Turn: {self.turn}, Move: {move.uci()} Initial Score: {initial_score}, Final Score: {final_score}, Difference: {final_score - initial_score}\n")

        return final_score - initial_score
    
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
