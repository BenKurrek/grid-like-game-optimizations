# src/game/chess.py
import math
import chess
import chess.svg
import random
from src.game.base_game import BaseGame
from src.utility.ttt_extraction import available_moves, make_move, undo_move, check_winner, minimax
from itertools import permutations
import json

# Edges controlled
# Number of 2 in a row
# Middle control


# weight_labels = [
#     "2-adjacent-corner",
#     "2-opposite-corner",
#     "1-corner",
#     "middle",
#     "3-corner",
#     "2-in-a-row-edge",
#     "2-in-a-row-center",
#     "A1",
#     "A2",
#     "A3",
#     "B1",
#     "B2",
#     "B3",
#     "C1",
#     "C2",
#     "C3",
# ]
# weight_bounds = [
#     (-10, 10), # Holding 2 adjacent corners
#     (-10, 10), # Holding 2 opposite corners
#     (-10, 10), # Holding 1 corner
#     (-10, 10), # Holding middle
#     (-10, 10), # Holding 3 corners
#     (-10, 10), # Holding two in a row edge
#     (-10, 10), # Holding two in a row center

#     (-10, 10), # A1
#     (-10, 10), # A2
#     (-10, 10), # A3
#     (-10, 10), # B1
#     (-10, 10), # B2
#     (-10, 10), # B3
#     (-10, 10), # C1
#     (-10, 10), # C2
#     (-10, 10), # C3
# ]

weight_labels = [
    "corners-controlled",
    "middle-controlled",
    "two-in-a-row",
    "winning-move",
    "blocking-win",
    "forking-move",
    "blocking-fork",
    
    "A1",
    "A2",
    "A3",
    "B1",
    "B2",
    "B3",
    "C1",
    "C2",
    "C3",
]
weight_bounds = [
    (-10, 10), # Holding 2 adjacent corners
    (-10, 10), # Holding 2 opposite corners
    (-10, 10), # Holding 1 corner
    (-10, 10), # Holding middle
    (-10, 10), # Holding 3 corners
    (-10, 10), # Holding two in a row edge
    (-10, 10), # Holding two in a row center

    (-10, 10), # A1
    (-10, 10), # A2
    (-10, 10), # A3
    (-10, 10), # B1
    (-10, 10), # B2
    (-10, 10), # B3
    (-10, 10), # C1
    (-10, 10), # C2
    (-10, 10), # C3
]

class tttGame(BaseGame):
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
        rank = 1
        for v in self.moves_and_scores:
            if v[0] == move:
                return (rank, len(list(self.moves_and_scores)))
            rank += 1
        
        return (rank, len(list(self.moves_and_scores)))

    def get_weights(self):
        return self.weights
    
    def get_best_move(self):
        best_move, best_score = self.determine_best_move_from_weights()
        return best_move
    
    def rank_moves(self):
        self.moves_and_scores = sorted(self.moves_and_scores, key=lambda x: x[1], reverse=True)
        
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
        score = 0
        
        # start with random guesses
        best_move = available_moves(self.board)[0]
        best_score = -math.inf

        avail_moves = available_moves(self.board)
        for move in avail_moves:
            # evaluate a score for each weight
            evaluated_score = self.evaluate_move(move)
            # filter through self.moves_and_scores to get the index of the tuple whose index 0 is the move
            # then get the score from that tuple
            minimax_score = 0
            for v in self.moves_and_scores:
                if v[0] == move:
                    minimax_score = v[1]          
            
            if evaluated_score > best_score:
                best_move = move
                best_score = evaluated_score

            score -= abs(minimax_score - evaluated_score)
        return (score / len(avail_moves), best_move, best_score)
    
    def evaluate_move(self, move):
        new_board = self.board.copy()
        
        three_corners_score = self.three_corners(new_board)
        two_adj_corners_score = self.two_adj_corners(new_board)
        two_opp_corners_score = self.two_opp_corners(new_board)
        one_corner_score = self.one_corner(new_board)
        middle_score = self.middle(new_board)
        two_in_a_row_edge_score = self.two_in_a_row_edge(new_board)
        two_in_a_row_middle_score = self.two_in_a_row_middle(new_board)
        a1_score = self.a1(new_board)
        a2_score = self.a2(new_board)
        a3_score = self.a3(new_board)
        b1_score = self.b1(new_board)
        b2_score = self.b2(new_board)
        b3_score = self.b3(new_board)
        c1_score = self.c1(new_board)
        c2_score = self.c2(new_board)
        c3_score = self.c3(new_board)
        initial_score = (
            self.weights[0] * two_adj_corners_score +
            self.weights[1] * two_opp_corners_score +
            self.weights[2] * one_corner_score +
            self.weights[3] * middle_score +
            self.weights[4] * three_corners_score +
            self.weights[5] * two_in_a_row_edge_score +
            self.weights[6] * two_in_a_row_middle_score +
            self.weights[7] * a1_score +
            self.weights[8] * a2_score +
            self.weights[9] * a3_score +
            self.weights[10] * b1_score +
            self.weights[11] * b2_score +
            self.weights[12] * b3_score +
            self.weights[13] * c1_score +
            self.weights[14] * c2_score +
            self.weights[15] * c3_score
        )

        make_move(new_board, move, "X")

        three_corners_score = self.three_corners(new_board)
        two_adj_corners_score = self.two_adj_corners(new_board)
        two_opp_corners_score = self.two_opp_corners(new_board)
        one_corner_score = self.one_corner(new_board)
        middle_score = self.middle(new_board)
        two_in_a_row_edge_score = self.two_in_a_row_edge(new_board)
        two_in_a_row_middle_score = self.two_in_a_row_middle(new_board)
        a1_score = self.a1(new_board)
        a2_score = self.a2(new_board)
        a3_score = self.a3(new_board)
        b1_score = self.b1(new_board)
        b2_score = self.b2(new_board)
        b3_score = self.b3(new_board)
        c1_score = self.c1(new_board)
        c2_score = self.c2(new_board)
        c3_score = self.c3(new_board)
        final_score = (
            self.weights[0] * two_adj_corners_score +
            self.weights[1] * two_opp_corners_score +
            self.weights[2] * one_corner_score +
            self.weights[3] * middle_score +
            self.weights[4] * three_corners_score +
            self.weights[5] * two_in_a_row_edge_score +
            self.weights[6] * two_in_a_row_middle_score + 
            self.weights[7] * a1_score +
            self.weights[8] * a2_score +
            self.weights[9] * a3_score +
            self.weights[10] * b1_score +
            self.weights[11] * b2_score +
            self.weights[12] * b3_score +
            self.weights[13] * c1_score +
            self.weights[14] * c2_score +
            self.weights[15] * c3_score
        )

        return final_score - initial_score
    
    def num_corners_controlled(self, board):
        corners = [0, 2, 6, 8]
        return len([corner for corner in corners if board[corner] == "X"])
                
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
    
    def a1(self, board):
        return board[0] == "X"
    
    def a2(self, board):
        return board[1] == "X"
    
    def a3(self, board):
        return board[2] == "X"
    
    def b1(self, board):
        return board[3] == "X"
    
    def b2(self, board):
        return board[4] == "X"
    
    def b3(self, board):
        return board[5] == "X"
    
    def c1(self, board):
        return board[6] == "X"
    
    def c2(self, board):
        return board[7] == "X"
    
    def c3(self, board):
        return board[8] == "X"
