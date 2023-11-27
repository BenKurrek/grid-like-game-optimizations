# Use Von Neumann Topology 

import random
import math
import numpy as np
from src.utility.chess_extraction import extract_random_chess_positions
from src.utility.othello_extraction import extract_random_othello_positions
from src.utility.game_chooser import create_base_game
from src.game.base_game import BaseGame
import matplotlib.pyplot as plt
from copy import deepcopy

from src.utility.ttt_extraction import extract_random_ttt_positions

class PSO():
    def __init__(self, game_name, num_particles=10):
        self.history = []  
        self.weight_history = []  
        self.weight_labels = []
        
        # Initalize PSO weights/
        # TODO Verify these values.
        scale = 0.15
        self.a1 = 0.6
        '''Inertia'''
        self.a2 = 1*scale
        self.a3 = 0.5*scale
        
        self.momentum_limit = 4

        self.game_name = game_name
        self.num_particles = num_particles
        
        # Initalize particles and get best local and global particles.
        self.particles = self.initialize_particles()
        self.local_best = deepcopy(self.particles)
        self.local_best_fitness = [particle.fitness()[0] for particle in self.local_best]
        
        self.particle_momentums = [np.array([0 for j in range(len(particle.get_weights()))]) for particle in self.particles]
        
        self.global_best = self.get_global_best()
        self.global_best_fitness, _, _ = self.global_best.fitness()
        
        
    def initialize_particles(self) -> list[BaseGame]:
        """Initlaize particles for the particlular game being optimized.
        Returns:
            list[BaseGame]: The list of games that are treated as particles.
        """
        if self.game_name == "chess":
            # Individuals in the population each start with the same random position.
            # Their chromosomes are made up of genes representing fitness function weights
            board_data = extract_random_chess_positions(num_positions=1)[0]
            # Create the population given the set of initial individuals
            return [create_base_game(self.game_name, board_data) for _ in range(self.num_particles)]
        elif self.game_name == "othello":
            board_data = extract_random_othello_positions(num_positions=1)[0]
            return [create_base_game(self.game_name, board_data) for _ in range(self.num_particles)]
        elif self.game_name == "tictactoe":
            board_data = extract_random_ttt_positions(num_positions=1)[0]
            return [create_base_game(self.game_name, board_data) for _ in range(self.num_particles)]
        # elif self.game_name == "go":
        #     self.game = Go()  # Replace with actual Go initialization
        else:
            raise ValueError("Invalid game name. Supported options: chess, othello, go")
        
    def plot_evolution_history(self):
        history = self.history
        weight_history = self.weight_history

        generations = range(1, len(history) + 1)
        best_fitness_values = [entry["best_fitness"] for entry in history]

        # Figure 1: Best Fitness and Best Move Rank
        fig1, axes1 = plt.subplots(1, 2, figsize=(18, 6))  # 1 row, 2 columns
        # Plotting best fitness values
        axes1[0].plot(generations, best_fitness_values, marker='o')
        axes1[0].set_title('Best Fitness')
        axes1[0].set_xlabel('Generation')
        axes1[0].set_ylabel('Fitness')

        # Plotting best move rank over time
        best_move_rank_values = [entry["best_move_rank"][0] for entry in history]
        max_moves = history[0]["best_move_rank"][1]

        axes1[1].plot(generations, best_move_rank_values, marker='o')
        axes1[1].set_title('Rank of Best Move')
        axes1[1].set_xlabel('Generation')
        axes1[1].set_ylabel('Rank')
        axes1[1].set_ylim(1, max_moves)

        # Figure 2: Weights
        total_weights = len(weight_history[0])
        rows_per_figure = 3
        columns_per_figure = 3
        num_figures = (total_weights - 1) // (rows_per_figure * columns_per_figure) + 1

        for figure_num in range(num_figures):
            fig, axes = plt.subplots(rows_per_figure, columns_per_figure, figsize=(18, 6))
            start_index = figure_num * rows_per_figure * columns_per_figure
            end_index = min((figure_num + 1) * rows_per_figure * columns_per_figure, total_weights)

            # Plotting weights
            for i in range(start_index, end_index):
                weights_values = [weights[i] for weights in weight_history]

                row_index = (i - start_index) // columns_per_figure
                col_index = (i - start_index) % columns_per_figure

                axes[row_index, col_index].plot(generations, weights_values, marker='o')
                axes[row_index, col_index].set_title(f'{self.weight_labels[i]}')
                axes[row_index, col_index].set_xlabel('Generation')
                axes[row_index, col_index].set_ylabel(f'Weight')
                axes[row_index, col_index].set_ylim(self.weight_bounds[i][0], self.weight_bounds[i][1])

            fig.tight_layout()
            plt.show()

        fig1.tight_layout()
        plt.show()

    def get_global_best(self) -> BaseGame:
        """Get the global best of local bests.

        Returns:
            BaseGame: Global best
        """
        best_fitness = -math.inf
        global_best_idx = None
        
        # Loop through each local best particle and find the global best.
        for idx, particle in enumerate(self.local_best):
            fitness, _, _ = particle.fitness()
            if fitness > best_fitness:
                best_fitness = fitness
                global_best_idx = idx
                
        return self.local_best[global_best_idx]

    def iterate_particle(self, particle_id):
        # Get local, global, and particle weights
        local_best_weights = np.array(self.local_best[particle_id].get_weights())
        local_best_fitness = self.local_best_fitness[particle_id]
        
        global_best_weights = np.array(self.global_best.get_weights())
    
        particle_weights = np.array(self.particles[particle_id].get_weights())
        
        # Calculate momentum based on the ECE457A definition of momentum.
        momentum = self.a1*self.particle_momentums[particle_id] + self.a2*(local_best_weights-particle_weights) + self.a3*(global_best_weights-particle_weights)
        # Limit the momentum from becoming too large.
        for i in range(len(momentum)):
            if momentum[i] > self.momentum_limit:
                momentum[i] = self.momentum_limit
            elif momentum[i] < -self.momentum_limit:
                momentum[i] = -self.momentum_limit
        
        # Update weights
        next_weights = particle_weights + momentum
        self.particles[particle_id].update_weights(list(next_weights))
        
        # Update momentum and check local best.
        self.particle_momentums[particle_id] = momentum
        
        new_particle_fitness, _, _ = self.particles[particle_id].fitness()
        if local_best_fitness < new_particle_fitness:
            self.local_best[particle_id] = deepcopy(self.particles[particle_id])
            self.local_best_fitness[particle_id] = new_particle_fitness
            
        if self.global_best_fitness < new_particle_fitness:
            self.global_best = deepcopy(self.particles[particle_id])
            self.global_best_fitness = new_particle_fitness
        
        
        
    def iterate(self, iterations, target_fitness=None) -> BaseGame:
        for i in range(iterations):
            fitness_scores = []
            # Evaluate the fitness scores of each individual in the population
            for particle in self.particles:
                fitness_score, best_move, best_score = particle.fitness()
                fitness_scores.append((particle, (fitness_score, best_move, best_score)))
               # print(f"Chosen Move: {best_move}. Evaluated Score: {best_score}. Fitnesss: {fitness_score}")
                        
            best_individual = self.global_best
            best_fitness_score, best_move, best_score = self.global_best.fitness()

            if target_fitness and best_fitness_score >= target_fitness:
                print(f"Target fitness reached. Stopping evolution.")
                break

            # Perform PSO iteration.
            for particle_idx in range(len(self.particles)):
                self.iterate_particle(particle_idx)

            
            # # Parents are the best individuals in the population based on fitness
            # # Choose half the parents to reproduce and create a new population
            # parents = [individual for individual, _ in fitness_scores[:self.population_size // 2]]
            # new_population = parents.copy()

            # # Keep reproducing until the new population is the same size as the old population
            # while len(new_population) < self.population_size:
            #     # Randomly select two parents to reproduce
            #     parent1, parent2 = random.sample(parents, 2)
            #     child = self.crossover(parent1, parent2)
                
            #     # Randomly mutate the child based on the mutation rate
            #     if random.random() < self.mutation_rate:
            #         self.mutate(child)

            #     new_population.append(child)

            # self.population = new_population

            best_move_rank = best_individual.rank_move(best_move)
            self.history.append({
                "best_fitness": best_fitness_score,
                "best_move": best_move,
                "best_score": best_score,
                "best_move_rank": best_move_rank
            })
            self.weight_history.append(best_individual.get_weights())

            print(f"\nIteration {i + 1}, Best Fitness: {best_fitness_score}, Best Move: {best_move} with rank: {best_move_rank}")
            print(f"Weights: {best_individual.get_weights()}\n")

        self.weight_labels = best_individual.get_weight_labels()
        self.weight_bounds = best_individual.get_weight_bounds()
        return best_individual