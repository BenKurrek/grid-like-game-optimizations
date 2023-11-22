from abc import ABC, abstractmethod

class BaseGame(ABC):
    @abstractmethod
    def update_weights(self, weights):
        pass

    @abstractmethod
    def get_board_data(self):
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
    def get_weights(self):
        pass

    @abstractmethod
    def get_weight_bounds(self):
        pass
    
    @abstractmethod
    def get_weight_labels(self):
        pass

    @abstractmethod
    def visualize_best_move(self, img_size):
        pass
