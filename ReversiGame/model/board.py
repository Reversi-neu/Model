from model.player import Player

class Board:
    def __init__(self, size, board=[]):
        self.size = size
        self.board = board

        for i in range(size):
            self.board.append([0] * size)

    def __getitem__(self, coordinate):
        return self.board[coordinate[1]][coordinate[0]]

    def __setitem__(self, coordinate, player: Player):
        self.board[coordinate[1]][coordinate[0]] = player

    def get_grid(self):
        return self.board