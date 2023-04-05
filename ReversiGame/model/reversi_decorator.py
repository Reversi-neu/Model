from model.game import Reversi
from model.reversi_interface import ReversiInterface
import copy

class ReversiDecorator(ReversiInterface):
    def __init__(self, reversi):
        self.reversi = reversi

    def is_valid_move(self, move):
        return self.reversi.is_valid_move(move)

    def make_move(self, move):
        return self.reversi.make_move(move)

    def change_cur_player(self):
        return self.reversi.change_cur_player()

    def check_win(self):
        return self.reversi.check_win()

    def possible_moves(self):
        return self.reversi.possible_moves()

    def copy(self):
        return self.reversi.copy()

    def __getattr__(self, attr):
        if attr == '__deepcopy__':
            return lambda memo: copy.deepcopy(self.reversi, memo)
        return getattr(self.reversi, attr)