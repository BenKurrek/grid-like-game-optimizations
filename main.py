# main.py

import sys
import matplotlib.pyplot as plt
import configparser
import io
import os
import json
from PIL import Image
from copy import deepcopy
from colorama import Fore, Style
from src.game.base_game import BaseGame
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
    print(f"{Fore.MAGENTA}~~~~~~~~~~~~~~~~~~~~   STARTING ALGORITHM   ~~~~~~~~~~~~~~~~~~~~{Style.RESET_ALL}")

    # Access game and algorithm choices
    game_name = config.get("Game", "name")
    algorithm_name = config.get("Algorithm", "name")

    # Use the choices in your project
    print(f"Selected Game: {game_name}")
    print(f"Selected Algorithm: {algorithm_name}")
    
    EVALUATE = True
    LAYER_OPTMIZATION = False
    
    if EVALUATE:
        weights_list = []
        # Number of boards to fit to.
        num_boards_to_fit = 50
        iterations = 500
        seed = 1
        for game_num in range(num_boards_to_fit):
            print(f"Evaluating: {game_num}")
            print(f"Iterations {iterations}")

            best_individual = None
            if algorithm_name == "genetic_algorithm":
                # Create a GeneticAlgorithm instance
                genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.8, seed=seed)

                # Evolve the population for a certain number of generations
                best_individual = genetic_algorithm.evolve(generations=100)
            elif algorithm_name == "pso":
                pso = PSO(game_name, num_particles=10, seed=seed)
                # Evolve the population for a certain number of generations
                best_individual = pso.iterate(iterations=iterations)
            elif algorithm_name == "simulated_annealing":
                
                simulated_annealing = SimulatedAnnealing(game_name, temperature=1, seed=seed)
                best_individual = simulated_annealing.iterate(iterations_per_temp=5)
                
            weights_list.append(best_individual.get_weights())
        
        # Combine weights by averaging them out.
        combined_weights = deepcopy(weights_list[0])
        for weight_idx in range(len(weights_list[0])):
            combined_weights[weight_idx] = sum([weights_list[i][weight_idx] for i in range(len(weights_list))])/len(weights_list)
        
        evaluations = []
        num_evaluations = 100 #Number of times the weights are evaluated on different board states.
        # Perform evaluations
        for evaluation in range(num_evaluations): 
            fitness_score, best_move, index, num_moves = create_and_evaluate_game(game_name, combined_weights, evaluation+seed)
            evaluations.append((fitness_score, str(best_move), index, num_moves))
        
        print(evaluations)
        
        file_path = f"{algorithm_name}_{game_name}_evaluations_{iterations}.json"
        with open(file_path, 'w') as json_file:
            json.dump(evaluations, json_file)
        with open(f"weights_{iterations}.json", 'w') as json_file:
            json.dump(combined_weights, json_file)
    
    elif LAYER_OPTMIZATION:
        history = None
        seed = 24
        iterations = 2000
        for particles in [5,10,20]:
            if algorithm_name == "genetic_algorithm":
                # Create a GeneticAlgorithm instance
                genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.8, seed=seed)

                # Evolve the population for a certain number of generations
                best_individual = genetic_algorithm.evolve(generations=2000)
                history = genetic_algorithm.history
                # genetic_algorithm.plot_evolution_history()
            elif algorithm_name == "pso":
                pso = PSO(game_name, num_particles=particles, seed=seed)
                # Evolve the population for a certain number of generations
                best_individual = pso.iterate(iterations=iterations)
                history = pso.history
                # pso.plot_evolution_history()
            elif algorithm_name == "simulated_annealing":
                simulated_annealing = SimulatedAnnealing(game_name, temperature=particles, seed=seed)

                best_individual = simulated_annealing.iterate(iterations_per_temp=4)
                history = simulated_annealing.history
                # simulated_annealing.plot_evolution_history()
        
            generations = range(1, len(history) + 1)
            best_fitness_values = [entry["best_fitness"] for entry in history]
            
            # Plotting best fitness values
            plt.plot(generations, best_fitness_values, linewidth=1.5, label=f"Particles: {particles}")
        plt.title(f'Best particle fitness comparison for {algorithm_name}\n with different numbers of particles on {game_name}.')
        plt.xlabel('Iterations')
        plt.ylabel('Fitness')
        # Add a legend
        plt.legend()

        # Show the plot
        plt.show()
        
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
