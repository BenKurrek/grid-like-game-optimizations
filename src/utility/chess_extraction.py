import chess
import chess.pgn
import random

def extract_random_positions(num_positions=5):
    # Load the games from the PGN file
    games = []
    with open('./src/utility/master_games.pgn') as file:
        while True:
            game = chess.pgn.read_game(file)
            if game is None:
                break
            games.append(game)

    boards = []
    # Extract random positions
    for _ in range(num_positions):
        # Choose a random game
        random_game = random.choice(games)

        # Traverse the game to a random position
        board = random_game.board()
        random_moves = list(random_game.mainline_moves())
        for _ in range(random.randint(1, len(random_moves))):
            move = random_moves.pop(0)
            board.push(move)

        boards.append(board)

        # # Output information about the current position
        # print(f"Game: {random_game.headers['Event']}")
        # print(f"Position: {board.fen()}")
        # print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        # print(f"Next Move: {random_moves[0] if random_moves else 'Game Over'}\n")

    return boards