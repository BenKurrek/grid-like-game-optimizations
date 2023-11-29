from src.game.base_game import BaseGame
from src.optimization.genetic_algorithm import GeneticAlgorithm
from src.utility.chess_extraction import extract_random_chess_positions
from src.utility.othello_extraction import extract_random_othello_positions
from src.utility.game_chooser import create_base_game
import chess

def create_and_evaluate_game(game_name, weights, board_num) -> tuple[float, chess.Move, int, int]:
    # Create game
    board_data = None
    if game_name == "chess":
        # Individuals in the population each start with the same random position.
        # Their chromosomes are made up of genes representing fitness function weights
        board_data = extract_random_chess_positions(num_positions=1, seed=board_num)[0]
        # Create the population given the set of initial individuals
    elif game_name == "othello":
        board_data = extract_random_othello_positions(seed=board_num, num_positions=1, randomize=False, dataset="test")[0]
        
    game = create_base_game(game_name, board_data)
    
    # Set weights
    game.update_weights(weights)
    
    fitness_score, best_move, best_score = game.fitness()
    index, num_moves = game.rank_move(best_move)
    
    return fitness_score, best_move, index, num_moves