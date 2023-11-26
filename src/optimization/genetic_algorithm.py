import random
from src.utility.chess_extraction import extract_random_chess_positions
from src.utility.othello_extraction import extract_random_othello_positions
from src.utility.game_chooser import create_base_game
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, game_name, population_size=10, mutation_rate=0, seed=None):
        self.history = []  
        self.weight_history = []  
        self.weight_labels = []
        self.weight_bounds = []
        self.seed = seed

        self.game_name = game_name
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def plot_evolution_history(self):
        history = self.history
        weight_history = self.weight_history

        generations = range(1, len(history) + 1)
        best_fitness_values = [entry["best_fitness"] for entry in history]

        # Figure 1: Best Fitness and Best Move Rank
        fig1, axes1 = plt.subplots(1, 2, figsize=(18, 6))  # 1 row, 2 columns
        # Plotting best fitness values
        axes1[0].plot(generations, best_fitness_values, marker='o')
        axes1[0].set_title(f'Best Fitness. Seed={self.seed}')
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

    def initialize_population(self):
        if self.game_name == "chess":
            # Individuals in the population each start with the same random position.
            # Their chromosomes are made up of genes representing fitness function weights
            board_data = extract_random_chess_positions(num_positions=1, seed=self.seed)[0]
            # Create the population given the set of initial individuals
            return [create_base_game(self.game_name, board_data) for _ in range(self.population_size)]
        elif self.game_name == "othello":
            board_data = extract_random_othello_positions(num_positions=1)[0]
            return [create_base_game(self.game_name, board_data) for _ in range(self.population_size)]
        # elif self.game_name == "go":
        #     self.game = Go()  # Replace with actual Go initialization
        else:
            raise ValueError("Invalid game name. Supported options: chess, othello, go")

    def mutate(self, game):
        # Randomly choose 3 weights to mutate
        weights = game.get_weights()
        weight_bounds = game.get_weight_bounds()

        weight_indices = random.sample(range(len(weights)), len(weights)//3)
        for weight_idx in weight_indices:
            weights[weight_idx] = random.uniform(float(weight_bounds[weight_idx][0]), float(weight_bounds[weight_idx][1]))
        
        game.update_weights(weights)

    def crossover(self, game1, game2):
        child_weights = []
        
        weights1 = game1.get_weights()
        weights2 = game2.get_weights()

        for idx in range(len(weights1)):
            # Randomly choose weights from either parent
            child_weights.append(random.choice([weights1[idx], weights2[idx]]))

        # Create a new ChessGame instance for the child
        board_data = game1.get_board_data()
        child_game = create_base_game(self.game_name, board_data)
        child_game.update_weights(child_weights)
        return child_game

    def evolve(self, generations, target_fitness=None):
        for generation in range(generations):
            fitness_scores = []
            # Evaluate the fitness scores of each individual in the population
            for individual in self.population:
                fitness_score, best_move, best_score = individual.fitness()
                fitness_scores.append((individual, (fitness_score, best_move, best_score)))
               # print(f"Chosen Move: {best_move}. Evaluated Score: {best_score}. Fitnesss: {fitness_score}")
            
            # Sort to get the top fitness scores for the next generation
            fitness_scores.sort(key=lambda x: x[1][0], reverse=True)
            best_individual, best_fitness_data = fitness_scores[0]
            best_fitness_score, best_move, best_score = best_fitness_data

            if target_fitness and best_fitness_score >= target_fitness:
                print(f"Target fitness reached. Stopping evolution.")
                break

            # Parents are the best individuals in the population based on fitness
            # Choose half the parents to reproduce and create a new population
            parents = [individual for individual, _ in fitness_scores[:self.population_size // 2]]
            new_population = parents.copy()

            # Keep reproducing until the new population is the same size as the old population
            while len(new_population) < self.population_size:
                # Randomly select two parents to reproduce
                parent1, parent2 = random.sample(parents, 2)
                child = self.crossover(parent1, parent2)
                
                # Randomly mutate the child based on the mutation rate
                if random.random() < self.mutation_rate:
                    self.mutate(child)

                new_population.append(child)

            self.population = new_population

            best_move_rank = best_individual.rank_move(best_move)
            self.history.append({
                "best_fitness": best_fitness_score,
                "best_move": best_move,
                "best_score": best_score,
                "best_move_rank": best_move_rank
            })
            self.weight_history.append(best_individual.get_weights())

            print(f"\nGeneration {generation + 1}, Best Fitness: {best_fitness_score}, Best Move: {best_move} with rank: {best_move_rank}")
            print(f"Weights: {best_individual.get_weights()}\n")

        self.weight_labels = best_individual.get_weight_labels()
        self.weight_bounds = best_individual.get_weight_bounds()
        return best_individual
