import math
import time
import random

# def minimax(board, player, max_player, original_board, cumulative_scores, last_moves:list):
#     maxplayer = "X"
#     other_player = 'O' if player == 'X' else 'X'

#     winner = check_winner(board)
#     empties = available_moves(board)

#     # Base cases
#     if winner == other_player:
#         if other_player == max_player:
#             print("Winner is X with a score of {}".format(1 * (len(empties) + 1)))
#             index = next((i for i, tpl in enumerate(cumulative_scores) if tpl[0] == last_moves[-1]), None)
#             print("Current Score: {}".format(cumulative_scores[index]))
#             cumulative_scores[index][1] += 1 * (len(empties) + 1)
#             print("Updated Score: {}".format(cumulative_scores[index]))
#             print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#             return {'position': last_moves[-1], 'score': 1 * (len(empties) + 1)}
#         else:
#             print("Winner is O with a score of {}".format(-1 * (len(empties) + 1)))
#             index = next((i for i, tpl in enumerate(cumulative_scores) if tpl[0] == last_moves[-1]), None)
#             print("Current Score: {}".format(cumulative_scores[index]))
#             cumulative_scores[index][1] += -1 * (len(empties) + 1)
#             print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#             return {'position': last_moves[-1], 'score': -1 * (len(empties) + 1)}
#     elif not empties:
#         #print("stalemate")
#         return {'position': last_moves[-1], 'score': 0}

#     if player == max_player:
#         best = {'position': None, 'score': -math.inf}  # each score should maximize
#     else:
#         best = {'position': None, 'score': math.inf}  # each score should minimize

#     # List to store [(move, cumulative_score)] for each move
#     moves_and_scores = []

#     for possible_move in available_moves(board):
#         # Store the original state of the board
#         original_board_copy = list(original_board)
#         # Assume you have a function make_move(board, move, player) that makes a move on the board.
#         # Implement this function as per your existing code.
#         make_move(board, possible_move, player)
#         print("made move {}".format(possible_move))
#         print(last_moves)
#         if len(last_moves) == 0:
#             last_moves = [possible_move]
#         else:
#             last_moves.append(possible_move)

    
#         sim_score = minimax(board, other_player, max_player, original_board_copy, cumulative_scores, last_moves)
#         # if sim_score['position'] is not None:
#         #     index = next((i for i, tpl in enumerate(cumulative_scores) if tpl[0] == sim_score['position']), None)
#         #     print("starting cumulative scores: {}".format(cumulative_scores[index]))
#         #     print("to be added: {}".format(sim_score))
#         #     cumulative_scores[index][1] += sim_score['score']
#         #     print(cumulative_scores)
#         # print(sim_score)
        
#         # Assume you have a function undo_move(board, move) that undoes a move on the board.
#         # Implement this function as per your existing code.

#         print("undoing move {}".format(possible_move))
#         undo_move(board, possible_move)
#         last_moves.pop()

#         sim_score['position'] = possible_move  # this represents the move optimal next move
        
#         moves_and_scores.append(cumulative_scores)

#         if player == max_player:  # X is max player
#             if sim_score['score'] > best['score']:
#                 best = sim_score
#         else:
#             if sim_score['score'] < best['score']:
#                 best = sim_score

#         #print("Moving onto next first move")

#     if board == original_board:  # Only return moves_and_scores for the initial function call
#         return cumulative_scores
#     else:
#         return best

# def minimax(board, player, max_player, original_board, cumulative_scores, possible_move):
#     maxplayer = "X"
#     other_player = 'O' if player == 'X' else 'X'

#     winner = check_winner(board)
#     empties = available_moves(board)

#     # Base cases
#     if winner == other_player:
#         if other_player == max_player:
#             return {'position': None, 'score': 1 * (len(empties) + 1)}
#         else:
#             return {'position': None, 'score': -1 * (len(empties) + 1)}
#     elif not empties:
#         #print("stalemate")
#         return {'position': None, 'score': 0}

#     if player == max_player:
#         best = {'position': None, 'score': -math.inf}  # each score should maximize
#     else:
#         best = {'position': None, 'score': math.inf}  # each score should minimize

#     # List to store [(move, cumulative_score)] for each move
#     moves_and_scores = []

#     for possible_move in available_moves(board):
#         # Store the original state of the board
#         original_board_copy = list(original_board)
#         # Assume you have a function make_move(board, move, player) that makes a move on the board.
#         # Implement this function as per your existing code.
#         make_move(board, possible_move, player)
#         print("made move {}".format(possible_move))
    
#         sim_score = minimax(board, other_player, max_player, original_board_copy, cumulative_scores, possible_move)
#         # if sim_score['position'] is not None:
#         #     index = next((i for i, tpl in enumerate(cumulative_scores) if tpl[0] == sim_score['position']), None)
#         #     print("starting cumulative scores: {}".format(cumulative_scores[index]))
#         #     print("to be added: {}".format(sim_score))
#         #     cumulative_scores[index][1] += sim_score['score']
#         #     print(cumulative_scores)
#         # print(sim_score)
        
#         # Assume you have a function undo_move(board, move) that undoes a move on the board.
#         # Implement this function as per your existing code.

#         print("undoing move {}".format(possible_move))
#         undo_move(board, possible_move)

#         sim_score['position'] = possible_move  # this represents the move optimal next move
        
#         moves_and_scores.append(cumulative_scores)

#         if player == max_player:  # X is max player
#             if sim_score['score'] > best['score']:
#                 best = sim_score
#         else:
#             if sim_score['score'] < best['score']:
#                 best = sim_score

#         #print("Moving onto next first move")

#     if board == original_board:  # Only return moves_and_scores for the initial function call
#         return cumulative_scores
#     else:
#         return best

# def minimax_wrapper(board, player, max_player, original_board):
#     next_moves_and_scores = []

#     for possible_moves in available_moves(board):
#         print("Analyzing after move {}".format(possible_moves))
#         make_move(board, possible_moves, player)
#         score_for_move = minimax(board, player, max_player, original_board, 0)
#         next_moves_and_scores.append((possible_moves, score_for_move))
#         undo_move(board, possible_moves)
    
#     print(next_moves_and_scores)
#     return next_moves_and_scores

# WORKING ISH VERSION, NO CUMULATIVE
def minimax(board, player, max_player, original_board):
    maxplayer = "X"
    other_player = 'O' if player == 'X' else 'X'

    winner = check_winner(board)
    empties = available_moves(board)

    # Base cases
    if winner == other_player:
        # if winner == max_player:
        #     print("Winner is X with a score of {}".format(1 * (len(empties) + 1)))
        #     print(board)
        #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #     return {'position': None, 'score': 1 * (len(empties) + 1)}
        # else:
        #     print("Winner is O with a score of {}".format(-1 * (len(empties) + 1)))
        #     print(board)
        #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #     return {'position': None, 'score': -1 * (len(empties) + 1)}
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

        original_board_copy = list(original_board)
        make_move(board, possible_move, player)


        sim_score = minimax(board, other_player, max_player, original_board_copy)
        # if sim_score['position'] is None:
        #     total_count += sim_score['score']
            
        
        # Assume you have a function undo_move(board, move) that undoes a move on the board.
        # Implement this function as per your existing code.
        undo_move(board, possible_move)
        moves_and_scores.append((possible_move, sim_score['score']))
        print("sim_score: {}".format(sim_score))

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


# def minimax(board, player, max_player, original_board, cumulative_scores=None):
#     if cumulative_scores is None:
#         cumulative_scores = []

#     maxplayer = "X"
#     other_player = 'O' if player == 'X' else 'X'

#     winner = check_winner(board)
#     empties = available_moves(board)

#     # Base cases
#     if winner == other_player:
#         score = 1 * (len(empties) + 1) if other_player == max_player else -1 * (len(empties) + 1)
#         return {'position': None, 'score': score}
#     elif not empties:
#         return {'position': None, 'score': 0}

#     if player == max_player:
#         best = {'position': None, 'score': -math.inf}  # each score should maximize
#     else:
#         best = {'position': None, 'score': math.inf}  # each score should minimize

#     # List to store [(move, cumulative_score)] for each move
#     moves_and_scores = []

#     for possible_move in empties:
#         original_board_copy = list(original_board)
#         make_move(board, possible_move, player)

#         cumulative_scores_for_move = list(cumulative_scores)
#         sim_score = minimax(board, other_player, max_player, original_board_copy, cumulative_scores_for_move)

#         undo_move(board, possible_move)

#         sim_score['position'] = possible_move  # this represents the move optimal next move

#         cumulative_score = sim_score['score'] + cumulative_scores_for_move[-1][1] if cumulative_scores_for_move else sim_score['score']
#         cumulative_scores_for_move = cumulative_scores_for_move[:-1] + [(possible_move, cumulative_score)]
#   # Update the cumulative score for the current move

#         cumulative_scores.extend(cumulative_scores_for_move)

#         if player == max_player:  # X is max player
#             if cumulative_score > best['score']:
#                 best = sim_score
#         else:
#             if cumulative_score < best['score']:
#                 best = sim_score

#         moves_and_scores.append((possible_move, cumulative_score))

#     if board == original_board:  # Only return moves_and_scores for the initial function call
#         return moves_and_scores
#     else:
#         return best

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
        #board = [item.replace('\n', ' ').strip() if item.strip() != '' else ' ' for item in  random.choice(games).split(",")]
        board = ['', 'O', 'X', 'O', 'O', 'X', 'X', '', '']
        print(board)
        empties = available_moves(board)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        cumulative_scores = [list([x, 0]) for x in empties]
        # return list of all possible next moves and their cumulative scores
        moves_and_scores = minimax(board, player="X", max_player="X", original_board=board)
        #, cumulative_scores={}
        board_data.append((board, moves_and_scores))
    
    print("[[0, -2], [7, 1]], [8, 3]")
    return board_data


# made move 0
# made move 7
# {'position': None, 'score': -2}
# undoing move 7
# made move 8
# made move 7
# {'position': None, 'score': 0}
# undoing move 7
# {'position': 7, 'score': 0}
# undoing move 8
# {'position': 7, 'score': -2}
# undoing move 0

# made move 7
# made move 0
# made move 8
# {'position': None, 'score': 1}
# undoing move 8
# {'position': 8, 'score': 1}
# undoing move 0
# made move 8
# made move 0
# {'position': None, 'score': 0}
# undoing move 0
# {'position': 0, 'score': 0}
# undoing move 8
# {'position': 8, 'score': 0}
# undoing move 7

# made move 8
# {'position': None, 'score': 3}
# undoing move 8