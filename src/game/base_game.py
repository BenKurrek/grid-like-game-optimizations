class BaseGame:
    def __init__(self, game):
        self.game = game
        
    def update_weights(self, weights):
        self.game.update_weights(weights)
    
    def generate_random_state(self):
        return self.game.generate_random_state()
    
    def set_random_state(self):
        return self.game.set_random_state()

    def fitness(self):
        return self.game.fitness()

    def mutate(self, state):
        return self.game.mutate(state)

    def crossover(self, game2):
        return self.game.crossover(game2)

    def get_weights(self):
        return self.game.get_weights()

    def get_svg_content(self, state, size):
        return self.game.get_svg_content(state, size)
