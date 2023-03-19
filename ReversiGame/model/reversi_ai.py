class ReversiAI:
    def __init__(self, depth):
        self.depth = depth

    def get_best_move(self, game):
        possible_moves = game.possible_moves()
        if not possible_moves:
            return None

        best_move = None
        best_score = float('-inf')

        print(possible_moves)
        print(game.board.get_grid())
        print(game.player1_score)
        print(game.player2_score)

    def minimax(self, game, depth, maximizing):
        pass
