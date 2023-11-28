from src.game.base_game import BaseGame

import matplotlib.pyplot as plt
import numpy as np


class OthelloGame(BaseGame):
    BOARD_SIZE = 8

    # Bounds for the weights
    WEIGHTS_MIN = -1000
    WEIGHTS_MAX = +1000

    # Board pieces
    EMPTY = +0
    BLACK = +1
    WHITE = -1

    def __init__(self, game: str = ""):
        self.game = game
        self.board = np.full((self.BOARD_SIZE, self.BOARD_SIZE), self.EMPTY, dtype=int)
        self.board[3, 3] = self.WHITE
        self.board[3, 4] = self.BLACK
        self.board[4, 3] = self.BLACK
        self.board[4, 4] = self.WHITE
        self.player = self.BLACK
        self.weights = np.random.uniform(
            self.WEIGHTS_MIN, self.WEIGHTS_MAX, size=(self.BOARD_SIZE, self.BOARD_SIZE)
        )
        for i in range(0, len(game), 2):
            self.board = self.make_move(self.board, self.player, game[i : i + 2])
            self.player = -self.player
        self.valid_moves = self.get_valid_moves(self.board, self.player)

    def update_weights(self, weights: list[float]):
        self.weights = np.array(weights).reshape((self.BOARD_SIZE, self.BOARD_SIZE))

    def get_board_data(self):
        return self.game

    def get_best_move(self) -> tuple[int, int]:
        if not self.valid_moves:
            return None
        move_scores = [
            self.evaluate_board(
                self.make_move(self.board, self.player, move), self.player
            )
            for move in self.valid_moves
        ]
        best_move = self.valid_moves[np.argmax(move_scores)]
        return best_move

    def rank_move(self, move) -> tuple[int, int]:
        move_scores = [
            self.reference_score(
                self.make_move(self.board, self.player, move), self.player
            )
            for move in self.valid_moves
        ]
        valid_moves, move_scores = zip(
            *sorted(
                zip(self.valid_moves, move_scores), reverse=True, key=lambda x: x[1]
            )
        )
        index = valid_moves.index(move)
        return (index, len(valid_moves))

    def fitness(self) -> tuple[float, tuple[int, int], float]:
        score = 0
        best_score = -np.inf
        best_move = None
        valid_moves = self.get_valid_moves(self.board, self.player)
        if not valid_moves:
            return (score, (-1, -1), 0)
        for move in valid_moves:
            new_board = self.make_move(self.board, self.player, move)
            new_score = self.evaluate_board(new_board, self.player)
            ref_score = self.reference_score(new_board, self.player)
            if new_score > best_score:
                best_score = new_score
                best_move = move
            score += abs(new_score - ref_score)
        return (score / len(valid_moves), best_move, best_score)

    def get_weights(self) -> np.ndarray:
        return self.weights.flatten()

    def get_weight_bounds(self) -> list[tuple[int, int]]:
        return [
            (self.WEIGHTS_MIN, self.WEIGHTS_MAX) for _ in range(self.BOARD_SIZE**2)
        ]

    def get_weight_labels(self):
        letters = "ABCDEFGH"
        numbers = "12345678"
        return [f"{i}{j}" for i in numbers for j in letters]

    def visualize_best_move(self, img_size):
        our_best_move = self.get_best_move()
        ref_moves = [self.rank_move(move) for move in self.valid_moves]
        ref_best_move = min(zip(ref_moves, self.valid_moves), key=lambda x: x[0][0])[1]
        black_x, black_y = np.where(self.board == self.BLACK) 
        white_x, white_y = np.where(self.board == self.WHITE)
        plt.figure(figsize=(8,8))
        plt.gca().set_facecolor('green')
        plt.scatter(black_x+0.5, black_y+0.5, c='black', s=1000, marker='o')
        plt.scatter(white_x+0.5, white_y+0.5, c='white', s=1000, marker='o')
        plt.scatter(our_best_move[0]+0.5, our_best_move[1]+0.5, c='red', s=1000, marker='o')
        plt.scatter(ref_best_move[0]+0.5, ref_best_move[1]+0.5, c='blue', s=1000, marker='o')
        plt.grid(axis='x', color='k')
        plt.grid(axis='y', color='k')
        plt.xlim(0, 8)
        plt.ylim(0, 8)
        plt.title(f"Othello Game\n"
                  f"Our Best Move (red): {our_best_move}\n"
                  f"Reference Best Move (blue): {ref_best_move}", loc='left')
        plt.show()
        return

    def is_valid_move(
        self,
        board: np.ndarray,
        player: int,
        move: tuple[int, int],
        direction: tuple[int, int],
    ) -> bool:
        """
        Check if a move is legal by checking if there is an opponent's piece adjacent to the move
        and if there is a player's piece in the direction of the opponent's piece.
        """
        opponent = -player
        row, col = move
        r, c = row + direction[0], col + direction[1]

        # Check if the move is within bounds
        if not (0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE):
            return False

        # Check if there is an opponent's piece adjacent to the move
        if board[r, c] != opponent:
            return False

        # Continue in the direction until an empty space or the player's piece is found
        while (
            0 <= r < self.BOARD_SIZE
            and 0 <= c < self.BOARD_SIZE
            and board[r, c] == opponent
        ):
            r, c = r + direction[0], c + direction[1]

        # Check if the move is valid by ensuring a player's piece is found after opponent's pieces
        return (
            0 <= r < self.BOARD_SIZE
            and 0 <= c < self.BOARD_SIZE
            and board[r, c] == player
        )

    def get_valid_moves(self, board: np.ndarray, player: int) -> list[tuple[int, int]]:
        valid_moves = []
        directions = [
            (-1, +0),
            (+1, +0),
            (+0, -1),
            (+0, +1),
            (-1, -1),
            (-1, +1),
            (+1, -1),
            (+1, +1),
        ]
        for row in range(8):
            for col in range(8):
                if board[row, col] == self.EMPTY:  # Check empty positions
                    for direction in directions:
                        if self.is_valid_move(board, player, (row, col), direction):
                            valid_moves.append((row, col))
                            break
        return valid_moves

    def make_move(
        self, board: np.ndarray, player: int, move: tuple[int, int] | str
    ) -> np.ndarray:
        """
        Make a move on the board by flipping the opponent's pieces in the directions of the player's pieces.
        """
        board_copy = board.copy()
        if isinstance(move, str):
            move = (int(move[1]) - 1, ord(move[0]) - ord("A"))
        opponent = -player
        board_copy[move] = player
        directions = [
            (-1, +0),
            (+1, +0),
            (+0, -1),
            (+0, +1),
            (-1, -1),
            (-1, +1),
            (+1, -1),
            (+1, +1),
        ]
        for direction in directions:
            if self.is_valid_move(board_copy, player, move, direction):
                r, c = move
                r, c = r + direction[0], c + direction[1]
                while board_copy[r, c] == opponent:
                    board_copy[r, c] = player
                    r, c = r + direction[0], c + direction[1]
        return board_copy

    def evaluate_board(self, board: np.ndarray, player: int) -> float:
        return np.sum(board * self.weights * player)

    def reference_score(self, board: np.ndarray, player: int) -> float:
        # Based on https://www.csse.uwa.edu.au/cig08/Proceedings/papers/8010.pdf
        weight_initial = np.array(
            [
                [0, +0.00000, +0.00000, +0.00000, +0.00000, +0.00000, +0.00000, 0],
                [0, -0.02231, +0.05583, +0.02004, +0.02004, +0.05583, -0.02231, 0],
                [0, +0.05583, +0.10126, -0.10927, -0.10927, +0.10126, +0.05583, 0],
                [0, +0.02004, -0.10927, -0.10155, -0.10155, -0.10927, +0.02004, 0],
                [0, +0.02004, -0.10927, -0.10155, -0.10155, -0.10927, +0.02004, 0],
                [0, +0.05583, +0.10126, -0.10927, -0.10927, +0.10126, +0.05583, 0],
                [0, -0.02231, +0.05583, +0.02004, +0.02004, +0.05583, -0.02231, 0],
                [0, +0.00000, +0.00000, +0.00000, +0.00000, +0.00000, +0.00000, 0],
            ]  
        )
        weight_midgame = np.array(
            [
                [+6.32711, -3.32813, +0.33907, -2.00512, -2.00512, +0.33907, -3.32813, +6.32711],
                [-3.32813, -1.52928, -1.87550, -0.18176, -0.18176, -1.87550, -1.52928, -3.32813],
                [+0.33907, -1.87550, +1.06939, +0.62415, +0.62415, +1.06939, -1.87550, +0.33907],
                [-2.00512, -0.18176, +0.62415, +0.10539, +0.10539, +0.62415, -0.18176, -2.00512],
                [-2.00512, -0.18176, +0.62415, +0.10539, +0.10539, +0.62415, -0.18176, -2.00512],
                [+0.33907, -1.87550, +1.06939, +0.62415, +0.62415, +1.06939, -1.87550, +0.33907],
                [-3.32813, -1.52928, -1.87550, -0.18176, -0.18176, -1.87550, -1.52928, -3.32813],
                [+6.32711, -3.32813, +0.33907, -2.00512, -2.00512, +0.33907, -3.32813, +6.32711],
            ]
        )
        weight_endgame = np.array(
            [
                [+5.50062, -0.17812, -2.58948, -0.59007, -0.59007, -2.58948, -0.17812, +5.50062],
                [-0.17812, +0.96804, -2.16084, -2.01723, -2.01723, -2.16084, +0.96804, -0.17812],
                [-2.58948, -2.16084, +0.49062, -1.07055, -1.07055, +0.49062, -2.16084, -2.58948],
                [-0.59007, -2.01723, -1.07055, +0.73486, +0.73486, -1.07055, -2.01723, -0.59007],
                [-0.59007, -2.01723, -1.07055, +0.73486, +0.73486, -1.07055, -2.01723, -0.59007],
                [-2.58948, -2.16084, +0.49062, -1.07055, -1.07055, +0.49062, -2.16084, -2.58948],
                [-0.17812, +0.96804, -2.16084, -2.01723, -2.01723, -2.16084, +0.96804, -0.17812],
                [+5.50062, -0.17812, -2.58948, -0.59007, -0.59007, -2.58948, -0.17812, +5.50062],
            ]
        )
        n_corner_occupied = np.sum(board[[0, 0, -1, -1], [0, -1, 0, -1]] != self.EMPTY)
        if n_corner_occupied == 0:
            return np.sum(board * weight_initial * player)
        elif n_corner_occupied == 1:
            return np.sum(board * weight_midgame * player)
        else:
            return np.sum(board * weight_endgame * player)
        
    def __str__(self):
        board_str = ""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row, col] == self.EMPTY:
                    board_str += "."
                elif self.board[row, col] == self.BLACK:
                    board_str += "B"
                elif self.board[row, col] == self.WHITE:
                    board_str += "W"
            board_str += "\n"
        return board_str
