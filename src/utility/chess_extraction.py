import chess
import chess.pgn
import chess.engine
import random
from tqdm import tqdm
import time

# Evaluate the score of every legal move
def stockfish_evaluation(board):
    engine = chess.engine.SimpleEngine.popen_uci("./stockfish")
    scores = {}
    total_moves = len(list(board.legal_moves))

    # Use tqdm for the loop with additional information
    for move in tqdm(board.legal_moves, desc="Evaluating Moves", unit="move", total=total_moves, position=1, unit_scale=True):
        info = engine.analyse(board, chess.engine.Limit(time=0.001), root_moves=[move])
        scores[move.uci()] = info['score']
    engine.quit()
    
    return scores

def extract_random_chess_positions(num_positions):
    # Load the games from the PGN file
    games = []
    with open('./src/utility/master_games.pgn') as file:
        while True:
            game = chess.pgn.read_game(file)
            if game is None:
                break
            games.append(game)

    board_data = []
    # Extract random positions
    for _ in range(num_positions):
        # Choose a random game
        random_game = random.choice(games)

        # Traverse the game to a random position
        board = random_game.board()
        board_moves = list(random_game.mainline_moves())
        for _ in range(random.randint(10, len(board_moves))):
            move = board_moves.pop(0)
            board.push(move)

        scores = stockfish_evaluation(board)

        # Output information about the current position
        # print(f"Game: {random_game.headers['Event']}")
        # print(f"Position: {board.fen()}")
        # print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        # print(f"Next Move (IN EXTRACTION): {board_moves[0] if board_moves else 'Game Over'}\n")
        board_data.append((board, board_moves, scores))

    return board_data