import chess
import chess.pgn
import chess.engine
import random
from tqdm import tqdm
import time

# Evaluate the score of every legal move (and get the next best move)
def stockfish_evaluation(board):
    two_ply_moves = 1

    engine = chess.engine.SimpleEngine.popen_uci("./stockfish")
    move_sequences = {}
    total_moves = len(list(board.legal_moves))

    starting_info = engine.analyse(board, chess.engine.Limit(time=1))
    move_sequences['stockfish'] = {
        'score': starting_info['score'],
        'move': starting_info['pv'][0]
    }

    best_moves_ascending = []

    # Use tqdm for the loop with additional information
    for move in tqdm(board.legal_moves, desc="Evaluating Moves", unit="move", total=total_moves, position=1, unit_scale=True):
        # Find the next two moves and evaluate the score
        principle_moveset = []
        score = None
        time_to_find_moveset = 0.1
        
        while len(principle_moveset) < two_ply_moves * 2:
            info = engine.analyse(board, chess.engine.Limit(time=0.1), root_moves=[move])
            principle_moveset = info['pv']
            score = info['score']
            time_to_find_moveset += 0.1

        move_sequences[move.uci()] = {
            'score': info['score'],
            # Get the first depth number of moves in the principle variation
            'next_moves': info['pv'][:two_ply_moves * 2]
        }

        # Add the move to the ranked moves list
        best_moves_ascending.append((move, score))

    print(f"Move Sequences: {move_sequences}")
    engine.quit()

    # Sort the moves by score
    best_moves_ascending.sort(key=lambda x: x[1].relative.score(mate_score=2000), reverse=board.turn)

    ranked_moves = {}
    rank = 1
    for move, score in best_moves_ascending:
        ranked_moves[move.uci()] = rank
        rank += 1

    print(f"Ranked Moves: {ranked_moves}")
    print(f"Best Moves: {best_moves_ascending}")
    return (move_sequences, ranked_moves)

def extract_random_chess_positions(num_positions, seed=None):
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
        if seed is None:
            seed = random.randint(0, 1000000)
        
        print(f"Seed used: {seed}")
        random.seed(seed)

        random_game = random.choice(games)
        print(f"Game: {random_game.headers['Event']}")

        # Traverse the game to a random position
        board = random_game.board()
        board_moves = list(random_game.mainline_moves())
        for _ in range(random.randint(4, len(board_moves) - 6)):
            move = board_moves.pop(0)
            board.push(move)

        move_sequences, ranked_moves = stockfish_evaluation(board)

        # Output information about the current position
        # print(f"Game: {random_game.headers['Event']}")
        # print(f"Position: {board.fen()}")
        # print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        # print(f"Next Move (IN EXTRACTION): {board_moves[0] if board_moves else 'Game Over'}\n")
        board_data.append((board, board_moves, move_sequences, ranked_moves, {}))


    return board_data