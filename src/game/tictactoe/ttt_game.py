# src/game/chess.py
import math
import chess
import chess.svg
import random
from src.game.base_game import BaseGame
from src.utility.ttt_extraction import available_moves, make_move, undo_move, check_winner, minimax
from itertools import permutations
import json

# *************** Game State Based Evaluation ***************
# Note: pure square based evaluation is available below.
weight_labels = [
    # board states
    "corners-controlled",
    "middle-controlled",
    "two-in-a-row",

    # move types
    "winning-move",
    "blocking-win",
    "forking-move", # creating a fork (3 adjacent corners)
    "blocking-fork", # block opponent fork creation
    "creating-fork-for-next-move", # two adjacent corners, create opportunity to create a fork next turn
]
weight_bounds = [
    (-10, 10), # corners-controlled
    (-10, 10), # middle-controlled
    (-10, 10), # two-in-a-row
    (-10, 10), # winning-move
    (-10, 10), # blocking-win
    (-10, 10), # forking-move
    (-10, 10), # blocking-fork
    (-10, 10), # creating-fork-for-next-move
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
            # evaluated_score measures how much board has improved, higher = better according to weights
            evaluated_score = self.evaluate_move(move)
            
            minimax_score = 0
            for v in self.moves_and_scores:
                if v[0] == move:
                    minimax_score = v[1]          
            
            if evaluated_score > best_score:
                best_move = move
                best_score = evaluated_score
            
            score -= abs(minimax_score - evaluated_score)

        # TODO: Confirm with Ben that this is the correct way to calculate score and fitness
        # TODO: Merge chess fix
        # genetic algorithm is looking for maximum score, this is driving the score down when there is a difference between minimax and evaluated
        return (score/len(avail_moves), best_move, best_score)
    
    def evaluate_move(self, move):
        new_board = self.board.copy()
        old_board = self.board.copy()
        make_move(new_board, move, "X")
        
        num_corner_score = self.num_corners_controlled(old_board, "X")
        two_in_a_row_score = self.two_in_a_row(old_board)
        middle_score = self.middle(old_board)

        initial_score = (
            self.weights[0] * num_corner_score +
            self.weights[1] * two_in_a_row_score +
            self.weights[2] * middle_score 
        )

        num_corner_score = self.num_corners_controlled(new_board, "X")
        two_in_a_row_score = self.two_in_a_row(new_board)
        middle_score = self.middle(new_board)
        winning_move = self.winning_move(new_board, move)
        blocking_win = self.blocking_win(new_board, move)
        forking_move = self.forking_move(new_board, move)
        blocking_fork = self.blocking_fork(new_board, move)
        creating_fork_for_next_move = self.creating_fork_for_next_move(new_board, move)


        final_score = (
            self.weights[0] * num_corner_score +
            self.weights[1] * two_in_a_row_score +
            self.weights[2] * middle_score + 
            self.weights[3] * winning_move +
            self.weights[4] * blocking_win +
            self.weights[5] * forking_move +
            self.weights[6] * blocking_fork +
            self.weights[7] * creating_fork_for_next_move
        )

        
        return final_score - initial_score
    
    # ~~~~~~~~~~~~~~~ BOARD STATES ~~~~~~~~~~~~~~~
    # These evaluations are done on the board both before and after the move
    def num_corners_controlled(self, board, player):
        conditions = [0, 2, 6, 8]
        return len([corner for corner in conditions if board[corner] == player])
    
    def two_in_a_row(self, board):
        conditions = [(0, 1), (1, 2), (0, 3), (2, 5), (3, 6), (5, 8), (6, 7), (7, 8), (1, 4), (3, 4), (4, 5), (4, 7)]
        return len([two_in_a_row for two_in_a_row in conditions if board[two_in_a_row[0]] == "X" and board[two_in_a_row[1]] == "X"])
    
    def middle(self, board):
        return board[4] == "X"
    
    # ~~~~~~~~~~~~~~~ MOVE CLASSIFICATION ~~~~~~~~~~~~~~~
    # When necessary, these functions will be given old and new boards to compute
    def winning_move(self, new_board, move):
        if check_winner(new_board) == "X":
            undo_move(new_board, move)
            if check_winner(new_board) is None:
                make_move(new_board, move, "X")
                return True
            make_move(new_board, move, "X")
        
        return False
    
    def blocking_win(self, new_board, move):
        # only evaluate if 0 is prevented from winning
        if check_winner(new_board) is None or check_winner(new_board) == "X":
            undo_move(new_board, move)
            make_move(new_board, move, "O")
            if check_winner(new_board) == "O":
                undo_move(new_board, move)
                make_move(new_board, move, "X")
                return True
            else:
                undo_move(new_board, move)
                make_move(new_board, move, "X")
                return False
            
        return False
    
    def forking_move(self, new_board, move):
        fork_conditions = [(0, 2, 6), (2, 6, 8), (0, 2, 8), (0, 6, 8)]
        corners = [0, 2, 6, 8]
        if move not in corners:
            return False
        # If fork exists, remove move and make sure fork did not exist prior to it
        if any(new_board[a] == new_board[b] == new_board[c] == "X" for a, b, c in fork_conditions):
            undo_move(new_board, move)
            if not any(new_board[a] == new_board[b] == new_board[c] == "X" for a, b, c in fork_conditions):
                make_move(new_board, move, "X")
                return True
            else:
                make_move(new_board, move, "X")
                return False
            
        return False
    
    def blocking_fork(self, new_board, move):
        fork_conditions = [(0, 2, 6), (2, 6, 8), (0, 2, 8), (0, 6, 8)]
        corners = [0, 2, 6, 8]
        if move not in corners:
            return False
        # Place 0 where latest move occured, if fork exists, then move made blocked a fork
        undo_move(new_board, move)
        make_move(new_board, move, "0")
        if any(new_board[a] == new_board[b] == new_board[c] == "O" for a, b, c in fork_conditions):
            undo_move(new_board, move)
            make_move(new_board, move, "X")
            return True
        else:
            undo_move(new_board, move)
            make_move(new_board, move, "X")
            return False
        

    def creating_fork_for_next_move(self, new_board, move):
        fork_conditions = [(0, 2, 6), (2, 6, 8), (0, 2, 8), (0, 6, 8)]
        corners = [0, 2, 6, 8]
        if move not in corners:
            return False
        
        # If O controls 1 or less corners and X now controls 2 corners after the move, then move creates a fork for next move
        return self.num_corners_controlled(new_board, "O") <= 1 and self.num_corners_controlled(new_board, "X") == 2
            

    # ****************** SQUARE BASED EVALUATION ******************
    # weight_labels = [
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

    # def evaluate_move(self, move):
    #     new_board = self.board.copy()
    #     old_board = self.board.copy()


        
    #     initial_score = (
    #         self.weights[0] * self.a1(old_board) +
    #         self.weights[1] * self.a2(old_board) +
    #         self.weights[2] * self.a3(old_board) +
    #         self.weights[3] * self.b1(old_board) +
    #         self.weights[4] * self.b2(old_board) +
    #         self.weights[5] * self.b3(old_board) +
    #         self.weights[6] * self.c1(old_board) +
    #         self.weights[7] * self.c2(old_board) +
    #         self.weights[8] * self.c3(old_board)
    #     )

    #     make_move(new_board, move, "X")

    #     final_score = (
    #         self.weights[0] * self.a1(new_board) +
    #         self.weights[1] * self.a2(new_board) +
    #         self.weights[2] * self.a3(new_board) +
    #         self.weights[3] * self.b1(new_board) +
    #         self.weights[4] * self.b2(new_board) +
    #         self.weights[5] * self.b3(new_board) +
    #         self.weights[6] * self.c1(new_board) +
    #         self.weights[7] * self.c2(new_board) +
    #         self.weights[8] * self.c3(new_board)
    #     )

    #     return final_score - initial_score

        
    # def a1(self, board):
    #     return board[0] == "X"
    
    # def a2(self, board):
    #     return board[1] == "X"
    
    # def a3(self, board):
    #     return board[2] == "X"
    
    # def b1(self, board):
    #     return board[3] == "X"
    
    # def b2(self, board):
    #     return board[4] == "X"
    
    # def b3(self, board):
    #     return board[5] == "X"
    
    # def c1(self, board):
    #     return board[6] == "X"
    
    # def c2(self, board):
    #     return board[7] == "X"
    
    # def c3(self, board):
    #     return board[8] == "X"
    



        

    



