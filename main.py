# main.py

import sys
import configparser
import io
import os
import json
from PIL import Image
from src.optimization.genetic_algorithm import GeneticAlgorithm
from src.optimization.simulated_annealing import SimulatedAnnealing
from src.optimization.pso import PSO
from src.utility.utility import create_and_evaluate_game

def read_config(file_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def main():
    # Parse command-line arguments
    args = sys.argv[1:]

    # Extract seed value if provided
    seed = None
    for arg in args:
        if arg.startswith("seed="):
            seed = int(arg.split("=")[1])

    # Read configuration from the file
    config = read_config()

    # Access game and algorithm choices
    game_name = config.get("Game", "name")
    algorithm_name = config.get("Algorithm", "name")

    # Use the choices in your project
    print(f"Selected Game: {game_name}")
    print(f"Selected Algorithm: {algorithm_name}")
    
    EVALUATE = True
    
    if EVALUATE:
        weights_list = []
        # Number of boards to fit to.
        num_boards_to_fit = 20
        
        for game_num in range(num_boards_to_fit):
            best_individual = None
            if algorithm_name == "genetic_algorithm":
                # Create a GeneticAlgorithm instance
                genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.8, seed=seed)

                # Evolve the population for a certain number of generations
                best_individual = genetic_algorithm.evolve(generations=500)
            elif algorithm_name == "pso":
                pso = PSO(game_name, num_particles=30)
                # Evolve the population for a certain number of generations
                best_individual = pso.iterate(iterations=500)
            elif algorithm_name == "simulated_annealing":
                
                simulated_annealing = SimulatedAnnealing(game_name, temperature=1, seed=seed)
                best_individual = simulated_annealing.iterate(iterations_per_temp=5)
                
            weights_list.append(best_individual.get_weights())
        
        # Combine weights by averaging them out.
        combined_weights = weights_list[0]
        for weight_idx in range(len(weights_list[0])):
            combined_weights[weight_idx] = sum([weights_list[i][weight_idx] for i in range(len(weights_list))])/len(weights_list)
        
        evaluations = []
        num_evaluations = 100 #Number of times the weights are evaluated on different board states.
        # Perform evaluations
        for evaluation in range(num_evaluations): 
            fitness_score, best_move, index, num_moves = create_and_evaluate_game(game_name, combined_weights)
            evaluations.append((fitness_score, str(best_move), index, num_moves))
        
        print(evaluations)
        
        file_path = "evaluations.json"
        with open(file_path, 'w') as json_file:
            json.dump(evaluations, json_file)
            
    else:
        best_individual = None
        if algorithm_name == "genetic_algorithm":
            # Create a GeneticAlgorithm instance
            genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.8, seed=seed)

            # Evolve the population for a certain number of generations
            best_individual = genetic_algorithm.evolve(generations=2000)
            genetic_algorithm.plot_evolution_history()
        elif algorithm_name == "pso":
            pso = PSO(game_name, num_particles=10)
            # Evolve the population for a certain number of generations
            best_individual = pso.iterate(iterations=10)
            pso.plot_evolution_history()
        elif algorithm_name == "simulated_annealing":
            simulated_annealing = SimulatedAnnealing(game_name, temperature=1, seed=seed)

            best_individual = simulated_annealing.iterate(iterations_per_temp=5)
            simulated_annealing.plot_evolution_history()


        if game_name == "chess":
            import cairosvg
            # Visualize the best move
            svg_content = best_individual.visualize_best_move(img_size=400)
            with open("game_board.svg", "w") as svg_file:
                svg_file.write(svg_content)

            # Convert SVG to PNG
            png_bytes = cairosvg.svg2png(url=os.path.abspath("game_board.svg"))

            # Display the PNG image
            image = Image.open(io.BytesIO(png_bytes))
            image.show()
        elif game_name == "othello":
            best_individual.visualize_best_move(img_size=400)
 
if __name__ == "__main__":
    main()
