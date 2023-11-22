from src.game.base_game import BaseGame

import numpy as np

BOARD_SIZE = 8

# Board pieces
EMPTY = +0
BLACK = +1
WHITE = -1

# Game phases
INI = 0  # 0 corner occupied
MID = 1  # 1 corner occupied
END = 2  # 2+ corners occupied

# Evaluation weights for Othello (initialized to 0)
weights_min, weights_max = -1000, 1000
weights_ini = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE), dtype=float)
weights_mid = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE), dtype=float)
weights_end = np.zeros(shape=(BOARD_SIZE, BOARD_SIZE), dtype=float)

class OthelloGame(BaseGame):

    def __init__(self, game):
        self.game = game
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), EMPTY, dtype=int)
        self.board[3][3] = WHITE
        self.board[3][4] = BLACK
        self.board[4][3] = BLACK
        self.board[4][4] = WHITE
        self.turn = BLACK
        self.phase = INI
        
    def update_weights(self, weights):
        self.game.update_weights(weights)
    
    def get_best_move(self):
        return self.game.get_best_move()

    def rank_move(self, move):
        return self.game.rank_move(move)
    
    def set_random_state(self):
        return self.game.set_random_state()

    def fitness(self):
        return self.game.fitness()

    def mutate(self):
        return self.game.mutate()

    def crossover(self, game2):
        return BaseGame(self.game.crossover(game2))

    def get_weights(self) -> np.ndarray:
        """
        Returns the weights of the game.  
        """
        if self.phase == INI:
            return weights_ini
        elif self.phase == MID:
            return weights_mid
        elif self.phase == END:
            return weights_end
        else:
            raise ValueError("Invalid phase")
    
    def get_weight_labels(self):
        return self.game.get_weight_labels()

    def visualize_best_move(self, size):
        best_move = self.game.get_best_move()
        return self.game.visualize_best_move(best_move, size)
    
    def get_board(self) -> np.ndarray:
        return self.board
    
    def get_legal_moves(self) -> list[tuple[int, int]]:
        legal_moves = []
        return legal_moves