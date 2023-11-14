class BaseGame:
    def __init__(self, game):
        self.game = game
        
    def update_weights(self, weights):
        self.game.update_weights(weights)
    
    def get_best_move(self):
        return self.game.get_best_move()
    
    def set_random_state(self):
        return self.game.set_random_state()

    def fitness(self):
        return self.game.fitness()

    def mutate(self):
        return self.game.mutate()

    def crossover(self, game2):
        return BaseGame(self.game.crossover(game2))

    def get_weights(self):
        return self.game.get_weights()

    def visualize_best_move(self, size):
        best_move = self.game.get_best_move()
        return self.game.visualize_best_move(best_move, size)
