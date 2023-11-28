import math
import time
import random

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
        original_board_copy = list(original_board)
        make_move(board, possible_move, player)

        sim_score = minimax(board, other_player, max_player, original_board_copy)

        undo_move(board, possible_move)
        moves_and_scores.append((possible_move, sim_score['score']))
        #print("sim_score: {}".format(sim_score))
        #print(moves_and_scores)

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
    return [i for i, spot in enumerate(board) if spot == " " or spot == ""]

def undo_move(board, possible_move):
    board[possible_move] = ""

def make_move(board, possible_move, player):
    board[possible_move] = player


def check_winner(board):
    # Check conditions for X and O
    x_conditions = [
        (board[0] == board[1] == board[2] == "X"),
        (board[3] == board[4] == board[5] == "X"),
        (board[6] == board[7] == board[8] == "X"),
        (board[0] == board[3] == board[6] == "X"),
        (board[1] == board[4] == board[7] == "X"),
        (board[2] == board[5] == board[8] == "X"),
        (board[0] == board[4] == board[8] == "X"),
        (board[2] == board[4] == board[6] == "X"),
    ]

    o_conditions = [
        (board[0] == board[1] == board[2] == "O"),
        (board[3] == board[4] == board[5] == "O"),
        (board[6] == board[7] == board[8] == "O"),
        (board[0] == board[3] == board[6] == "O"),
        (board[1] == board[4] == board[7] == "O"),
        (board[2] == board[5] == board[8] == "O"),
        (board[0] == board[4] == board[8] == "O"),
        (board[2] == board[4] == board[6] == "O"),
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
        board = [item.replace('\n', ' ').strip() if item.strip() != '' else ' ' for item in  random.choice(games).split(",")]
        #board = ['O', ' ', ' ', ' ', ' ', 'O', ' ', ' ', 'X']
        moves_and_scores = minimax(board, player="X", max_player="X", original_board=board)
        board_data.append((board, moves_and_scores))

    return board_data
