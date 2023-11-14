import random
from src.utility.chess_extraction import extract_random_chess_positions
from src.utility.game_chooser import create_base_game

class GeneticAlgorithm:
    def __init__(self, game_name, population_size=100, mutation_rate=0):        
        self.game_name = game_name
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        if self.game_name == "chess":
            from src.game.chess import ChessGame # Avoid circular import
            # Individuals in the population each start with the same random position.
            # Their chromosomes are made up of genes representing fitness function weights
            board_data = extract_random_chess_positions(num_positions=1)[0]
            # Create the population given the set of initial individuals
            return [create_base_game(self.game_name, board_data) for _ in range(self.population_size)]
        # elif self.game_name == "othello":
        #     self.game = Othello( )  # Replace with actual Othello initialization
        # elif self.game_name == "go":
        #     self.game = Go()  # Replace with actual Go initialization
        else:
            raise ValueError("Invalid game name. Supported options: chess, othello, go")

    def evolve(self, generations, target_fitness=None):
        for generation in range(generations):
            # Evaluate the fitness scores of each individual in the population
            fitness_scores = [(individual, individual.fitness()) for individual in self.population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            best_individual, best_fitness = fitness_scores[0]

            print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")
            print(f"Weights: {best_individual.get_weights()}\n")
            
            if target_fitness and best_fitness >= target_fitness:
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
                child = parent1.crossover(parent2)
                
                # Randomly mutate the child based on the mutation rate
                if random.random() < self.mutation_rate:
                    child.mutate()

                new_population.append(child)

            self.population = new_population

            print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

        return best_individual
