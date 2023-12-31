import time
import random
import chess

from tqdm import tqdm
from chess import engine, pgn

# Evaluate the score of every legal move (and get the next best move)
def stockfish_evaluation(board):
    two_ply_moves = 8

    engine = chess.engine.SimpleEngine.popen_uci("./stockfish")
    move_sequences = {}
    total_moves = len(list(board.legal_moves))
    best_moves_ascending = []

    # Use tqdm for the loop with additional information
    for move in tqdm(board.legal_moves, desc="Evaluating Moves", unit="move", total=total_moves, position=1, unit_scale=True):
        # Find the next two moves and evaluate the score
        principle_moveset = []
        score = None
        time_to_find_moveset = 1
        
        while len(principle_moveset) < two_ply_moves * 2:
            info = engine.analyse(board, chess.engine.Limit(time=time_to_find_moveset, depth=20), root_moves=[move])
            principle_moveset = info['pv']
            score = info['score']
            time_to_find_moveset += 0.1

            if time_to_find_moveset > 5:
                print(f"Time to find moveset exceeded 5 seconds. Breaking.")
                return (None, None)

        move_sequences[move.uci()] = {
            'score': info['score'],
            # Get the first depth number of moves in the principle variation
            'next_moves': info['pv'][:two_ply_moves * 2]
        }

        # Add the move to the ranked moves list
        best_moves_ascending.append((move, score))

    #print(f"Move Sequences: {move_sequences}")
    engine.quit()

    # Sort the moves by score
    best_moves_ascending.sort(key=lambda x: x[1].relative.score(mate_score=2000), reverse=chess.WHITE)

    move_sequences['stockfish'] = {
        'score': best_moves_ascending[0][1],
        'move': best_moves_ascending[0][0],
    }

    ranked_moves = {}
    rank = 1
    for move, score in best_moves_ascending:
        ranked_moves[move.uci()] = rank
        rank += 1

    #print(f"Ranked Moves: {ranked_moves}")
    #print(f"Best Moves: {best_moves_ascending}")
    return (move_sequences, ranked_moves)

def load_games():
    games = []
    with open('./src/utility/master_games.pgn') as file:
        while True:
            game = chess.pgn.read_game(file)
            if game is None:
                break
            games.append(game)
    
    return games

def extract_random_chess_positions(num_positions, seed=None):
    # Load the games from the PGN file
    games = load_games()

    board_data = []
    # Extract random positions
    for _ in range(num_positions):
        # Choose a random game
        if seed is None:
            seed = random.randint(0, 1000000)
        
        print(f"Seed used: {seed}")
        random.seed(seed)

        random_game = random.choice(games)
        #print(f"Game: {random_game.headers['Event']}")

        #print(f"PGN Used: {random_game}")

        # Traverse the game to a random position
        board = random_game.board()
        board_moves = list(random_game.mainline_moves())

        total_moves = 1
        num_moves_to_traverse = random.randint(40, len(board_moves) - 40)
        for _ in range(num_moves_to_traverse):
            move = board_moves.pop(0)
            board.push(move)
            total_moves += 1

        #print(f"Final Ply: {(total_moves//2)}\n")
        (move_sequences, ranked_moves) = stockfish_evaluation(board)

        if move_sequences is None or ranked_moves is None:
            return extract_random_chess_positions(num_positions, seed=seed+1)

        # Output information about the current position
        # print(f"Game: {random_game.headers['Event']}")
        # print(f"Position: {board.fen()}")
        # print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        # print(f"Next Move (IN EXTRACTION): {board_moves[0] if board_moves else 'Game Over'}\n")
        board_data.append((board, board_moves, move_sequences, ranked_moves, {}))


    return board_data
