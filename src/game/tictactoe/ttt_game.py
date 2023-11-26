# src/game/chess.py
import math
import chess
import chess.svg
import random
from src.game.base_game import BaseGame
from src.utility.ttt_extraction import available_moves, make_move, undo_move, check_winner, minimax
from itertools import permutations
import json

weight_labels = [
    "3-corner",
    "2-adjacent-corner",
    "2-opposite-corner",
    "1-corner",
    "middle",
    "2-in-a-row-edge",
    "2-in-a-row-center",
]
weight_bounds = [
    (-100, 100), # Holding 3 corners
    (-100, 100), # Holding 2 adjacent corners
    (-100, 100), # Holding 2 opposite corners
    (-100, 100), # Holding 1 corner
    (-100, 100), # Holding middle
    (-100, 100), # Holding two in a row edge
    (-100, 100), # Holding two in a row center
]

class tttGame(BaseGame):
    def __init__(self, meta):
        board, moves_and_scores = meta

        self.board = board
        self.moves_and_scores = moves_and_scores
        self.initialize_random_weights()

    # Random starting genes for the chromosome based on lower and upper bounds
    def initialize_random_weights(self):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]

    def get_board_data(self):
        return [self.board, self.moves_and_scores]

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
    
    def determine_best_move_from_weights(self):
        # start with random guesses
        best_move = available_moves(self.board)[0]
        best_score = -math.inf

        for move in available_moves(self.board):
            # evaluate a score for each weight
            score = self.evaluate_move(move)
            if score > best_score:
                best_move = move
                best_score = score
            
        return best_move, best_score

    def evaluate_move(self, move):
        new_board = self.board.copy()
        
        three_corners_score = self.three_corners(new_board)
        two_adj_corners_score = self.two_adj_corners(new_board)
        two_opp_corners_score = self.two_opp_corners(new_board)
        one_corner_score = self.one_corner(new_board)
        middle_score = self.middle(new_board)
        two_in_a_row_edge_score = self.two_in_a_row_edge(new_board)
        two_in_a_row_middle_score = self.two_in_a_row_middle(new_board)
        initial_score = (
            self.weights[0] * three_corners_score +
            self.weights[1] * two_adj_corners_score +
            self.weights[2] * two_opp_corners_score +
            self.weights[3] * one_corner_score +
            self.weights[4] * middle_score +
            self.weights[5] * two_in_a_row_edge_score +
            self.weights[6] * two_in_a_row_middle_score
        )

        make_move(new_board, move, "X")

        three_corners_score = self.three_corners(new_board)
        two_adj_corners_score = self.two_adj_corners(new_board)
        two_opp_corners_score = self.two_opp_corners(new_board)
        one_corner_score = self.one_corner(new_board)
        middle_score = self.middle(new_board)
        two_in_a_row_edge_score = self.two_in_a_row_edge(new_board)
        two_in_a_row_middle_score = self.two_in_a_row_middle(new_board)
        final_score = (
            self.weights[0] * three_corners_score +
            self.weights[1] * two_adj_corners_score +
            self.weights[2] * two_opp_corners_score +
            self.weights[3] * one_corner_score +
            self.weights[4] * middle_score +
            self.weights[5] * two_in_a_row_edge_score +
            self.weights[6] * two_in_a_row_middle_score
        )

        return final_score - initial_score
    
    # Cost is the minimax difference between the actual best move and the predicted best move
    def cost(self):
        score = -math.inf
        (best_move, best_score) = self.determine_best_move_from_weights(self.board)
        minimax_best_score = -math.inf
        for move in self.moves_and_scores:
            if move[1] > minimax_best_score:
                minimax_best_score = move[1]
                minimax_best_move = move[0]

            if move[0] == best_move:
                predicted_best_minimax_score = move[1]
        
        return predicted_best_minimax_score - minimax_best_score
            
        
        

    def three_corners(self, board):
        # Any combination of 3 corners
        conditions = [(0, 2, 6), (2, 6, 8), (0, 2, 8), (0, 6, 8)]
        return any(board[a] == board[b] == board[c] == "X" for a, b, c in conditions)
    
    def two_opp_corners(self, board):
        # Any combination of 2 opposite corners
        conditions = [(0, 8), (2, 6)]
        return any(board[a] == board[b] == "X" for a, b in conditions)
    
    def two_adj_corners(self, board):
        # Any combination of 2 adjacent corners
        conditions = [(0, 2), (6, 8)], [(0, 6), (2, 8)]
        return any(board[a] == board[b] == "X" for a, b in conditions)
    
    def one_corner(self, board):
        conditions = [0, 2, 6, 8]
        return any(board[a] == "X" for a in conditions)
    
    def middle(self, board):
        return board[4] == "X"
    
    def two_in_a_row_edge(self, board):
        conditions = [(0, 1), (1, 2), (0, 3), (2, 5), (3, 6), (5, 8), (6, 7), (7, 8)]
        return any(board[a] == board[b] == "X" for a, b in conditions)
    
    def two_in_a_row_middle(self, board):
        conditions = [(1, 4), (3, 4), (4, 5), (4, 7)]
        return any(board[a] == board[b] == "X" for a, b in conditions)
