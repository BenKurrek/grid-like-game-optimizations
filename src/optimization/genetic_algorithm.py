import random
from src.game.base_game import BaseGame

class GeneticAlgorithm:
    def __init__(self, game_name, population_size=10, mutation_rate=0):
        self.game_name = game_name
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.initialize_population()

    def initialize_population(self):
        return [BaseGame(self.game_name) for _ in range(self.population_size)]

    def evolve(self, generations, target_fitness=None):
        for generation in range(generations):
            # Evaluate the fitness scores of each member of the population
            fitness_scores = [(individual, individual.fitness()) for individual in self.population]
            fitness_scores.sort(key=lambda x: x[1], reverse=True)

            best_individual, best_fitness = fitness_scores[0]
            
            if target_fitness and best_fitness >= target_fitness:
                print(f"Target fitness reached. Stopping evolution.")
                break

            parents = [individual for individual, _ in fitness_scores[:self.population_size // 2]]
            new_population = parents.copy()

            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(parents, 2)
                child = parent1.crossover(parent2)
                if random.random() < self.mutation_rate:
                    child = self.game.mutate(child)
                    
                new_population.append(child)

            self.population = new_population

            print(f"Generation {generation + 1}, Best Fitness: {best_fitness}")

        return best_individual
