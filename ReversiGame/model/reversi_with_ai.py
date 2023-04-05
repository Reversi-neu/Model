from model.reversi_decorator import ReversiDecorator
from model.reversi_ai import ReversiAI

class ReversiWithAI(ReversiDecorator):
    def __init__(self, reversi, ai_depth=0):
        super().__init__(reversi)
        if ai_depth != 0:
            self.ai = ReversiAI(ai_depth)

    def get_ai_move(self):
        self.reversi.check_win()
        return self.ai.get_best_move(self.reversi.copy())