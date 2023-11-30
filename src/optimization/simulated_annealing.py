
import random
import math
import numpy as np
from src.utility.chess_extraction import extract_random_chess_positions
from src.utility.othello_extraction import extract_random_othello_positions
from src.utility.ttt_extraction import extract_random_ttt_positions
from src.utility.game_chooser import create_base_game
import matplotlib.pyplot as plt
from math import e

class SimulatedAnnealing:
    def __init__(self, game_name, temperature=1, seed=None):
        self.history = []  
        self.weight_history = []  
        self.weight_labels = []
        self.seed = seed

        self.game_name = game_name
        self.temperature = temperature
        self.candidate = self.initialize_candidate()
        
    def initialize_candidate(self):
        if self.game_name == "chess":
            # Getting a random position
            board_data = extract_random_chess_positions(num_positions=1, seed=self.seed)[0]
            # Create the candidate given the set of initial individuals
            return create_base_game(self.game_name, board_data)
        elif self.game_name == "othello":
            board_data = extract_random_othello_positions(num_positions=1, seed=self.seed)[0]
            return create_base_game(self.game_name, board_data)
        elif self.game_name == "tictactoe":
            board_data = extract_random_ttt_positions(num_positions=1, board_number=self.seed)[0]
            return create_base_game(self.game_name, board_data)
        if self.seed:
            self.seed += 1
        # elif self.game_name == "go":
        #     self.game = Go()  # Replace with actual Go initialization
        else:
            raise ValueError("Invalid game name. Supported options: chess, othello, go")

    def plot_evolution_history(self):
        history = self.history
        weight_history = self.weight_history

        iterations = range(1, len(history) + 1)
        best_fitness_values = [entry["best_fitness"] for entry in history]

        # Figure 1: Best Fitness and Best Move Rank
        fig1, axes1 = plt.subplots(1, 2, figsize=(18, 6))  # 1 row, 2 columns
        # Plotting best fitness values
        axes1[0].plot(iterations, best_fitness_values, marker='o')
        axes1[0].set_title(f'Best Fitness. Seed={self.seed}')
        axes1[0].set_xlabel('Iteration')
        axes1[0].set_ylabel('Fitness')

        # Plotting best move rank over time
        best_move_rank_values = [entry["best_move_rank"][0] for entry in history]
        max_moves = history[0]["best_move_rank"][1]

        axes1[1].plot(iterations, best_move_rank_values, marker='o')
        axes1[1].set_title('Rank of Best Move')
        axes1[1].set_xlabel('Iteration')
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

                axes[row_index, col_index].plot(iterations, weights_values, marker='o')
                axes[row_index, col_index].set_title(f'{self.weight_labels[i]}')
                axes[row_index, col_index].set_xlabel('Iteration')
                axes[row_index, col_index].set_ylabel(f'Weight')
                axes[row_index, col_index].set_ylim(self.weight_bounds[i][0], self.weight_bounds[i][1])

            fig.tight_layout()
            plt.show()

        fig1.tight_layout()
        plt.show()
        
    def calculate_probability(self, cur_val, neighbour_val, temperature):
        return e**((neighbour_val - cur_val)/temperature) if neighbour_val <= cur_val else 1
    
    def decrease_temp_geometrically(self, t, alpha):
        return t * alpha
    
    def get_random_weight_neighbour(self):
        def get_random_value(lower, upper):
            return random.uniform(float(lower), float(upper))

        def get_neighbour(value, lower, upper):
            min_val = max(value - 0.01 * abs(upper - lower), lower)
            max_val = min(value + 0.01 * abs(upper - lower), upper)
            return get_random_value(min_val, max_val)

        neighbour_weights = []
        
        for weight, (lower, upper) in zip(self.candidate.get_weights(), self.candidate.get_weight_bounds()):
            neighbour_weights.append(get_neighbour(weight, lower, upper))

        return neighbour_weights

    def iterate(self, iterations_per_temp, target_fitness=None):
        cur_temp = self.temperature

        counter = 0
        cur_fitness_score, cur_best_move, cur_best_score = self.candidate.fitness()
        best_fitness_score, best_best_move, best_best_score, best_best_move_rank = cur_fitness_score, cur_best_move, cur_best_score, self.candidate.rank_move(cur_best_move)
        best_weights = self.candidate.get_weights()
        
        while cur_temp >= 10**(-100):            
            for _ in range(iterations_per_temp):
                counter += 1
                cur_weights = self.candidate.get_weights()
                next_candidate_weights = self.get_random_weight_neighbour()  
                
                self.candidate.update_weights(next_candidate_weights)
                fitness_score, best_move, best_score = self.candidate.fitness()
                
                if target_fitness and best_fitness_score >= target_fitness:
                    print(f"Target fitness reached. Stopping evolution.")
                    cur_temp = 0
                    break

                # Keep track of the best answer found so far:
                if (fitness_score > best_fitness_score):
                    best_fitness_score, best_best_move, best_best_score = fitness_score, best_move, best_score
                    best_best_move_rank = self.candidate.rank_move(best_move)
                    best_weights = next_candidate_weights
                
                prob = self.calculate_probability(cur_fitness_score, fitness_score, self.temperature)
                rnd = random.uniform(0,1)
                
                if rnd <= prob:
                    cur_fitness_score, cur_best_move, cur_best_score = fitness_score, best_move, best_score                                                           
                else:
                    self.candidate.update_weights(cur_weights)
                    
                cur_best_move_rank = self.candidate.rank_move(cur_best_move)
                self.history.append({
                    "best_fitness": cur_fitness_score,
                    "best_move": cur_best_move,
                    "best_score": cur_best_score,
                    "best_move_rank": cur_best_move_rank
                })
                
                self.weight_history.append(self.candidate.get_weights())
                
                print(f"\nIteration {counter + 1}, Best Fitness: {best_fitness_score}, Best Move: {best_best_move} with rank: {best_best_move_rank}")
                print(f"Weights: {best_weights}\n")

            
            cur_temp = self.decrease_temp_geometrically(cur_temp, 0.95)

        self.weight_labels = self.candidate.get_weight_labels()
        self.weight_bounds = self.candidate.get_weight_bounds()
        return self.candidate

