from abc import ABC, abstractmethod

class ReversiInterface(ABC):

    @abstractmethod
    def is_valid_move(self, move):
        pass

    @abstractmethod
    def make_move(self, move):
        pass

    @abstractmethod
    def change_cur_player(self):
        pass

    @abstractmethod
    def check_win(self):
        pass

    @abstractmethod
    def possible_moves(self):
        pass

    @abstractmethod
    def copy(self):
        pass