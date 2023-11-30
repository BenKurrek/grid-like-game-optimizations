import sys
import configparser
import io
import os
from PIL import Image
from src.game.base_game import BaseGame
from src.optimization.genetic_algorithm import GeneticAlgorithm
from src.optimization.simulated_annealing import SimulatedAnnealing
from src.optimization.pso import PSO

def train_engine():
    def train_for_one_generation():
        genetic_algorithm = GeneticAlgorithm("chess", population_size=20, mutation_rate=0.8, seed=None)
        # Evolve the population for a certain number of generations
        best_individual = genetic_algorithm.evolve(generations=500)
        return best_individual.get_weights()

    cumulative_weights = train_for_one_generation()
    print(f"Generation 0: {cumulative_weights}")
    num_generations = 100
    
    for i in range(1, num_generations + 1):
        weights = train_for_one_generation()
        print(f"Generation {i}: {weights}")

        cumulative_weights = [cw + w for cw, w in zip(cumulative_weights, weights)]

    average_weights = [weight / (num_generations + 1) for weight in cumulative_weights]
    print(f"Average Weights: {average_weights}")

if __name__ == "__main__":
    train_engine()