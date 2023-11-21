from abc import ABC, abstractmethod

class BaseGame(ABC):
    def __init__(self, game):
        self.game = game
       
    @abstractmethod
    def update_weights(self, weights):
        pass

    @abstractmethod
    def get_best_move(self):
        pass

    @abstractmethod
    def rank_move(self, move):
        pass

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def crossover(self, game2):
        pass

    def get_weights(self):
        pass
    
    @abstractmethod
    def get_weight_labels(self):
        pass

    @abstractmethod
    def visualize_best_move(self, img_size):
        pass
