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
    "2-adjacent-corner",
    "2-opposite-corner",
    "1-corner",
    "middle",
]
weight_bounds = [
    (-10000, 10000), # Holding 2 adjacent corners
    (-10000, 10000), # Holding 2 opposite corners
    (-10000, 10000), # Holding 1 corner
    (-10000, 10000), # Holding middle
]

class tttGame(BaseGame):
    # "3-corner",
    # "2-in-a-row-edge",
    # "2-in-a-row-center",
    # (-10000, 10000), # Holding 3 corners
#     (-10000, 10000), # Holding two in a row edge
#     (-10000, 10000), # Holding two in a row center
    def __init__(self, meta):
        board, moves_and_scores = meta

        self.board = board
        self.moves_and_scores = moves_and_scores
        self.initialize_random_weights()
        self.rank_moves()

    # Random starting genes for the chromosome based on lower and upper bounds
    def initialize_random_weights(self):
        self.weights = [random.uniform(float(lower), float(upper)) for lower, upper in weight_bounds]

    def get_board_data(self):
        return [self.board, self.moves_and_scores]

    def rank_move(self, move):
        rank = 0;
        for move_score in self.moves_and_scores:
            if move_score[0] == move:
                rank = move_score[1]
        return (rank, len(list(self.moves_and_scores)))

    def get_weights(self):
        return self.weights
    
    def get_best_move(self):
        best_move, best_score = self.determine_best_move_from_weights()
        return best_move
    
    def rank_moves(self):
        self.ranked_moves = sorted(self.moves_and_scores, key=lambda x: x[1], reverse=True)
        
    def visualize_best_move(self, img_size=400):
        return None

    def get_weight_bounds(self):
        return weight_bounds
    
    def get_weight_labels(self): 
        return weight_labels
    
    def update_weights(self, weights):
        self.weights = weights
    
    # Cost is the minimax difference between the actual best move and the predicted best move
    def fitness(self):
        # best score from determine_best_move_from_weights is internal score (weights * features)
        (predicted_best_move, best_score) = self.determine_best_move_from_weights()

        minimax_best_score = -math.inf
        for move in self.moves_and_scores:
            # Get ACTUAL best move according to minimax
            if move[1] > minimax_best_score:
                minimax_best_score = move[1]
                minimax_best_move = move[0]

            # Get the score the the predicted best move
            if move[0] == predicted_best_move:
                predicted_best_minimax_score = move[1]
        
        print(f"predicted {predicted_best_move}")
        print(f"predicted score {predicted_best_minimax_score}")
        # maximize predicted - actual, in this case trying to get it to 0
        return predicted_best_minimax_score - minimax_best_score, predicted_best_move, predicted_best_minimax_score
    
    def determine_best_move_from_weights(self):
        # start with random guesses
        best_move = available_moves(self.board)[0]
        best_score = -math.inf

        move_scores = list()

        for move in available_moves(self.board):
            # evaluate a score for each weight
            score = self.evaluate_move(move)
            if score > best_score:
                best_move = move
                best_score = score
            move_scores.append((move, score))
        print("calculated scores: {}".format(move_scores))
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
            self.weights[0] * two_adj_corners_score +
            self.weights[1] * two_opp_corners_score +
            self.weights[2] * one_corner_score +
            self.weights[3] * middle_score 
            # self.weights[0] * three_corners_score +
            # self.weights[5] * two_in_a_row_edge_score +
            # self.weights[6] * two_in_a_row_middle_score
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
            self.weights[0] * two_adj_corners_score +
            self.weights[1] * two_opp_corners_score +
            self.weights[2] * one_corner_score +
            self.weights[3] * middle_score 
            # self.weights[0] * three_corners_score +
            # self.weights[5] * two_in_a_row_edge_score +
            # self.weights[6] * two_in_a_row_middle_score
        )

        return final_score - initial_score
    
            
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
        conditions = [(0, 2), (6, 8), (0, 6), (2, 8)]
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
