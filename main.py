# main.py

import sys
import configparser
import io
import os
from PIL import Image
from colorama import Fore, Style
from src.game.base_game import BaseGame
from src.optimization.genetic_algorithm import GeneticAlgorithm
from src.optimization.simulated_annealing import SimulatedAnnealing
from src.optimization.pso import PSO

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
    
    best_individual = None
    if algorithm_name == "genetic_algorithm":
        # Create a GeneticAlgorithm instance

        # Evolve the population for a certain number of generations
        if game_name == "tictactoe":
            genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.5)
            generations = 20
        else:
            genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.5)
            generations = 500

        best_individual = genetic_algorithm.evolve(generations=generations)
        #genetic_algorithm.plot_evolution_history()
        genetic_algorithm = GeneticAlgorithm(game_name, population_size=20, mutation_rate=0.8, seed=seed)

        # Evolve the population for a certain number of generations
        best_individual = genetic_algorithm.evolve(generations=generations)
        genetic_algorithm.plot_evolution_history()
    elif algorithm_name == "pso":
        if game_name == "tictactoe":
            pso = PSO(game_name, num_particles=2)
        else:
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
