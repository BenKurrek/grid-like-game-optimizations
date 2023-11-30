import chess
import chess.pgn
import chess.engine
from tqdm import tqdm
import time
from src.game.chess.chess_game import ChessGame

OPTIMIZED_WEIGHTS = [927.7280191624782, 83.08823957262602, 15.343374060129644, 4.473831328015487, 537.8854560005145, 17.55686262711021, 0.14261403655964622, 0.2060585787812097, 1.1593834488541233, 0.4071849945450623, 6.759968443600224, 0.10193100641349151, 95.91108180009874, 360.4302874051135, 4.493237030068775, 4.792727401898991, 33.75930653023406, 0.39051821197877423, 72.636094287533, 415.9525522895785, 27.71102751607682, 0.3835361635716794, 2.403460127239865, 18.016974323154, 1.0, 11.124343041847926, 15.390020588960486, 100.0, 3.009113750301795, 0.06593957017376195, 0.15980803519064501, 0.8760315878773017, 9.993067154447713, 0.032979278718681115, 1.5273365331153088, 0.9043514614281378, 49.58821431251195, 40.50380067586322, 48.27420526228854, 0.0902644325052826]

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
    two_ply_moves = 8

    move_sequences = {}
    total_moves = len(list(board.legal_moves))
    best_moves_ascending = []

    (time, depth) = (2, 24)

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
    result = engine.play(board, chess.engine.Limit(time=0.01))
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
