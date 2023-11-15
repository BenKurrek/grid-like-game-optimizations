# main.py

import configparser
import io
import os
from PIL import Image
import cairosvg
from src.game.base_game import BaseGame
from src.optimization.genetic_algorithm import GeneticAlgorithm

def read_config(file_path="config.ini"):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def main():
    # Read configuration from the file
    config = read_config()

    # Access game and algorithm choices
    game_name = config.get("Game", "name")
    algorithm_name = config.get("Algorithm", "name")

    # Use the choices in your project
    print(f"Selected Game: {game_name}")
    print(f"Selected Algorithm: {algorithm_name}")

    # Create a GeneticAlgorithm instance
    genetic_algorithm = GeneticAlgorithm(game_name, population_size=10, mutation_rate=0.5)

    # Evolve the population for a certain number of generations
    best_individual = genetic_algorithm.evolve(generations=2000)
    genetic_algorithm.plot_evolution_history()

    svg_content = best_individual.visualize_best_move(size=400)
    with open("game_board.svg", "w") as svg_file:
        svg_file.write(svg_content)

    # Convert SVG to PNG
    png_bytes = cairosvg.svg2png(url=os.path.abspath("game_board.svg"))

    # Display the PNG image
    image = Image.open(io.BytesIO(png_bytes))
    image.show()

if __name__ == "__main__":
    main()
