class BaseGame:
    def __init__(self, game_name):
        self.game_name = game_name
        self.initialize()

    def initialize(self):
        if self.game_name == "chess":
            from .chess import ChessGame # Avoid circular import
            self.game = ChessGame(self.game_name)  # Pass the game_name argument
        # elif self.game_name == "othello":
        #     self.game = Othello()  # Replace with actual Othello initialization
        # elif self.game_name == "go":
        #     self.game = Go()  # Replace with actual Go initialization
        else:
            raise ValueError("Invalid game name. Supported options: chess, othello, go")

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

    def crossover(self, parent1, parent2):
        return self.game.crossover(parent1, parent2)

    def get_svg_content(self, state, size):
        return self.game.get_svg_content(state, size)
