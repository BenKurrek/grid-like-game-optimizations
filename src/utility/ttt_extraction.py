import math
import time
import random

from tqdm import tqdm
from chess import engine, pgn

def minimax(board, player, max_player, original_board):
    maxplayer = "X"
    other_player = 'O' if player == 'X' else 'X'

    winner = check_winner(board)
    empties = available_moves(board)

    # Base cases
    if winner == other_player:
        return {'position': None, 'score': 1 * (len(empties) + 1) if other_player == max_player else -1 * (
                    len(empties) + 1)}
    elif not empties:
        return {'position': None, 'score': 0}

    if player == max_player:
        best = {'position': None, 'score': -math.inf}  # each score should maximize
    else:
        best = {'position': None, 'score': math.inf}  # each score should minimize

    # List to store [(move, cumulative_score)] for each move
    moves_and_scores = []

    for possible_move in available_moves(board):
        # Assume you have a function make_move(board, move, player) that makes a move on the board.
        # Implement this function as per your existing code.
        make_move(board, possible_move, player)

        sim_score = minimax(board, other_player, max_player, original_board)
        
        # Assume you have a function undo_move(board, move) that undoes a move on the board.
        # Implement this function as per your existing code.
        undo_move(board, possible_move)

        sim_score['position'] = possible_move  # this represents the move optimal next move
        moves_and_scores.append((possible_move, sim_score['score']))

        if player == max_player:  # X is max player
            if sim_score['score'] > best['score']:
                best = sim_score
        else:
            if sim_score['score'] < best['score']:
                best = sim_score

    if board == original_board:  # Only return moves_and_scores for the initial function call
        return moves_and_scores
    else:
        return best

def available_moves(board):
    # empties = []
    # idx = 0
    # for square in board:
    #     if square == "" or square == " ":
    #         empties.push(idx)
    #     idx += 1
    # return empties
    return [i for i, spot in enumerate(board) if spot == " " or spot == ""]

def undo_move(board, possible_move):
    board[possible_move] = ""

def make_move(board, possible_move, player):
    board[possible_move] = player


def check_winner(board):
    # Check conditions for X and O
    x_conditions = [
        not (board[0] == board[1] == board[2] == "X"),
        not (board[3] == board[4] == board[5] == "X"),
        not (board[6] == board[7] == board[8] == "X"),
        not (board[0] == board[3] == board[6] == "X"),
        not (board[1] == board[4] == board[7] == "X"),
        not (board[2] == board[5] == board[8] == "X"),
        not (board[0] == board[4] == board[8] == "X"),
        not (board[2] == board[4] == board[6] == "X"),
    ]

    o_conditions = [
        not (board[0] == board[1] == board[2] == "O"),
        not (board[3] == board[4] == board[5] == "O"),
        not (board[6] == board[7] == board[8] == "O"),
        not (board[0] == board[3] == board[6] == "O"),
        not (board[1] == board[4] == board[7] == "O"),
        not (board[2] == board[5] == board[8] == "O"),
        not (board[0] == board[4] == board[8] == "O"),
        not (board[2] == board[4] == board[6] == "O"),
    ]

    if any(x_conditions):
        return "X"
    elif any(o_conditions):
        return "O"
    else:
        return None

def extract_random_ttt_positions(num_positions):
    # Load the games from the PGN file
    games = []
    with open("src/utility/ttt_all_incomplete_board_states.csv", "r") as file:
        games = file.readlines()

    board_data = []
    # Extract random positions
    for _ in range(num_positions):
        # Choose a random game, currently represented as a line in a csv file
        board = random.choice(games).split(",")
        # return list of all possible next moves and their cumulative scores
        [(move, cumulative_score)] = minimax(board, "X", "X", board)

        # Output information about the current position
        # print(f"Game: {random_game.headers['Event']}")
        # print(f"Position: {board.fen()}")
        # print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        # print(f"Next Move (IN EXTRACTION): {board_moves[0] if board_moves else 'Game Over'}\n")
        board_data.append((board, [(move, cumulative_score)]))

    return board_data