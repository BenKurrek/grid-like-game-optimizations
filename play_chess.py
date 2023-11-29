import chess
import chess.pgn
import chess.engine
from tqdm import tqdm
import time
from src.game.chess.chess_game import ChessGame

OPTIMIZED_WEIGHTS = [909.5311585114814, 34.82671836764669, 4.949262700867152, 19.29256367900613, 577.4028970857374, 27.03399070944851, 20.449359384334944, 0.23773537706858194, 89.81225474749954, 11.71038710087402, 0.07946303248350439, 0.011048190069546937, 74.45003244383089, 281.83964667959697, 4.752312530733061, 8.135891926677195, 2.9285781193051275, 17.75590334367726, 1.9110210483360257, 233.21615270854056, 0.864323936900957, 20.212088377808122, 26.847206277494262, 1.6906154200180823, 1.0, 28.984949707290635, 43.1749148100976, 100.0, 31.549901621507836, 18.418632215138036, 0.33543549696671837, 38.02001168011155, 4.795852074912625, 0.020602790819679306, 0.005795604405495203, 31.987428534648675, 49.615431936149236, 48.21723217069149, 13.541283911537416, 3.586232533244882]

def get_depth_and_time(board):
    num_moves = len(list(board.move_stack))
    time = 5 / 100 * (num_moves // 2) + 1
    depth = 20 / 100 * (num_moves // 2) + 16

    if depth > 28:
        depth = 24
    
    if time > 5:
        time = 5

    return (time, int(depth))

def stockfish_evaluation(board, engine):
    two_ply_moves = 4

    move_sequences = {}
    total_moves = len(list(board.legal_moves))
    best_moves_ascending = []

    (time, depth) = get_depth_and_time(board)

    print(f"Time: {time}, Depth: {depth}")

    for move in tqdm(board.legal_moves, desc="Evaluating Moves", unit="move", total=total_moves, position=1, unit_scale=True):
        info = engine.analyse(board, chess.engine.Limit(time=time, depth=depth), root_moves=[move])
        principle_moveset = info['pv']
        score = info['score']

        move_sequences[move.uci()] = {
            'score': info['score'],
            'next_moves': info['pv'][:two_ply_moves * 2]
        }

        best_moves_ascending.append((move, score))

    best_moves_ascending.sort(key=lambda x: x[1].relative.score(mate_score=2000), reverse=chess.WHITE)
    move_sequences['stockfish'] = {
        'score': best_moves_ascending[0][1],
        'move': best_moves_ascending[0][0],
    }

    ranked_moves = {move.uci(): rank + 1 for rank, (move, _) in enumerate(best_moves_ascending)}
    
    print(f"Ranked Moves: {ranked_moves}")
    print(f"Best Moves: {best_moves_ascending}")
    return move_sequences, ranked_moves

def stockfish_move(board, engine):
    result = engine.play(board, chess.engine.Limit(time=0.1, depth=4))
    return result.move

def bonj_move(board, stockfish_engine):
    move_sequences, ranked_moves = stockfish_evaluation(board, stockfish_engine)
    board_data = (board, [], move_sequences, ranked_moves, {})

    bonj = ChessGame(board_data)
    bonj.update_weights(OPTIMIZED_WEIGHTS)

    return bonj.get_best_move()

def play_game():
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    stockfish_engine = chess.engine.SimpleEngine.popen_uci("./stockfish")
    while not board.is_game_over():
        print(f"PGN: {game}\n")
        print(f"Board {board}\n")

        if board.turn == chess.WHITE:
            move = bonj_move(board, stockfish_engine)
        else:
            move = stockfish_move(board, stockfish_engine)

        board.push(move)
        node = node.add_variation(move)
        time.sleep(1)  # Optional delay to see the moves

    print("Game Over")
    print("Result:", board.result())

if __name__ == "__main__":
    play_game()
