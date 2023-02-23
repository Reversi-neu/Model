from abc import ABC, abstractmethod

class GameLogic(ABC):
    def __init__(self):
        self.size = 8
        pass

    @abstractmethod
    def get_size(self, s):
        pass

    @abstractmethod
    def is_move_possible(self, board, move, player):
        pass

    @abstractmethod
    def make_move(self, board, move, player):
        pass

    @abstractmethod
    def possible_moves(self, board, player):
        pass

    @abstractmethod
    def check_win(self, board):
        pass

    
